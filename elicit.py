import numpy as np
import pickle

from common import VoterData
from solver import F_ERROR, Fairness, MAX_F, MIN_F, option2_find_f


CONVERGE_F = 1e-1

# each house rep represents 1e6 people
HOUSE_REP_TO_POP = 1e6


class Option2Elicit:
    def __init__(self, ns: int):
        assert ns >= 2
        f = open(f'ns={ns}_rand.pkl', 'rb')
        self.bounds_upper = pickle.load(f)
        f.close()
        self.ns = ns
        self.fairness = Fairness(MAX_F, MIN_F)
        self.converged = False


    def generate_trial(self) -> VoterData:
        search = (self.fairness.f_hi + self.fairness.f_lo) / 2
        cutoff, vd = self.bounds_upper.ceiling_item(search)
        return vd # we can ignore cutoff, it will be something close to search

    
    def process_trial(self, vd: VoterData, dwins: bool) -> F_ERROR:
        f, f_err = option2_find_f(vd, dwins)
        if f_err != F_ERROR.none:
            return f_err
        
        if f.f_hi < MAX_F:
            # this means f_hi was changed
            if f.f_hi > self.fairness.f_hi:
                raise Warning(f"current fairness high is {self.fairness.f_hi}, computed a higher cutoff of {f.f_hi}")
            else:
                self.fairness.f_hi = f.f_hi # narrow bound

        if f.f_lo > MIN_F:
            # this means f_lo was changed
            if f.f_lo < self.fairness.f_lo:
                raise Warning(f"current fairness low is {self.fairness.f_hi}, computed a lower cutoff of {f.f_lo}")
            else:
                self.fairness.f_lo = f.f_lo # narrow bound

        self.converged = (self.fairness.f_hi - self.fairness.f_lo) < CONVERGE_F
        return F_ERROR.none


    def predict_f(self) -> float:
        return (self.fairness.f_hi + self.fairness.f_lo) / 2


    def clear(self):
        self.fairness = Fairness(MAX_F, MIN_F)
        self.converged = False
