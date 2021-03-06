def note_to_int(note):
    '''
	Converts string representation of note into int, octave specified by last integer,
    where C1 = 0, A0 = -3, C2 = 12, etc.
    '''
    note_to_int_dict = {
        "C": 0,
        "D": 2,
        "E": 4,
        "F": 5,
        "G": 7,
        "A": 9,
        "B": 11,
    }
    if ("#" in note) and ("b" in note):
        raise ValueError("Note cannot be sharp and flat simultaneously")
    octave = int(note[-1]) 
    note_letter = note[0]
    if (octave > 8) or (octave < 0):
        raise ValueError("Octave out of range")
    if note_letter not in note_to_int_dict:
        raise ValueError("Invalid note name")
    result = 12 * (octave - 1) + note_to_int_dict[note_letter]
    if "#" in note:
        result += 1
    if "b" in note:
        result -= 1
    return result

def int_to_note(num, oct=False):
    int_to_note_dict = {
        0 : "C",
        1 : "C#",
        2 : "D",
        3 : "D#",
        4 : "E",
        5 : "F",
        6 : "F#",
        7 : "G",
        8 : "G#",
        9 : "A",
        10 : "A#",
        11 : "B"
    }
    octave = num // 12 + 1
    num = num % 12
    result = int_to_note_dict[num]
    if oct:
        result += str(octave)
    return result

consonances = [3, 4, 7, 8, 9, 12]
perfects = [0, 7, 12]
dissonances = [1, 2, 5, 6, 10, 11]

def is_melodic_leap(note1, note2):
    '''Returns true if interval between both notes is not
    unison, tritone, or 7th'''
    leaps = [0, 6, 10, 11]
    return not abs(note1 - note2) % 12 in leaps

def is_second(note1, note2):
    distance = abs(note1 - note2) % 12 
    return distance == 1 or distance == 2

def is_third(note1, note2):
    distance = abs(note1 - note2) % 12 
    return distance == 3 or distance == 4

def is_fifth(note1, note2):
    distance = abs(note1 - note2) % 12 
    return distance == 7

def is_sixth(note1, note2):
    distance = abs(note1 - note2) % 12 
    return distance == 8 or distance == 9

def is_octave(note1, note2):
    distance = abs(note1 - note2) % 12 
    return distance == 0

def modes():
    '''Returns integers representing numbers of modes as if they started on C1,
    in order of scale degrees'''
    mode = {
        "ionian": [0, 2, 4, 5, 7, 9, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "phrygian": [0, 1, 3, 5, 7, 8, 10],
        "lydian": [0, 2, 4, 6, 7, 9, 11],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "aeolian": [0, 2, 3, 5, 7, 8, 10] 
    }
    return mode

def stepwise(prev, next):
    '''Returns true if next moves in stepwise motion from prev, 
    where prev and next are ints representing notes'''
    intrvl = abs(prev - next)
    return intrvl == 1 or intrvl == 2

def change_direction(note1, note2, note3):
    '''Returns true if direction changes around note2'''
    return (note1 - note2)*(note2 - note3) < 0

def is_perfect(interval):
    return (interval % 12) in perfects

def is_consonance(interval):
    return (interval % 12) in consonances

def is_dissonant(interval):
    return (interval % 12) in dissonances

def scale_degree(note, mode):
    tonic = mode[0]
    note = (note % 12 - tonic) % 12
    if note < 1:
        return 1
    if note < 3:
        return 2
    if note < 5:
        return 3
    if note == 5:
        return 4
    if note == 7:
        return 5
    if note < 10:
        return 6
    if note < 12:
        return 7
    raise ValueError
