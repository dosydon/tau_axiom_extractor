import unittest
import os
from sas3_extended import SAS3Extended
from encode import encode
from extract_tau_operators_opgraph import extract_tau_operators_opgraph
from extract_tau_operators_top import extract_tau_operators_top

class TestSas(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_sas3_extended(self):
        file_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = 'test_cases/miconic.sas'
        abs_file_path = os.path.join(file_dir, rel_path)
        sas = SAS3Extended.from_file(abs_file_path)
        with open(abs_file_path,'r') as f:
            self.assertEqual(str(sas),f.read())

    def test_miconic_extracted_top_down(self):
        file_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        original_sas = SAS3Extended.from_file(os.path.join(file_dir, 'test_cases/miconic.sas'))
        encoded_sas = SAS3Extended.from_file(os.path.join(file_dir, 'test_cases/miconic_extracted.sas'))

        candidates = extract_tau_operators_top(original_sas)
        if len(candidates) > 0:
            original_sas = encode(original_sas,candidates)
        self.assertEqual(str(original_sas),str(encoded_sas))

    def test_gripper01_extracted_top_down(self):
        file_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        original_sas = SAS3Extended.from_file(os.path.join(file_dir, 'test_cases/gripper01.sas'))
        encoded_sas = SAS3Extended.from_file(os.path.join(file_dir, 'test_cases/gripper01_extracted.sas'))

        candidates = extract_tau_operators_top(original_sas)
        if len(candidates) > 0:
            original_sas = encode(original_sas,candidates)
        self.assertEqual(str(original_sas),str(encoded_sas))

    def test_gripper01_extracted_opgraph(self):
        file_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        original_sas = SAS3Extended.from_file(os.path.join(file_dir, 'test_cases/gripper01.sas'))
        encoded_sas = SAS3Extended.from_file(os.path.join(file_dir, 'test_cases/gripper01_extracted.sas'))

        candidates = extract_tau_operators_opgraph(original_sas)
        if len(candidates) > 0:
            original_sas = encode(original_sas,candidates)
        self.assertEqual(str(original_sas),str(encoded_sas))

    def test_sokoban01_extracted_top_down(self):
        file_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        original_sas = SAS3Extended.from_file(os.path.join(file_dir, 'test_cases/sokoban01_essential.sas'))
        encoded_sas = SAS3Extended.from_file(os.path.join(file_dir, 'test_cases/sokoban01_extracted.sas'))

        candidates = extract_tau_operators_top(original_sas)
        if len(candidates) > 0:
            original_sas = encode(original_sas,candidates)
        with open('output.sas','w') as f:
            print(str(original_sas),file=f)
        self.assertEqual(str(original_sas),str(encoded_sas))

if __name__ == '__main__':
    unittest.main()

