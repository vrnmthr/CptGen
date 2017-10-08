import unittest
import CptGen

class TestMethods(unittest.TestCase):

    def test_note_to_int(self):
        self.assertEqual(CptGen.note_to_int("A1"), 0)
        self.assertEqual(CptGen.note_to_int("A#1"), 1)
        self.assertEqual(CptGen.note_to_int("C4"), 39)
        self.assertEqual(CptGen.note_to_int("C1"), 3)
        self.assertEqual(CptGen.note_to_int("F1"), 8)
        self.assertEqual(CptGen.note_to_int("C2"), 15)
        self.assertRaises(ValueError, CptGen.note_to_int, "Q1")
        self.assertRaises(ValueError, CptGen.note_to_int, "A9")
        self.assertRaises(ValueError, CptGen.note_to_int, ("A3#b"))
        self.assertRaises(ValueError, CptGen.note_to_int, ("Aw"))

if __name__ == '__main__':
    unittest.main()
