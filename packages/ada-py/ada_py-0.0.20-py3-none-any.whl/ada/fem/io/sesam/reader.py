import logging
import os
from itertools import chain, count
from typing import List

import numpy as np

from ada.concepts.containers import Materials, Nodes, Sections
from ada.concepts.levels import FEM, Assembly, Part
from ada.concepts.points import Node
from ada.concepts.structural import Section
from ada.core.utils import roundoff, unit_vector, vector_length
from ada.fem import Bc, Constraint, Csys, Elem, FemSection, FemSet, Mass, Spring
from ada.fem.containers import FemElements, FemSections
from ada.fem.io.utils import str_to_int
from ada.fem.shapes import ElemShapes, ElemType
from ada.materials import Material
from ada.materials.metals import CarbonSteel
from ada.sections import GeneralProperties

from . import cards
from .common import sesam_el_map


def read_fem(assembly: Assembly, fem_file: os.PathLike, fem_name: str = None):
    """Import contents from a Sesam fem file into an assembly object"""

    print("Starting import of Sesam input file")
    part_name = "T1" if fem_name is None else fem_name
    with open(fem_file, "r") as d:
        part = read_sesam_fem(d.read(), part_name)

    assembly.add_part(part)


def read_sesam_fem(bulk_str, part_name) -> Part:
    """Reads the content string of a Sesam input file and converts it to FEM objects"""

    part = Part(part_name)
    fem = part.fem

    fem.nodes = get_nodes(bulk_str, fem)
    fem.elements = get_elements(bulk_str, fem)
    fem.elements.build_sets()
    part._materials = get_materials(bulk_str, part)
    fem.sets = part.fem.sets + get_sets(bulk_str, fem)
    fem.sections = get_sections(bulk_str, fem)
    # part.fem._masses = get_mass(bulk_str, part.fem)
    fem.constraints += get_constraints(bulk_str, fem)
    fem._springs = get_springs(bulk_str, fem)
    fem.bcs += get_bcs(bulk_str, fem)

    print(8 * "-" + f'Imported "{fem.instance_name}"')
    return part


class SesamReader:

    """
    :param assembly: Assembly object
    :type assembly: ada.Assembly
    """

    def __init__(self, assembly: Assembly, part_name="T1"):
        self.assembly = assembly
        self.part = Part(part_name)
        assembly.add_part(self.part)


def sesam_eltype_2_general(eltyp):
    """
    Converts the numeric definition of elements in Sesam to a generalized element type form (ie. B31, S4, etc..)

    :param eltyp:
    :return: Generic element description
    """
    for ses, gen in sesam_el_map.items():
        if str_to_int(eltyp) == ses:
            return gen

    raise Exception("Currently unsupported eltype", eltyp)


def eltype_2_sesam(eltyp):
    for ses, gen in sesam_el_map.items():
        if eltyp == gen:
            return ses

    raise Exception("Currently unsupported eltype", eltyp)


def get_nodes(bulk_str, parent) -> Nodes:
    """
    Imports

    :param bulk_str:
    :param parent:
    :return: SortedNodes object
    :rtype: ada.core.containers.SortedNodes
    Format of input:

    GNODE     1.00000000E+00  1.00000000E+00  6.00000000E+00  1.23456000E+05
    GCOORD    1.00000000E+00  2.03000000E+02  7.05000000E+01  5.54650024E+02

    """

    def get_node(m):
        d = m.groupdict()
        return Node(
            [float(d["x"]), float(d["y"]), float(d["z"])],
            int(float(d["id"])),
            parent=parent,
        )

    return Nodes(list(map(get_node, cards.re_gcoord_in.finditer(bulk_str))), parent=parent)


