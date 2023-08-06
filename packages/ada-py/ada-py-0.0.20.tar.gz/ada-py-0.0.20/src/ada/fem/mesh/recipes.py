from itertools import chain

import gmsh
import meshio

from ada import FEM, Beam
from ada.config import Settings as _Settings
from ada.fem import FemSection, FemSet
from ada.fem.shapes import ElemType
from ada.ifc.utils import create_guid

from .gmshapi import (
    _init_gmsh_session,
    eval_thick_normal_from_cog_of_beam_plate,
    get_nodes_and_elements,
    get_point,
)


def create_plate_mesh(
    plate,
    geom_repr=ElemType.SOLID,
    max_size=0.1,
    order=1,
    algo=8,
    tol=1e-3,
    fem=None,
    interactive=False,
    gmsh_session=None,
    gmsh_silent=False,
):
    """

    :param plate:
    :param gmsh_session:
    :param geom_repr:
    :param max_size:
    :param order:
    :param algo: Mesh algorithm
    :param tol: Maximum geometry tolerance
    :param fem:
    :param interactive:
    :param gmsh_silent:

    :type plate: ada.Plate
    :type fem: ada.fem.FEM
    :type gmsh_session: gmsh
    """
    temp_dir = _Settings.temp_dir
    if gmsh_session is None:
        gmsh_session = _init_gmsh_session(gmsh_silent)

    option = gmsh_session.option
    model = gmsh_session.model

    option.setNumber("Mesh.Algorithm", algo)
    option.setNumber("Mesh.MeshSizeFromCurvature", True)
    option.setNumber("Mesh.MinimumElementsPerTwoPi", 12)
    option.setNumber("Mesh.MeshSizeMax", max_size)
    option.setNumber("Mesh.ElementOrder", order)
    option.setNumber("Mesh.SecondOrderIncomplete", 1)
    option.setNumber("Mesh.Smoothing", 3)

    option.setNumber("Geometry.Tolerance", tol)
    option.setNumber("Geometry.OCCImportLabels", 1)  # import colors from STEP

    if geom_repr == ElemType.SOLID:
        option.setNumber("Geometry.OCCMakeSolids", 1)

    name = f"temp_{create_guid()}"
    plate.to_stp(temp_dir / name, geom_repr=geom_repr)
    gmsh_session.merge(str(temp_dir / f"{name}.stp"))

    factory = model.geo

    factory.synchronize()

    model.mesh.setRecombine(2, 1)
    model.mesh.generate(3)
    model.mesh.removeDuplicateNodes()

    if interactive:
        gmsh_session.fltk.run()

    if fem is None:
        gmsh_session.write(str(temp_dir / f"{name}.msh"))
        m = meshio.read(str(temp_dir / f"{name}.msh"))
        m.write(temp_dir / f"{name}.xdmf")
        gmsh.finalize()
        return None

    fem_set_name = f"{plate.name}_all"
    get_nodes_and_elements(gmsh_session, fem, fem_set_name=fem_set_name)

    femset = fem.elsets[fem_set_name]
    if geom_repr == ElemType.SOLID:
        fem_sec = FemSection(
            f"{plate.name}_sec",
            ElemType.SOLID,
            femset,
            plate.material,
        )
    else:
        fem_sec = FemSection(
            f"{plate.name}_sec",
            ElemType.SHELL,
            femset,
            plate.material,
            local_z=plate.n,
            thickness=plate.t,
            int_points=5,
        )
    fem.add_section(fem_sec)


