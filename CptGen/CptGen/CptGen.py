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
	if note_letter not in note_vals:
		raise ValueError("Invalid note name")
	result = 12 * (octave - 1) + utils.note_vals[note_letter]
	if "#" in note:
		result += 1
	if "b" in note:
		result -= 1
	return result

def int_to_note(num, oct = False):
	octave = num // 12
	num = num % 12
	result = utils.note_vals[num]
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
	def cpt_inner(cpt, cf, gf):
		'''
		Calculates counterpoint from given note until 
		'''
		#cpt is list of tuples where first int represents cpt note
		#and second int represents interval between cpt and cf
	
		allowable = gf(cf[0])
		for option in allowable:
			added = (option, abs(cf[0] - option))
			rest_cpt = cpt_inner(cpt + option, cf[1:], gf)
			if rest_cpt:
				return added + rest_cpt
		return []
	
	return cpt_inner([], cf, gf)

def first_species(note, prev, mode):
	'''
	Given a note (int) and the previous counterpoint written
	generates a list of potential next notes. 
	Rules followed:
	1. Only 3rds, 5th, 6th, 8th allowed
	2. No repeating same note
	3. Must recover all leaps
	4. No perfect intervals in a row
	5. No perfect intervals in similar motion
	'''
	options = [note + 3, note + 4, note + 7, note + 8, note + 9, note + 12]
	for option in options:
		in_mode = option in mode

	pass

def main():
	cf = cf_to_ints("C#1 A1 Bb1")
	print cf

if __name__ == '__main__':
    main()