def get_elements(bulk_str, fem) -> FemElements:
    """
    Import elements from Sesam Bulk str


    :param bulk_str:
    :param fem:
    :type fem: ada.fem.FEM
    :return: FemElementsCollections
    :rtype: ada.fem.containers.FemElements
    """

    def grab_elements(match):
        d = match.groupdict()
        nodes = [
            fem.nodes.from_id(x)
            for x in filter(
                lambda x: x != 0,
                map(str_to_int, d["nids"].replace("\n", "").split()),
            )
        ]
        eltyp = d["eltyp"]
        el_type = sesam_eltype_2_general(eltyp)
        metadata = dict(eltyad=str_to_int(d["eltyad"]), eltyp=eltyp)
        return Elem(
            str_to_int(d["elno"]),
            nodes,
            el_type,
            None,
            parent=fem,
            metadata=metadata,
        )

    return FemElements(list(map(grab_elements, cards.re_gelmnt.finditer(bulk_str))), fem_obj=fem)


def get_materials(bulk_str, part) -> Materials:
    """
    Interpret Material bulk string to FEM objects


    TDMATER: Material Element
    MISOSEL: linear elastic,isotropic

    TDMATER   4.00000000E+00  4.50000000E+01  1.07000000E+02  0.00000000E+00
            softMat

    MISOSEL   1.00000000E+00  2.10000003E+11  3.00000012E-01  1.15515586E+04
              1.14999998E+00  1.20000004E-05  1.00000000E+00  3.55000000E+08

    :return:
    """

    def grab_name(m):
        d = m.groupdict()
        return str_to_int(d["geo_no"]), d["name"]

    mat_names = {matid: mat_name for matid, mat_name in map(grab_name, cards.re_matnames.finditer(bulk_str))}

    def get_morsmel(m) -> Material:
        """
        MORSMEL

        Anisotropy, Linear Elastic Structural Analysis, 2-D Membrane Elements and 2-D Thin Shell Elements

        :param m:
        :return:
        """

        d = m.groupdict()
        matno = str_to_int(d["matno"])
        return Material(
            name=mat_names[matno],
            mat_id=matno,
            mat_model=CarbonSteel(
                rho=roundoff(d["rho"]),
                E=roundoff(d["d11"]),
                v=roundoff(d["ps1"]),
                alpha=roundoff(d["alpha1"]),
                zeta=roundoff(d["damp1"]),
                sig_p=[],
                eps_p=[],
                sig_y=5e6,
            ),
            metadata=d,
            parent=part,
        )

    def get_mat(match) -> Material:
        d = match.groupdict()
        matno = str_to_int(d["matno"])
        return Material(
            name=mat_names[matno],
            mat_id=matno,
            mat_model=CarbonSteel(
                rho=roundoff(d["rho"]),
                E=roundoff(d["young"]),
                v=roundoff(d["poiss"]),
                alpha=roundoff(d["damp"]),
                zeta=roundoff(d["alpha"]),
                sig_p=[],
                eps_p=[],
                sig_y=roundoff(d["yield"]),
            ),
            parent=part,
        )

    return Materials(
        chain(map(get_mat, cards.re_misosel.finditer(bulk_str)), map(get_morsmel, cards.re_morsmel.finditer(bulk_str))),
        parent=part,
    )


