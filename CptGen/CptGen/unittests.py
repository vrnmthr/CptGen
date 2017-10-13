import unittest
import CptGen as cg
import utils as u

class TestMethods(unittest.TestCase):

    def test_note_to_int(self):
        self.assertEqual(u.note_to_int("A1"), 0)
        self.assertEqual(u.note_to_int("A#1"), 1)
        self.assertEqual(u.note_to_int("C4"), 39)
        self.assertEqual(u.note_to_int("C1"), 3)
        self.assertEqual(u.note_to_int("F1"), 8)
        self.assertEqual(u.note_to_int("C2"), 15)
        self.assertRaises(ValueError, u.note_to_int, "Q1")
        self.assertRaises(ValueError, u.note_to_int, "A9")
        self.assertRaises(ValueError, u.note_to_int, ("A3#b"))
        self.assertRaises(ValueError, u.note_to_int, ("Aw"))

    def test_detect_mode(self):
        self.assertEqual(cg.detect_mode(cg.cf_to_ints("C4 D4 E4 F4 G4 A5 B5 C5")), "ionian")
        self.assertEqual(cg.detect_mode(cg.cf_to_ints("D4 E4 F4 G4 A4 B4 C4 D4")), "dorian")
        self.assertEqual(cg.detect_mode(cg.cf_to_ints("E4 F4 G4 A4 B4 C4 D4 E4")), "phrygian")
        self.assertEqual(cg.detect_mode(cg.cf_to_ints("F4 G4 A4 B4 C4 D4 E4 F4")), "lydian")
        self.assertEqual(cg.detect_mode(cg.cf_to_ints("G4 A4 B4 C4 D4 E4 F4 G4")), "mixolydian")
        self.assertEqual(cg.detect_mode(cg.cf_to_ints("A4 B4 C4 D4 E4 F4 G4 A4")), "aeolian")

if __name__ == '__main__':
    unittest.main()
