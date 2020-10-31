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
        num = 0
        denom = 0
        for i in range(vd.ns):
            e_s = vd.stoh[i] + self.f
            if vd.stodv[i] > 0.5:
                num += e_s
            denom += e_s
        return num / denom > 0.5

    
    def should_dwin_o2(self, vd: VoterData) -> bool:
        num = 0
        denom = 0
        for i in range(vd.ns):
            e_s = vd.stoh[i] + self.f
            num += vd.stodv[i] * e_s
            denom += e_s
        return num / denom > 0.5


def get_random_dv() -> float:
    return np.random.uniform(0.35, 0.65)


def get_random_hs(normal: bool, frac: bool) -> int:
    if normal:
        v = np.random.normal(10, 8)
        while v < 1 or v > 53:
            v = np.random.normal(10, 8)
        if frac:
            return v
        else:
            return round(v)
    
    else:
        if frac:
            return np.random.uniform(1, 53)
        else:
            return np.random.randint(1, 53)

    
