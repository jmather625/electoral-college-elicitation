from typing import Tuple
import numpy as np
import pickle

from common import VoterData, Oracle
from solver import F_ERROR, Fairness, MAX_F, MIN_F, option2_find_f, option1_find_f


CONVERGE_F = 2e-1

# each house rep represents 1e6 people
HOUSE_REP_TO_POP = 1e6


f = open(f'o1_ns=50_rand.pkl', 'rb')
BOUNDS_UPPER_O1 = pickle.load(f)
f.close()


f = open(f'o2_ns=50_rand.pkl', 'rb')
BOUNDS_UPPER_O2 = pickle.load(f)
f.close()


class ElectoralElicitation:
    def __init__(self, ns: int):
        assert ns >= 2 and ns % 2 == 0
        self.ns = ns
        self.option_elicit = None # Option2Elicit or Option1Elicit
        self.conflicting_trial = None
        self.opt_hat = None
    

    def generate_trial(self) -> VoterData:
        if self.option_elicit is None:
            # generate a trial to choose option_elict
            vd, o1_wins = self.generate_o2_o1_conflicting_trial()
            self.conflicting_trial = {
                "expected_o1": o1_wins
            }
            return vd
        return self.option_elicit.generate_trial()
    

    def process_trial(self, vd: VoterData, dwins: bool) -> F_ERROR:
        if self.conflicting_trial is not None:
            if dwins == self.conflicting_trial["expected_o1"]:
                # option 1 is chosen
                self.opt_hat = 1
                self.option_elicit = Option1Elicit(self.ns)
            else:
                # option 2 is chosen
                self.opt_hat = 2
                self.option_elicit = Option2Elicit(self.ns)
            self.conflicting_trial = None
            return F_ERROR.none

        return self.option_elicit.process_trial(vd, dwins)


    def converged(self) -> bool:
        if self.option_elicit is None:
            return False
        return self.option_elicit.converged


    def predict_opt(self) -> int:
        return self.opt_hat


    def predict_f(self) -> float:
        return self.option_elicit.predict_f()


    def clear(self):
        self.option_elicit = None
        self.conflicting_trial = None    

        
    def generate_o2_o1_conflicting_trial(self) -> Tuple[VoterData, bool]:
        stop = []
        stoh = []
        stodv = []
        for i in range(self.ns - 2):
            dv = None
            hs = 10
            if i % 2 == 0:
                dv = 0.52
            else:
                dv = 0.48
            stodv.append(dv)
            stoh.append(hs)
            stop.append(hs * HOUSE_REP_TO_POP)
        
        # if 1, then we will make it so o1 always goes D and o2 always goes R for any fairness
        # if 0, vice-versa
        o1_dwins = np.random.randint(0, 2) == 1
        hs1 = None
        dv1 = None
        hs2 = None
        dv2 = None
        if o1_dwins:
            hs1 = 20
            dv1 = 0.51
            hs2 = 7
            dv2 = 0.45
        else:
            hs1 = 20
            dv1 = 0.49
            hs2 = 7
            dv2 = 0.55
        stodv.append(dv1)
        stodv.append(dv2)
        stoh.append(hs1)
        stoh.append(hs2)
        stop.append(hs1 * HOUSE_REP_TO_POP)
        stop.append(hs2 * HOUSE_REP_TO_POP)
        return VoterData(self.ns, stop, stoh, stodv), o1_dwins


class Option2Elicit:
    def __init__(self, ns: int):
        assert ns >= 2
        # f = open(f'o2_ns={ns}_rand.pkl', 'rb')
        # self.bounds_upper = pickle.load(f)
        # f.close()
        self.bounds_upper = BOUNDS_UPPER_O2
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


class Option1Elicit:
    def __init__(self, ns: int):
        assert ns >= 2
        # f = open(f'o1_ns={ns}_rand.pkl', 'rb')
        # self.bounds_upper = pickle.load(f)
        # f.close()
        self.bounds_upper = BOUNDS_UPPER_O1
        self.ns = ns
        self.fairness = Fairness(MAX_F, MIN_F)
        self.converged = False


    def generate_trial(self) -> VoterData:
        search = (self.fairness.f_hi + self.fairness.f_lo) / 2
        cutoff, vd = self.bounds_upper.ceiling_item(search)
        if not (self.fairness.f_lo < cutoff < self.fairness.f_hi):
            raise ValueError()
        return vd # we can ignore cutoff, it will be something close to search

    
    def process_trial(self, vd: VoterData, dwins: bool) -> F_ERROR:
        f, f_err = option1_find_f(vd, dwins)
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
