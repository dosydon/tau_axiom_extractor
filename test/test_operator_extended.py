import doctest
import unittest
import operator_extended

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(operator_extended))
    return tests

