import utils as u
import species

def note_to_int(note):
    '''
	Converts string representation of note into int, octave specified by last integer. 
    '''
    if ("#" in note) and ("b" in note):
        raise ValueError("Note cannot be sharp and flat simultaneously")
    octave = int(note[-1]) 
    note_letter = note[0]
    if (octave > 8) or (octave < 1):
        raise ValueError("Octave out of range")
    if note_letter not in u.note_to_int:
        raise ValueError("Invalid note name")
    result = 12 * (octave - 1) + u.note_to_int[note_letter]
    if "#" in note:
        result += 1
    if "b" in note:
        result -= 1
    return result

def int_to_note(num, oct=False):
    octave = num // 12 + 1
    num = num % 12
    result = u.int_to_note[num]
    if oct:
        result += str(octave)
    return result

def cf_to_ints(cf):
    '''
    Converts space separated list of notes into list of integers
    '''
    return [note_to_int(note) for note in cf.split()]    

def cpt(cf, gf):
    '''
    Returns counterpoint for a given cf (list of ints), and a
    valid generation function. 
    '''
    def cpt_inner(cf, cpt, base=False):
        '''
        Calculates counterpoint from given note until 
        '''
        #cpt is list of tuples where first int represents cpt note
        #and second int represents interval between cpt and cf
        allowable = gf(cf, cpt, None)
        for option in allowable:
            if len(cf) == 1:
                return [option]
            rest_cpt = cpt_inner(cf[1:], cpt + [option])
            if rest_cpt:
                result = [option] + rest_cpt
                if base:
                    error = species.FirstSpecies.score(cf, result)
                    if error < threshold:
                        return result
                    else:
                        if vars['counter'] >= max_iterations:
                            return vars['sol'][0]
                        vars['sol'] = min(vars['sol'], (result, error), key=lambda i:i[1])
                        vars['counter'] += 1
                else:
                    return result
        return []
    
    vars = {'counter':0, 'sol': (None, float('inf'))}
    threshold = 0.1
    max_iterations = 1000
    return cpt_inner(cf, list(), True)

def first_species(cf, prev, mode):
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
        in_mode = u.in_mode(option[0], None)
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

def main():
    cf_in = "C4 D4 F4 E4 D4 E4 D4 C4"
    cf = cf_to_ints(cf_in)
    harmony = cpt(cf, first_species)
    score = species.FirstSpecies.score(cf, harmony)
    print cf_in
    print [int_to_note(h[0], True) for h in harmony]
    print score

if __name__ == '__main__':
    main()