def create_beam_mesh(
    beam: Beam,
    fem: FEM,
    geom_repr=ElemType.SHELL,
    max_size=0.1,
    order=1,
    algo=8,
    tol=1e-3,
    interactive=False,
    gmsh_session=None,
    gmsh_silent=False,
):
    """
    :param beam:
    :param gmsh_session:
    :param geom_repr:
    :param max_size:
    :param order:
    :param algo: Mesh algorithm
    :param tol: Maximum geometry tolerance
    :param interactive:
    :param gmsh_silent:
    :type beam: ada.Beam
    :type fem: ada.fem.FEM
    :type gmsh_session: gmsh
    """
    if gmsh_session is None:
        gmsh_session = _init_gmsh_session(gmsh_silent)

    temp_dir = _Settings.temp_dir
    name = beam.name.replace("/", "") + f"_{create_guid()}"
    option = gmsh_session.option
    model = gmsh_session.model

    option.setNumber("Mesh.Algorithm", algo)
    option.setNumber("Mesh.MeshSizeFromCurvature", True)
    option.setNumber("Mesh.MinimumElementsPerTwoPi", 12)
    option.setNumber("Mesh.MeshSizeMax", max_size)
    option.setNumber("Mesh.ElementOrder", order)
    option.setNumber("Mesh.SecondOrderIncomplete", 1)
    option.setNumber("Mesh.Smoothing", 3)

    option.setNumber("Geometry.Tolerance", tol)
    option.setNumber("Geometry.OCCImportLabels", 1)  # import colors from STEP

    if geom_repr == ElemType.SOLID:
        option.setNumber("Geometry.OCCMakeSolids", 1)

    model.add(name)

    if geom_repr in [ElemType.SOLID, ElemType.SHELL]:
        beam.to_stp(temp_dir / name, geom_repr=geom_repr)
        gmsh_session.open(str(temp_dir / f"{name}.stp"))
    else:  # beam
        p1, p2 = beam.n1.p, beam.n2.p
        s = get_point(p1, gmsh_session)
        e = get_point(p2, gmsh_session)
        if len(s) == 0:
            s = [(0, model.geo.addPoint(*p1.tolist(), max_size))]
        if len(e) == 0:
            e = [(0, model.geo.addPoint(*p2.tolist(), max_size))]

    model.geo.synchronize()
    model.mesh.setRecombine(3, 1)
    model.mesh.generate(3)
    model.mesh.removeDuplicateNodes()

    if interactive:
        gmsh_session.fltk.run()

    get_nodes_and_elements(gmsh_session, fem)

    # This is needed for code aster MED to do proper roundtripping
    fem.nodes.renumber()

    if fem is None:
        gmsh_session.write(str(temp_dir / f"{name}.msh"))
        m = meshio.read(str(temp_dir / f"{name}.msh"))
        m.write(temp_dir / f"{name}.xdmf")

        gmsh.finalize()
        return None

    # TODO: Identify which part of cross section the entities belong to and add physical group to assign section props
    # Alternatively it might be more simple to just build the geometries from scratch.
    # p1, p2 = beam.n1.p, beam.n2.p
    if geom_repr == ElemType.SOLID:
        fem_sec = FemSection(
            f"{beam.name}_sec",
            ElemType.SOLID,
            fem.elsets["all_elements"],
            beam.material,
        )
        fem.add_section(fem_sec)
    elif geom_repr == ElemType.SHELL:
        # Get element section properties
        ents = gmsh.model.occ.getEntities(2)
        for dim, ent in ents:
            r = model.occ.getCenterOfMass(2, ent)
            t, n, c = eval_thick_normal_from_cog_of_beam_plate(beam, r)
            # name = model.getEntityName(dim, ent)
            tags, coord, param = model.mesh.getNodes(2, ent, True)
            # get surface normal on all nodes, i.e. including on the geometrical
            # singularities (edges/points)
            # normals = gmsh.model.getNormal(ent, param)
            # curv = gmsh.model.getCurvature(2, ent, param)
            # print(ent, r)
            elemTypes, elemTags, elemNodeTags = model.mesh.getElements(2, ent)
            femset = FemSet(
                f"{beam.name}_ent{ent}", [fem.elements.from_id(x) for x in chain.from_iterable(elemTags)], "elset"
            )
            fem.add_set(femset)
            fem_sec = FemSection(
                f"{beam.name}_{c}_{ent}",
                ElemType.SHELL,
                femset,
                beam.material,
                local_z=n,
                thickness=t,
                int_points=5,
            )
            fem.add_section(fem_sec)
    else:
        fem_sec = FemSection(
            f"d{beam.name}_sec",
            ElemType.LINE,
            fem.elsets["all_elements"],
            beam.material,
            beam.section,
            beam.ori[2],
        )
        fem.add_section(fem_sec)

    gmsh.finalize()
