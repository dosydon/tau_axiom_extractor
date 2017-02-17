import doctest
import unittest
import operator_extended

def load_tests(loader, tests, ignore):
    print("load_tests")
    tests.addTests(doctest.DocTestSuite(operator_extended))
    return tests

