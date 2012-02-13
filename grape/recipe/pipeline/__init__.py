# -*- coding: utf-8 -*-
"""
Buildout recipe grape.recipe.pipeline
"""
from grape.recipe.pipeline import prepare


class Recipe(object):
    """
    Buildout recipe for preparing pipelines.
    """

    def __init__(self, buildout, name, options):
        """
        Store the parameters for the buildout recipe.
        """
        self.buildout = buildout
        self.name = name
        self.options = options

    def install(self):
        """
        Prepare the pipeline.
        """
        return prepare.main(self.options, self.buildout)

    def update(self):
        """
        Prepare the updated pipeline.
        """
        return self.install()
