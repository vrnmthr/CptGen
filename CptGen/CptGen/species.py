import numpy as np
import utils as u
from collections import Counter

"""
class SpeciesCpt:
    __metaclass__ = ABCMeta()

    @abstractmethod
    def score():
        pass

    @abstractmethod
    def next_move():
        pass"""

class FirstSpecies():

    def __init__(self, cf):
        self.cf = cf
        self.cpt = [None for i in cf]
        
    def next_move():
        pass
    
    @staticmethod
    def score(cf, cpt):
        l = len(cpt)
        #calculates how often a given interval is selected in cpt
        check_intrvls = [u.is_third, u.is_fifth, u.is_sixth, u.is_octave]
        intrvls = [sum(1 for x in range(l) if f(cpt[x][0], cf[x])) for f in check_intrvls]
        itvl_sigma = np.var(intrvls)/l
        #calculates how close the ratio of perfect consonances is to ideal
        ideal_p_ratio = float(3)/float(8)
        p_ratio_err = (ideal_p_ratio - float(intrvls[1] + intrvls[3])/l) ** 2
        #calculates how often a note is selected in cpt
        c = Counter([note[0] for note in cpt])
        note_sigma = np.var([c[note] for note in c])/l
        #calculates how close the ratio of leaps is to ideal
        ideal_leaps = float(3)/8
        num_leaps = sum(1 for x in range(l - 1) if not u.is_second(cpt[x][0], cpt[x+1][0]))
        leaps_err = (ideal_leaps - float(num_leaps)/l) ** 2
        #scores the shape
        climax_freq = c[max(cpt, key=lambda h:h[0])[0]]
        d_changes = sum(1 for x in range(l-2) if (cpt[x][0] - cpt[x+1][0])*(cpt[x+1][0] - cpt[x+2][0]) < 0)
        ideal_d = float(3)/8
        d_changes_err = (ideal_d - (float(d_changes)/l)) ** 2
        total = itvl_sigma + note_sigma + p_ratio_err + d_changes_err + leaps_err
        return total
