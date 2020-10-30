from typing import Tuple
from dataclasses import dataclass
from enum import Enum

from common import VoterData


MAX_F = 4.0
MIN_F = 0.0


@dataclass
class Fairness:
    # upper bound
    f_hi: float
    # lower bound
    f_lo: float


class F_ERROR(Enum):
    none = 0
    bad_dwin = 1
    bad_rwin = 2
    large_f_lo = 3


def option2_find_f(vd: VoterData, dwins: bool) -> Tuple[Fairness, F_ERROR]:
    '''
    Computes a lower and upper bound on f given voter data `vd` and a boolean `dwins`
    indicating whether democrats won
    '''
    lhs = 0
    rhs = 0
    for s in range(vd.ns):
        lhs += vd.stodv[s] - 0.5
        rhs += (vd.stodv[s] - 0.5) * vd.stoh[s]

    rhs *= -1
    f_err = check_inconsistencies(lhs, rhs, dwins)
    if f_err != F_ERROR.none:
        return Fairness(MAX_F, MIN_F), f_err
    if lhs > 0:
        if dwins:
            f_lo = max(rhs / lhs, MIN_F)
            if f_lo > MAX_F:
                # this requires a fairness beyond the capacities possible
                return Fairness(MAX_F, MIN_F), F_ERROR.large_f_lo
            return Fairness(MAX_F, f_lo), F_ERROR.none
        else:
            f_hi = min(rhs / lhs, MAX_F)
            return Fairness(f_hi, MIN_F), F_ERROR.none
    else:
        if dwins:
            f_hi = min(rhs / lhs, MAX_F)
            return Fairness(f_hi, MIN_F), F_ERROR.none
        else:
            f_lo = max(rhs / lhs, MIN_F)
            if f_lo > MAX_F:
                # this requires a fairness beyond the capacities possible
                return Fairness(MAX_F, MIN_F), F_ERROR.large_f_lo
            return Fairness(MAX_F, f_lo), F_ERROR.none


def check_inconsistencies(lhs: float, rhs: float, dwins: bool) -> F_ERROR:
    '''
    Checks inconsistencies based on the outcome (`dwins`), `lhs`, and `rhs` of option 2 equation.
    These should never happen and are logical inconsistencies.
    '''
    if dwins and lhs < 0 and rhs > 0:
        return F_ERROR.bad_dwin
    elif not dwins and lhs > 0 and rhs < 0:
        return F_ERROR.bad_rwin
    return F_ERROR.none
    