def get_sections(bulk_str, fem: FEM) -> FemSections:
    """

    General beam:
    GBEAMG    2.77000000E+02  0.00000000E+00  1.37400001E-01  6.93661906E-03
          1.07438751E-02  3.47881648E-03  0.00000000E+00  1.04544004E-02
          3.06967851E-02  1.39152659E-02  2.50000004E-02  2.08000001E-02
          0.00000000E+00  0.00000000E+00  6.04125019E-03  4.07929998E-03

    I-beam
    GIORH     1.00000000E+00  3.00000012E-01  7.10000005E-03  1.50000006E-01
          1.07000005E-02  1.50000006E-01  1.07000005E-02  1.00000000E+00
          1.00000000E+00

    GIORH (I-section description - if element type beam)
    GUSYI (unsymm.I-section)
    GCHAN  (Channel section)
    GBOX (Box section)
    GPIPE (Pipe section)
    GBARM (Massive bar)
    GTONP (T on plate)
    GDOBO (Double box)
    GLSEC (L section)
    GIORHR
    GCHANR
    GLSECR
    """
    # Get section names
    def get_section_names(m):
        d = m.groupdict()
        return str_to_int(d["geono"]), d["set_name"].strip()

    sect_names = {sec_id: name for sec_id, name in map(get_section_names, cards.re_sectnames.finditer(bulk_str))}

    # Get local coordinate systems

    def get_lcsys(m):
        d = m.groupdict()
        return str_to_int(d["transno"]), (
            roundoff(d["unix"]),
            roundoff(d["uniy"]),
            roundoff(d["uniz"]),
        )

    lcsysd = {transno: vec for transno, vec in map(get_lcsys, cards.re_lcsys.finditer(bulk_str))}

    # I-beam
    def get_IBeams(match) -> Section:
        d = match.groupdict()
        sec_id = str_to_int(d["geono"])
        return Section(
            name=sect_names[sec_id],
            sec_id=sec_id,
            sec_type="IG",
            h=roundoff(d["hz"]),
            t_w=roundoff(d["ty"]),
            w_top=roundoff(d["bt"]),
            w_btn=roundoff(d["bb"]),
            t_ftop=roundoff(d["tt"]),
            t_fbtn=roundoff(d["tb"]),
            genprops=GeneralProperties(sfy=float(d["sfy"]), sfz=float(d["sfz"])),
            parent=fem.parent,
        )

    # Box-beam
    def get_BoxBeams(match) -> Section:
        d = match.groupdict()
        sec_id = str_to_int(d["geono"])
        return Section(
            name=sect_names[sec_id],
            sec_id=sec_id,
            sec_type="BG",
            h=roundoff(d["hz"]),
            w_top=roundoff(d["by"]),
            w_btn=roundoff(d["by"]),
            t_w=roundoff(d["ty"]),
            t_ftop=roundoff(d["tt"]),
            t_fbtn=roundoff(d["tb"]),
            genprops=GeneralProperties(sfy=float(d["sfy"]), sfz=float(d["sfz"])),
            parent=fem.parent,
        )

    # General-beam
    def get_GenBeams(match) -> Section:
        d = match.groupdict()
        sec_id = str_to_int(d["geono"])
        gen_props = GeneralProperties(
            ax=roundoff(d["area"]),
            ix=roundoff(d["ix"]),
            iy=roundoff(d["iy"]),
            iz=roundoff(d["iz"]),
            iyz=roundoff(d["iyz"]),
            wxmin=roundoff(d["wxmin"]),
            wymin=roundoff(d["wymin"]),
            wzmin=roundoff(d["wzmin"]),
            shary=roundoff(d["shary"]),
            sharz=roundoff(d["sharz"]),
            scheny=roundoff(d["shceny"]),
            schenz=roundoff(d["shcenz"]),
            sy=float(d["sy"]),
            sz=float(d["sz"]),
        )
        if sec_id in fem.parent.sections.idmap.keys():
            sec = fem.parent.sections.get_by_id(sec_id)
            sec._genprops = gen_props
            gen_props.parent = sec
        else:
            sec = Section(name=f"GB{sec_id}", sec_id=sec_id, sec_type="GENBEAM", genprops=gen_props, parent=fem.parent)
            gen_props.parent = sec
            fem.parent.sections.add(sec)

    # Tubular-beam
    def get_gpipe(match) -> Section:
        d = match.groupdict()
        sec_id = str_to_int(d["geono"])
        if sec_id not in sect_names:
            sec_name = f"TUB{sec_id}"
        else:
            sec_name = sect_names[sec_id]
        t = d["t"] if d["t"] is not None else (d["dy"] - d["di"]) / 2
        return Section(
            name=sec_name,
            sec_id=sec_id,
            sec_type="TUB",
            r=roundoff(float(d["dy"]) / 2),
            wt=roundoff(t),
            genprops=GeneralProperties(sfy=float(d["sfy"]), sfz=float(d["sfz"])),
            parent=fem.parent,
        )

    def get_thicknesses(match):
        d = match.groupdict()
        sec_id = str_to_int(d["geono"])
        t = d["th"]
        return sec_id, t

    def get_hinges(match):
        d = match.groupdict()
        fixno = str_to_int(d["fixno"])
        opt = str_to_int(d["opt"])
        trano = str_to_int(d["trano"])
        a1 = str_to_int(d["a1"])
        a2 = str_to_int(d["a2"])
        a3 = str_to_int(d["a3"])
        a4 = str_to_int(d["a4"])
        a5 = str_to_int(d["a5"])
        try:
            a6 = str_to_int(d["a6"])
        except BaseException as e:
            logging.debug(e)
            a6 = 0
            pass
        return fixno, (opt, trano, a1, a2, a3, a4, a5, a6)

    def get_eccentricities(match):
        d = match.groupdict()
        eccno = str_to_int(d["eccno"])
        ex = float(d["ex"])
        ey = float(d["ey"])
        ez = float(d["ez"])
        return eccno, (ex, ey, ez)

    hinges_global = {fixno: values for fixno, values in map(get_hinges, cards.re_belfix.finditer(bulk_str))}
    thicknesses = {geono: t for geono, t in map(get_thicknesses, cards.re_thick.finditer(bulk_str))}
    eccentricities = {eccno: values for eccno, values in map(get_eccentricities, cards.re_geccen.finditer(bulk_str))}

    list_of_sections = chain(
        map(get_IBeams, cards.re_giorh.finditer(bulk_str)),
        map(get_BoxBeams, cards.re_gbox.finditer(bulk_str)),
        map(get_gpipe, cards.re_gpipe.finditer(bulk_str)),
    )

    fem.parent._sections = Sections(list_of_sections)
    list(map(get_GenBeams, cards.re_gbeamg.finditer(bulk_str)))

    importedgeom_counter = count(1)
    total_geo = count(1)

    def get_femsecs(match):
        d = match.groupdict()
        geono = str_to_int(d["geono"])
        next(total_geo)
        transno = str_to_int(d["transno"])
        elno = str_to_int(d["elno"])
        elem = fem.elements.from_id(elno)

        matno = str_to_int(d["matno"])

        # Go no further if element has no fem section
        if elem.type in ElemShapes.springs + ElemShapes.masses:
            next(importedgeom_counter)
            elem.metadata["matno"] = matno
            return None

        mat = fem.parent.materials.get_by_id(matno)
        if elem.type in ElemShapes.lines:
            next(importedgeom_counter)
            sec = fem.parent.sections.get_by_id(geono)
            n1, n2 = elem.nodes
            v = n2.p - n1.p
            if vector_length(v) == 0.0:
                xvec = [1, 0, 0]
            else:
                xvec = unit_vector(v)
            zvec = lcsysd[transno]
            crossed = np.cross(zvec, xvec)
            ma = max(abs(crossed))
            yvec = tuple([roundoff(x / ma, 3) for x in crossed])

            fix_data = str_to_int(d["fixno"])
            ecc_data = str_to_int(d["eccno"])

            members = None
            if d["members"] is not None:
                members = [str_to_int(x) for x in d["members"].replace("\n", " ").split()]

            hinges = None
            if fix_data == -1:
                hinges = get_hinges_from_elem(elem, members, hinges_global, lcsysd, xvec, zvec, yvec)

            offset = None
            if ecc_data == -1:
                offset = get_ecc_from_elem(elem, members, eccentricities, fix_data)

            fem_set = FemSet(sec.name, [elem], "elset", metadata=dict(internal=True), parent=fem)
            fem.sets.add(fem_set, append_suffix_on_exist=True)
            fem_sec = FemSection(
                name=sec.name,
                sec_type=ElemType.LINE,
                elset=fem_set,
                section=sec,
                local_z=zvec,
                local_y=yvec,
                material=mat,
                offset=offset,
                hinges=hinges,
                parent=fem,
            )
            return fem_sec

        elif elem.type in ElemShapes.shell:
            next(importedgeom_counter)
            sec_name = f"sh{elno}"
            fem_set = FemSet(sec_name, [elem], "elset", parent=fem, metadata=dict(internal=True))
            fem.sets.add(fem_set)
            fem_sec = FemSection(
                name=sec_name,
                sec_type=ElemType.SHELL,
                thickness=roundoff(thicknesses[geono]),
                elset=fem_set,
                material=mat,
                parent=fem,
            )
            return fem_sec
        else:
            raise ValueError("Section not added to conversion")

    sections = filter(lambda x: x is not None, map(get_femsecs, cards.re_gelref1.finditer(bulk_str)))
    fem_sections = FemSections(sections, fem_obj=fem)
    print(f"Successfully imported {next(importedgeom_counter) - 1} FEM sections out of {next(total_geo) - 1}")
    return fem_sections


