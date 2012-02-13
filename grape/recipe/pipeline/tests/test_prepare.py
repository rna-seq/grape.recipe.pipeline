"""
Test for prepare.py
"""

import unittest
from pkg_resources import get_provider

from grape.recipe.pipeline.prepare import main


class MainTests(unittest.TestCase):
    """
    Test the main method in prepare.py
    """

    def test_main(self):
        """
        Test the main method
        """
        options = {}
        buildout = {}
        result = main(options, buildout)


def test_suite():
    """
    Run the test suite
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
