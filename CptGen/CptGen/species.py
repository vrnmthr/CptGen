import numpy as np
import utils as u
from collections import Counter
import abc


class SpeciesCpt:
    __metaclass__  = abc.ABCMeta

    @staticmethod
    @abc.abstractmethod
    def score(cf, cpt):
        """Score a given counterpoint"""
        pass

    @staticmethod
    @abc.abstractmethod
    def generate_cf(string):
        """Given a cf as string, returns cf representation"""
        pass
    
    @staticmethod
    @abc.abstractmethod
    def next_move(cf, prev, mode):
        """
        Given a cf representing the rest of the cantus firmus
        that requires cpt to be written and cpt representing 
        cpt that has already been generated, outputs a list 
        of valid integer moves
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def cpt_to_string(cpt):
        """Converts a representation of cpt into a readable string"""
        pass
    

class FirstSpecies(SpeciesCpt):

    def __init__():
        pass
        
    @staticmethod
    def score(cf, cpt):
        """Score a given counterpoint"""
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
        climax_err = float((1 - climax_freq) ** 2)/l
        d_changes = sum(1 for x in range(l-2) if (cpt[x][0] - cpt[x+1][0])*(cpt[x+1][0] - cpt[x+2][0]) < 0)
        ideal_d = float(3)/8
        d_changes_err = (ideal_d - (float(d_changes)/l)) ** 2
        total = itvl_sigma + note_sigma + p_ratio_err + d_changes_err + leaps_err + climax_err
        return total

    @staticmethod
    def generate_cf(cf):
        """
        Generates representation of cf inputted as string
        """
        return [u.note_to_int(note) for note in cf.split()]  
    
    @staticmethod
    def next_move(cf, prev, mode):
        '''
        Given a cantus firmus and the previous counterpoint written
        generates a list of potential next notes. 
        Rules followed:
        1. Only 3rds, 5th, 6th, 8th allowed
        2. No repeating same note
        3. Must recover all leaps
        4. No perfect intervals in a row
        5. No perfect intervals in similar motion
        6. Must end on unison
        '''
        note = cf[0]
        #maximum range between voices is two octaves
        #options contains tuple where first value is note, second value is interval
        options = [(note + i + 12*j, i + 12*j) for j in range(2) for i in u.consonances]
        filtered = []
        for option in options:
            in_mode = option[0] % 12 in mode
            #only checks if note is in mode if it is first note
            if not prev:
                if in_mode:
                    filtered.append(option)
                continue
            prev_h = prev[-1]
            ends_unison = not(len(cf) == 1 and option[1] % 12 > 0)
            penultimate_seventh = not(len(cf) == 2 and u.scale_degree(option[0], mode) != 7)
            recover_leap = True
            melodic_leap = u.is_melodic_leap(prev_h[0], option[0])
            #signed interval between option and previous harmony
            intrvl = prev_h[0] - option[0]
            if len(prev) > 1:
                #signed interval between previous harmony and double previous harmony
                prev_intrvl = prev[-2][0] - prev_h[0]
                recover_leap = not(len(prev) > 1 and abs(prev_intrvl) > 4 
							       and (prev_intrvl*intrvl > 0 or abs(intrvl) > 2))
            perfect_row = not (u.is_perfect(prev_h[1]) 
						       and prev_h[1] == option[1])
            not_same_note = not option[0] == prev_h[0]
            no_p_ints_similar = not (u.is_perfect(option[1]) and intrvl*(prev_h[0] - prev_h[1] - note) > 0)
            if in_mode and ends_unison and penultimate_seventh and melodic_leap and recover_leap \
                and perfect_row and not_same_note and no_p_ints_similar:
                filtered.append(option)
        return filtered

    @staticmethod
    def cpt_to_string(cpt):
        """Converts a representation of cpt into a readable string"""
        return [u.int_to_note(h[0], True) for h in cpt]


class SecondSpecies(SpeciesCpt):
    
    def __init__():
        pass

    @staticmethod
    def cpt_to_string(cpt):
        '''cpt representation contains tuples of first note, 
        harmony'''
        return [u.int_to_note(h[0], True) for h in cpt]
    
    @staticmethod
    def generate_cf(string):
        '''cf representation contains list of notes, along with
        Boolean representing whether the accompanying note is strong
        beat'''
        result = []
        ints = [u.note_to_int(note) for note in string.split()]
        for i in range(len(ints)):
            val = ints[i]
            if i > len(ints) - 3:
                #is last element or second last element, only include once
                result.append((val, True))
            else:
                result.append((val, True))
                result.append((val, False))
        return result
            
    @staticmethod
    def next_move(cf, prev, mode):
        note = cf[0]
        #maximum range between voices is two octaves
        if note[1]:
            #note is strong beat
            options = [(note[0] + i + 12*j, i + 12*j) for j in range(2) for i in u.consonances]
        else:
            #note is weak beat - dissonances allowed
            options = [(note[0] + i, i) for i in range(1, 25)]
        
        filtered = []
        for option in options:
            in_mode = option[0] % 12 in mode
            #only checks if note is in mode if it is first note
            if not prev:
                if in_mode:
                    filtered.append(option)
                continue
            prev_h = prev[-1]
            ends_unison = not(len(cf) == 1 and option[1] % 12 > 0)
            penultimate_seventh = not(len(cf) == 2 and u.scale_degree(option[0], mode) != 7)
            recover_leap = True
            melodic_leap = u.is_melodic_leap(prev_h[0], option[0])
            #signed interval between option and previous harmony
            intrvl = prev_h[0] - option[0]
            if len(prev) > 1:
                #signed interval between previous harmony and double previous harmony
                prev_intrvl = prev[-2][0] - prev_h[0]
                recover_leap = not(len(prev) > 1 and abs(prev_intrvl) > 4 
							       and (prev_intrvl*intrvl > 0 or abs(intrvl) > 2))
            perfect_row = not (u.is_perfect(prev_h[1]) 
						       and prev_h[1] == option[1])
            not_same_note = not option[0] == prev_h[0]
            no_p_ints_similar = not (u.is_perfect(option[1]) and intrvl*(prev_h[0] - prev_h[1] - note[0]) > 0)
            start_diss_step = not(u.is_dissonant(option[1]) and not u.stepwise(prev_h[0], option[0]))
            end_diss_step = not(u.is_dissonant(prev_h[1]) and not(u.stepwise(prev_h[0], option[0])) \
                and u.change_direction(prev[-2][0], prev_h[0], option[0]))
            if in_mode and ends_unison and penultimate_seventh and melodic_leap and recover_leap \
                and perfect_row and not_same_note and no_p_ints_similar and start_diss_step and end_diss_step:
                filtered.append(option)
        return filtered

    @staticmethod
    def score(cf, cpt):
        """Score a given counterpoint"""
        """l = len(cpt)
        #calculates how often a given interval is selected in cpt
        check_intrvls = [u.is_third, u.is_fifth, u.is_sixth, u.is_octave]
        intrvls = [sum(1 for x in range(l) if f(cpt[x][0], cf[x][0])) for f in check_intrvls]
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
        climax_err = float((1 - climax_freq) ** 2)/l
        d_changes = sum(1 for x in range(l-2) if (cpt[x][0] - cpt[x+1][0])*(cpt[x+1][0] - cpt[x+2][0]) < 0)
        ideal_d = float(3)/8
        d_changes_err = (ideal_d - (float(d_changes)/l)) ** 2
        total = itvl_sigma + note_sigma + p_ratio_err + d_changes_err + leaps_err + climax_err
        return total"""
        return 0