def get_sets(bulk_str, parent):
    from itertools import groupby
    from operator import itemgetter

    from ada.fem import FemSet
    from ada.fem.containers import FemSets

    def get_setmap(m):
        d = m.groupdict()
        set_type = "nset" if str_to_int(d["istype"]) == 1 else "elset"
        if set_type == "nset":
            members = [parent.nodes.from_id(str_to_int(x)) for x in d["members"].split()]
        else:
            members = [parent.elements.from_id(str_to_int(x)) for x in d["members"].split()]
        return str_to_int(d["isref"]), set_type, members

    set_map = dict()
    for setid_el_type, content in groupby(map(get_setmap, cards.re_setmembs.finditer(bulk_str)), key=itemgetter(0, 1)):
        setid = setid_el_type[0]
        eltype = setid_el_type[1]
        set_map[setid] = [list(), eltype]
        for c in content:
            set_map[setid][0] += c[2]

    def get_femsets(m):
        nonlocal set_map
        d = m.groupdict()
        isref = str_to_int(d["isref"])
        fem_set = FemSet(
            d["set_name"].strip(),
            set_map[isref][0],
            set_map[isref][1],
            parent=parent,
        )
        return fem_set

    return FemSets(list(map(get_femsets, cards.re_setnames.finditer(bulk_str))), fem_obj=parent)


