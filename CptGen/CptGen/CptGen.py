import utils as u
import species

def cf_to_ints(cf):
    '''
    Converts space separated list of notes into list of integers
    '''
    return [note_to_int(note) for note in cf.split()]    

def cpt(cf, spcs):
    '''
    Returns counterpoint for a given cf (list of ints), and spcs,
    a class representation of SpeciesCpts
    '''
    def cpt_inner(cf, cpt, base=False):
        allowable = spcs.next_move(cf, cpt, None)
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

def main():
    cf_in = "C4 D4 F4 E4 D4 E4 D4 C4"
    spcs = species.FirstSpecies
    cf = spcs.generate_cf(cf_in)
    harmony = cpt(cf, spcs)
    print harmony

if __name__ == '__main__':
    main()