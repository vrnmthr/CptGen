import utils

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
    if note_letter not in utils.note_to_int:
        raise ValueError("Invalid note name")
    result = 12 * (octave - 1) + utils.note_to_int[note_letter]
    if "#" in note:
        result += 1
    if "b" in note:
        result -= 1
    return result

def int_to_note(num, oct=False):
    octave = num // 12
    num = num % 12
    result = utils.int_to_note[num]
    if oct:
        result += octave
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
    def cpt_inner(cf, cpt):
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
                return [option] + rest_cpt
        return []
    
    return cpt_inner(cf, list())

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
    options = [(note + i + 12*j, i + 12*j) for j in range(2) for i in utils.consonances]
    filtered = []
    for option in options:
        in_mode = utils.in_mode(option[0], None)
        #only checks if note is in mode if it is first note
        if not prev:
            if in_mode:
                filtered.append(option)
            continue
        prev_h = prev[-1]
        ends_unison = not(len(cf) == 1 and option[1] % 12 > 0)
        ends_unison = not(len(cf) == 2 and utils.scale_degree(option[1], mode) != 2)
        recover_leap = True
        melodic_leap = utils.is_melodic_leap(prev_h[0], option[0])
        #signed interval between option and previous harmony
        intrvl = prev_h[0] - option[0]
        if len(prev) > 1:
            #signed interval between previous harmony and double previous harmony
            prev_intrvl = prev[-2][0] - prev_h[0]
            recover_leap = not(len(prev) > 1 and abs(prev_intrvl) > 4 
							   and (prev_intrvl*intrvl > 0 or abs(intrvl) > 2))
        perfect_row = not (utils.is_perfect(prev_h[1]) 
						   and prev_h[1] == option[1])
        not_same_note = not option[0] == prev_h[0]
        no_p_ints_similar = not (utils.is_perfect(option[1]) 
                        and intrvl*(prev_h[0] - prev_h[1] - note) < 0)
        if ends_unison and in_mode and melodic_leap and recover_leap and perfect_row and not_same_note and no_p_ints_similar:
            filtered.append(option)
    return filtered

def main():
    cf = cf_to_ints("C4 D4 F4 E4 D4 E4 D4 C4")
    print cpt(cf, first_species)

if __name__ == '__main__':
    main()