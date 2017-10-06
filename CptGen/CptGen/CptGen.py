def note_to_int(note):
	'''
	Converts string representation of note into int, octave specified by last integer. 
	'''
	if ("#" in note) and ("b" in note):
		raise ValueError("Note cannot be sharp and flat simultaneously")
	note_vals = {
		"A": 0,
		"B": 2,
		"C": 3,
		"D": 5,
		"E": 7,
		"F": 8,
		"G": 10
	}
	octave = int(note[-1]) 
	note_letter = note[0]
	if (octave > 8) or (octave < 1):
		raise ValueError("Octave out of range")
	if note_letter not in note_vals:
		raise ValueError("Invalid note name")
	result = 12 * (octave - 1) + note_vals[note_letter]
	if "#" in note:
		result += 1
	if "b" in note:
		result -= 1
	return result

def main():
	note_to_int("C#")
	print "started"