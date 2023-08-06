import logging
import traceback
from itertools import chain
from typing import List

from ada.concepts.levels import Part

from ..concepts.points import Node
from ..concepts.structural import Beam
from .utils import intersect_calc, is_parallel, vector_length


def basic_intersect(bm: Beam, margins, all_parts: [Part]):
    if bm.section.type == "gensec":
        return bm, []
    try:
        vol = bm.bbox
    except ValueError as e:
        logging.error(f"Intersect bbox skipped: {e}\n{traceback.format_exc()}")
        return None
    vol_in = [x for x in zip(vol[0], vol[1])]
    beams = filter(
        lambda x: x != bm,
        chain.from_iterable([p.beams.get_beams_within_volume(vol_in, margins=margins) for p in all_parts]),
    )
    return bm, beams


def beam_cross_check(bm1: Beam, bm2: Beam, outofplane_tol=0.1):
    """Calculate intersection of beams and return point, s, t"""
    p_check = is_parallel
    i_check = intersect_calc
    v_len = vector_length
    a = bm1.n1.p
    b = bm1.n2.p
    c = bm2.n1.p
    d = bm2.n2.p

    ab = b - a
    cd = d - c

    s, t = i_check(a, c, ab, cd)

    ab_ = a + s * ab
    cd_ = c + t * cd

    if p_check(ab, cd):
        logging.debug(f"beams {bm1} {bm2} are parallel")
        return None

    if v_len(ab_ - cd_) > outofplane_tol:
        logging.debug("The two lines do not intersect within given tolerances")
        return None

    return ab_, s, t


def are_beams_connected(bm1: Beam, beams: List[Beam], out_of_plane_tol, point_tol, nodes, nmap) -> None:
    for bm2 in beams:
        if bm1 == bm2:
            continue
        res = beam_cross_check(bm1, bm2, out_of_plane_tol)
        if res is None:
            continue
        point, s, t = res
        t_len = (abs(t) - 1) * bm2.length
        s_len = (abs(s) - 1) * bm1.length
        if t_len > bm2.length / 2 or s_len > bm1.length / 2:
            continue
        if point is not None:
            new_node = Node(point)
            n = nodes.add(new_node, point_tol=point_tol)
            if n not in nmap.keys():
                nmap[n] = [bm1]
            if bm1 not in nmap[n]:
                nmap[n].append(bm1)
            if bm2 not in nmap[n]:
                nmap[n].append(bm2)
