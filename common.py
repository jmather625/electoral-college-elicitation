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
    def __init__(self, option: int, fairness: float):
        assert option in [1, 2]
        self.option = option
        self.f = fairness


    def should_dwin(self, vd: VoterData) -> bool:
        if self.option == 1:
            return self.should_dwin_o1(vd)
        elif self.option == 2:
            return self.should_dwin_o2(vd)
        raise ValueError("bad option:", self.option)


    def should_dwin_o1(self, vd: VoterData) -> bool:
        lhs = 0
        rhs = 0
        for i in range(vd.ns):
            if vd.stodv[i] > 0.5:
                lhs += 1
                rhs += -vd.stoh[i]
            else:
                lhs -= 1
                rhs += vd.stoh[i]
        return self.f * lhs > rhs

    
    def should_dwin_o2(self, vd: VoterData) -> bool:
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

    
