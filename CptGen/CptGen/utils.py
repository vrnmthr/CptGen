note_to_int = {
    "A": 0,
    "B": 2,
    "C": 3,
    "D": 5,
    "E": 7,
    "F": 8,
    "G": 10
}

int_to_note = {
    0 : "A",
    1 : "A#",
    2 : "B",
    3 : "C",
    4 : "C#",
    5 : "D",
    6 : "D#",
    7 : "E",
    8 : "F",
    9 : "F#",
    10 : "G",
    11 : "G#"
}



consonances = [3, 4, 7, 8, 9, 12]
perfects = [0, 7, 12]
dissonances = [1, 2, 5, 6, 10, 11]

def is_melodic_leap(note1, note2):
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
    return distance == 12


def is_perfect(interval):
    return (interval % 12) in perfects

def is_consonance(interval):
    return (interval % 12) in consonances

def is_dissonant(interval):
    return (interval % 12) in dissonances

def in_mode(note, mode):
    note = note % 12
    mode = [0, 2, 3, 5, 7, 8, 10]
    return note in mode

def scale_degree(note, mode):
    base = 3
    note = note % 12 - base
    if note < 0:
        note += 12
    if note < 1:
        return 1
    if note < 3:
        return 2
    if note < 5:
        return 3
    if note == 7:
        return 5
    if note < 10:
        return 6
    if note < 12:
        return 7
    raise ValueError
