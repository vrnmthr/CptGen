import utils as u
import species

def cf_to_ints(cf):
    '''
    Converts space separated list of notes into list of integers
    '''
    return [u.note_to_int(note) for note in cf.split()]

def cpt_bds(cf, spcs):
    '''Runs breadth-first search from both ends of cpt, stores 
    notes reachable for each position in CPT and path taken to get there'''
    pass

def cpt(cf, spcs, mode):
    '''
    Returns counterpoint for a given cf (list of ints), and spcs,
    a class representation of SpeciesCpts, and a mode (tuple with 
    name and list of ints)
    '''
    def cpt_inner(cf, cpt, base=False):
        allowable = spcs.next_move(cf, cpt, mode)
        for option in allowable:
            if len(cf) == 1:
                return [option]
            rest_cpt = cpt_inner(cf[1:], cpt + [option])
            if rest_cpt:
                result = [option] + rest_cpt
                if base:
                    error = spcs.score(cf, result)
                    if error < threshold:
                        return spcs.cpt_to_string(result)
                    else:
                        if vars['counter'] >= max_iterations:
                            return spcs.cpt_to_string(['sol'][0])
                        vars['sol'] = min(vars['sol'], (result, error), key=lambda i:i[1])
                        vars['counter'] += 1
                else:
                    return result
        return []
    
    vars = {'counter':0, 'sol': (None, float('inf'))}
    threshold = 0.1
    max_iterations = 1000
    return cpt_inner(cf, list(), True)

def detect_mode(cf):
    '''Given a cantus firmus as a list of ints, attempts to detect the mode
    and returns a tuple containing a string for the name of the mode and ints
    representing the notes present in the mode, assuming that the first note provided
    is the tonic.'''
    modes = u.modes()
    tonic = cf[0]
    transposed = [(note - tonic) % 12 for note in cf]
    sums = [(sum(1 for note in transposed if note in modes[mode]), mode) for mode in modes]
    max_freq = max(sums, key = lambda i: i[0])[0]
    filtered = [i[1] for i in sums if i[0] == max_freq]
    if len(filtered) == 1:
        notes = [(note + tonic) % 12 for note in modes[filtered[0]]]
        return (filtered[0], notes)
    else:
        while True:
            stout = "Which mode is this in: " + ", ".join(filtered) + "?\n"
            resp = raw_input(stout).lower()
            if resp in modes:
                notes = [(note + tonic) % 12 for note in modes[resp]]
                return (resp, notes)
            print "I didn't recognize that. Type the name of a mode.\n"

def main():
    cf_in = "C4 D4 F4 E4 D4 E4 D4 C4"
    mode = detect_mode(cf_to_ints(cf_in))
    print "Detected mode: " + mode[0] + "\n"
    spcs = species.FirstSpecies
    #spcs = species.SecondSpecies
    cf = spcs.generate_cf(cf_in)
    harmony = cpt(cf, spcs, mode[1])
    print harmony

if __name__ == '__main__':
    main()