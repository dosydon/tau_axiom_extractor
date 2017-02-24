import unittest
import os
from sas3_extended import SAS3Extended
from preprocess import normalize

class TestSas(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
    def test_sokoban01_unormalized(self):
        file_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        tested_sas = SAS3Extended.from_file(os.path.join(file_dir, 'test_cases/sokoban01_unnormalized.sas'))
        expected_sas = SAS3Extended.from_file(os.path.join(file_dir, 'test_cases/sokoban01_extracted.sas'))

        normalize(tested_sas)
        self.assertEqual(str(tested_sas),str(expected_sas))

if __name__ == '__main__':
    unittest.main()