def get_hinges_from_elem(elem, members, hinges_global, lcsysd, xvec, zvec, yvec):
    """

    :param elem:
    :param members:
    :param hinges_global:
    :type elem: ada.Elem
    :return:
    """
    if len(elem.nodes) > 2:
        raise ValueError("This algorithm was not designed for more than 2 noded elements")
    from ada.core.utils import unit_vector

    hinges = []
    for i, x in enumerate(members):
        if i >= len(elem.nodes):
            break
        if x == 0:
            continue
        if x not in hinges_global.keys():
            raise ValueError("fixno not found!")
        opt, trano, a1, a2, a3, a4, a5, a6 = hinges_global[x]
        n = elem.nodes[i]
        if trano > 0:
            csys = None
        else:
            csys = Csys(
                f"el{elem.id}_hinge{i + 1}_csys",
                coords=([unit_vector(xvec) + n.p, unit_vector(yvec) + n.p, n.p]),
                parent=elem.parent,
            )
        dofs_origin = [1, 2, 3, 4, 5, 6]
        d = [int(x) for x, i in zip(dofs_origin, (a1, a2, a3, a4, a5, a6)) if int(i) != 0]

        hinges.append((n, d, csys))
    return hinges


def get_ecc_from_elem(elem, members, eccentricities, fix_data):
    """

    :param elem:
    :param members:
    :param eccentricities:
    :param fix_data:
    :type elem: ada.fem.Elem
    """
    # To the interpretation here
    start = 0 if fix_data != -1 else len(elem.nodes)
    end = len(elem.nodes) if fix_data != -1 else 2 * len(elem.nodes)
    eccen = []
    for i, x in enumerate(members[start:]):
        if i >= end:
            break
        if x == 0:
            continue
        n_offset = elem.nodes[i]
        ecc = eccentricities[x]
        eccen.append((n_offset, ecc))
    return eccen


