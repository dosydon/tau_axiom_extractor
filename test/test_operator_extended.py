import doctest
import unittest
import encode_observable_operator

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(encode_observable_operator))
    return tests

