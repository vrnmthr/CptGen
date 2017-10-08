import numpy as np
import utils as u

class SpeciesCpt:
    __metaclass__ = ABCMeta

    @abstractmethod
    def score():
        pass

    @abstractmethod
    def next_move():
        pass

class FirstSpecies(SpeciesCpt):

    def __init__(self, cf):
        self.cf = cf
        self.cpt = [None for i in cf]
        
    def next_move():
        pass
    
    @staticmethod
    def score(self):
        l = len(self.cpt)
        #calculates how often a given interval is selected in cpt
        check_intrvls = [u.is_third, u.is_fifth, u.is_sixth, u.is_octave]
        intrvls = [sum(1 for x in range(l) if f(self.cpt[l][0], self.cf[l][0])) for f in check_intrvls]
        itvl_sigma = np.var(intrvls)
        #calculates how close the ratio of perfect consonances is to ideal
        ideal_p_ratio = 3/8
        p_ratio_err = (ideal_p_ratio - (intrvls[1] + intrvls[3])/l) ** 2
        #calculates how often a note is selected in cpt
        c = Counter([note[0] for note in self.cpt])
        note_sigma = np.var(c.elements())
        #calculates how close the ratio of leaps is to ideal
        ideal_leaps = 3/8
        num_leaps = sum(1 for x in range(l - 1) if not u.is_second(self.cpt[x][0], self.cpt[x+1][0]))
        leaps_err = (ideal_leaps - num_leaps/l) ** 2
        #scores the shape
        climax_freq = c[max(self.cpt)]
        d_changes = sum(1 for x in range(l-2) if (self.cpt[x][0] - self.cpt[x+1][0])*(self.cpt[x+1][0] - self.cpt[x+2][0]) < 0)
        ideal_d = 3/8
        d_changes_err = (ideal_d - d_changes) ** 2
        total = itvl_sigma + note_sigma + p_ratio_err + d_changes_err + leaps_err
        return total