def get_mass(bulk_str, fem):
    """

    :param bulk_str:
    :param fem:
    :type fem: ada.fem.FEM
    :return:
    """

    def checkEqual2(iterator):
        return len(set(iterator)) <= 1

    def grab_mass(match):
        d = match.groupdict()

        nodeno = str_to_int(d["nodeno"])
        mass_in = [
            roundoff(d["m1"]),
            roundoff(d["m2"]),
            roundoff(d["m3"]),
            roundoff(d["m4"]),
            roundoff(d["m5"]),
            roundoff(d["m6"]),
        ]
        masses = [m for m in mass_in if m != 0.0]
        if checkEqual2(masses):
            mass_type = None
            masses = [masses[0]] if len(masses) > 0 else [0.0]
        else:
            mass_type = "anisotropic"
        no = fem.nodes.from_id(nodeno)
        fem_set = FemSet(f"m{nodeno}", [], "elset", metadata=dict(internal=True), parent=fem)
        mass = Mass(f"m{nodeno}", fem_set, masses, "mass", ptype=mass_type, parent=fem)
        elem = Elem(no.id, [no], "mass", fem_set, mass_props=mass, parent=fem)
        fem.elements.add(elem)
        fem_set.add_members([elem])
        fem.sets.add(fem_set)
        return Mass(f"m{nodeno}", fem_set, masses, "mass", ptype=mass_type, parent=fem)

    return {m.name: m for m in map(grab_mass, cards.re_bnmass.finditer(bulk_str))}


def get_constraints(bulk_str, fem: FEM) -> List[Constraint]:
    def grab_constraint(master, data):
        m = str_to_int(master)
        m_set = FemSet(f"co{m}_m", [fem.nodes.from_id(m)], "nset")
        slaves = []
        for d in data:
            s = str_to_int(d["slave"])
            slaves.append(fem.nodes.from_id(s))
        s_set = FemSet(f"co{m}_m", slaves, "nset")
        fem.add_set(m_set)
        fem.add_set(s_set)
        return Constraint(f"co{m}", "coupling", m_set, s_set, parent=fem)

    con_map = [m.groupdict() for m in cards.re_bldep.finditer(bulk_str)]
    con_map.sort(key=lambda x: x["master"])
    from itertools import groupby

    return [grab_constraint(m, d) for m, d in groupby(con_map, key=lambda x: x["master"])]


def get_springs(bulk_str, fem: FEM):
    gr_spr_elements = None
    for eltype, elements in fem.elements.group_by_type():
        if eltype == "SPRING1":
            gr_spr_elements = {el.metadata["matno"]: el for el in elements}

    def grab_grspring(m):
        nonlocal gr_spr_elements
        d = m.groupdict()
        matno = str_to_int(d["matno"])
        ndof = str_to_int(d["ndof"])
        bulk = d["bulk"].replace("\n", "").split()
        el = gr_spr_elements[matno]
        spr_name = f"spr{el.id}"

        n1 = el.nodes[0]
        a = 1
        row = 0
        spring = []
        subspring = []
        for dof in bulk:
            subspring.append(float(dof.strip()))
            a += 1
            if a > ndof - row:
                spring.append(subspring)
                subspring = []
                a = 1
                row += 1
        new_s = []
        for row in spring:
            l = abs(len(row) - 6)
            if l > 0:
                new_s.append([0.0 for i in range(0, l)] + row)
            else:
                new_s.append(row)
        X = np.array(new_s)
        X = X + X.T - np.diag(np.diag(X))
        return Spring(spr_name, matno, "SPRING1", n1=n1, stiff=X, parent=fem)

    return {c.name: c for c in map(grab_grspring, cards.re_mgsprng.finditer(bulk_str))}


def get_bcs(bulk_str, fem: FEM) -> List[Bc]:
    def grab_bc(match) -> Bc:
        d = match.groupdict()
        node = fem.nodes.from_id(str_to_int(d["nodeno"]))
        assert isinstance(node, Node)

        fem_set = FemSet(f"bc{node.id}_set", [node], "nset")
        fem.sets.add(fem_set)
        dofs = []
        for i, c in enumerate(d["content"].replace("\n", "").split()):
            bc_sestype = str_to_int(c.strip())
            if bc_sestype in [0, 4]:
                continue
            dofs.append(i + 1)
        bc = Bc(f"bc{node.id}", fem_set, dofs, parent=fem)
        node.bc = bc

        return bc

    return list(map(grab_bc, cards.re_bnbcd.finditer(bulk_str)))
