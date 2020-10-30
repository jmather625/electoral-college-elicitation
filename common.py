from typing import List
from dataclasses import dataclass
import numpy as np


# each house rep represents 1e6 people
HOUSE_REP_TO_POP = 1e6


@dataclass
class VoterData:
    # number of states
    ns: int
    # state to population
    stop: List[int]
    # state to house reps
    stoh: List[int]
    # state to % democrat votes
    stodv: List[int]


class Oracle:
    def __init__(self, f: float):
        self.f = f


    def should_dwin(self, vd: VoterData) -> bool:
        lhs = 0
        rhs = 0
        for s in range(vd.ns):
            lhs += vd.stodv[s] - 0.5
            rhs += (vd.stodv[s] - 0.5) * vd.stoh[s]
        return self.f * lhs > -rhs


def get_random_dv() -> float:
    return np.random.uniform(0.35, 0.65)


def get_random_hs() -> int:
    return np.random.randint(1, 53)

    
