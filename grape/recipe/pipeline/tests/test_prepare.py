"""
Test for prepare.py
"""

import os
import unittest
import shutil
from pkg_resources import get_provider

from grape.recipe.pipeline.prepare import main
from grape.recipe.pipeline.prepare import run_python
from grape.recipe.pipeline.prepare import get_pipeline_script_command
from grape.recipe.pipeline.prepare import CUFFLINKS_BINARIES

PROVIDER = get_provider('grape.recipe.pipeline')
SANDBOX = PROVIDER.get_resource_filename("", 'tests/sandbox/')
PATH = os.path.join(SANDBOX, 'buildout')
OPTIONS = {
    'accession': 'TestRun',
    'location': os.path.join(PATH, 'parts/TestRun'),
    }
BUILDOUT = {
    'TestRun': {
        'file_location': '\n'.join([
            os.path.join(PATH, "src/testdata/testA.r2.fastq.gz"),
            os.path.join(PATH, "src/testdata/testA.r1.fastq.gz"),
            os.path.join(PATH, "src/testdata/testB.r2.fastq.gz"),
            os.path.join(PATH, "src/testdata/testB.r1.fastq.gz")]),
        'species': 'Homo sapiens',
        'readType': '2x76',
        'cell': 'NHEK',
        'rnaExtract': 'LONGPOLYA',
        'localization': 'CELL',
        'qualities': 'solexa',
        'pair_id': 'testA\ntestA\ntestB\ntestB',
        'mate_id': 'testA.2\ntestA.1\ntestB.2\ntestB.1',
        'label': 'Test\nTest\nTest\nTest',
       },
    'pipeline': {
         'TEMPLATE': os.path.join(
             PATH,
             "/src/pipeline/template3.0.txt"),
         'PROJECTID': 'Test',
         'THREADS': '2',
         'DB': 'TestRNAseqPipeline',
         'COMMONDB': 'TestRNAseqPipelineCommon',
         'MAPPER': 'GEM',
         'MISMATCHES': '2',
         'GENOMESEQ': os.path.join(
             PATH,
             "/src/testdata/H.sapiens.genome.hg19.test.fa"),
         'ANNOTATION': os.path.join(
             PATH,
             "/src/testdata/H.sapiens.EnsEMBL.55.test.gtf"),
        },
    'buildout': {'directory': PATH},
    'settings': {
         'java': '',
         'flux_jar': '',
         'overlap': os.path.join(PATH, 'src/overlap/overlap'),
         'gem_folder': os.path.join(PATH, 'src/gem'),
         }
    }
SCRIPT = ["#!/bin/bash\nbin/start_RNAseq_pipeline.3.0.pl",
          "-species",
          "'Homo",
          "sapiens'",
          "-genome",
          "/src/testdata/H.sapiens.genome.hg19.test.fa",
          "-annotation",
          "/src/testdata/H.sapiens.EnsEMBL.55.test.gtf",
          "-project",
          "Test",
          "-experiment",
          "TestRun",
          "-template",
          "/src/pipeline/template3.0.txt",
          "-readlength",
          "76",
          "-cellline",
          "'NHEK'",
          "-rnafrac",
          "LONGPOLYA",
          "-compartment",
          "CELL",
          "-threads",
          "2",
          "-qualities",
          "solexa",
          "-database",
          "TestRNAseqPipeline",
          "-commondb",
          "TestRNAseqPipelineCommon",
          "-mapper",
          "GEM",
          "-mismatches",
          "2"]


class MainTests(unittest.TestCase):
    """
    Test the main method in prepare.py
    """

    def setUp(self):  # pylint: disable=C0103
        shutil.rmtree(PATH, ignore_errors=True)
        os.mkdir(PATH)
        os.mkdir(os.path.join(PATH, 'bin'))
        os.mkdir(os.path.join(PATH, 'parts'))
        os.mkdir(os.path.join(PATH, 'parts/TestRun'))
        os.mkdir(os.path.join(PATH, 'src'))
        os.mkdir(os.path.join(PATH, 'src/flux'))
        os.mkdir(os.path.join(PATH, 'src/flux/bin'))
        path = open(os.path.join(PATH, 'src/flux/bin/flux'), 'w')
        path.close()
        os.mkdir(os.path.join(PATH, 'src/gem'))
        os.mkdir(os.path.join(PATH, 'src/overlap'))
        path = open(os.path.join(PATH, 'src/overlap/overlap'), 'w')
        path.close()
        cufflinks_path = os.path.join(PATH, 'src/cufflinks')
        os.mkdir(cufflinks_path)
        for cuffbin in CUFFLINKS_BINARIES:
            path = open(os.path.join(cufflinks_path, cuffbin), 'w')
            path.close()
        os.mkdir(os.path.join(PATH, 'src/pipeline'))
        os.mkdir(os.path.join(PATH, 'src/pipeline/bin'))
        os.mkdir(os.path.join(PATH, 'src/pipeline/lib'))
        os.mkdir(os.path.join(PATH, 'src/testdata'))
        path = open(os.path.join(PATH,
                                 'src/testdata/testA.r1.fastq.gz'), 'w')
        path.close()
        path = open(os.path.join(PATH,
                                 'src/testdata/testA.r2.fastq.gz'), 'w')
        path.close()
        path = open(os.path.join(PATH,
                                 'src/testdata/testB.r1.fastq.gz'), 'w')
        path.close()
        path = open(os.path.join(PATH,
                                 'src/testdata/testB.r2.fastq.gz'), 'w')
        path.close()
        os.mkdir(os.path.join(PATH, 'var'))

    def test_main(self):
        """
        Test the main method
        """
        os.chdir(PATH)
        result = main(OPTIONS.copy(), BUILDOUT.copy())
        self.failUnless(result == None)


class PipelineScriptTests(unittest.TestCase):
    """
    Test the part producing the pipeline scripts.
    """

    def test_command(self):
        """
        Test the get_pipeline_script_command
        """
        os.chdir(PATH)
        buildout = BUILDOUT.copy()
        accession = buildout['TestRun']
        pipeline = BUILDOUT['pipeline'].copy()
        options = OPTIONS.copy()
        options['experiment_id'] = os.path.split(options['location'])[-1]
        command = get_pipeline_script_command(accession, pipeline, options)
        self.failUnless(command.split(' ') == SCRIPT, command.split(' '))

    def test_more_options(self):
        """
        Test the get_pipeline_script_command method with replicate and other
        options.
        """
        os.chdir(PATH)
        buildout = BUILDOUT.copy()
        accession = buildout['TestRun']
        accession['replicate'] = '1'
        pipeline = BUILDOUT['pipeline'].copy()
        pipeline['HOST'] = 'dummyhost'
        pipeline['PREPROCESS'] = 'dummypreprocess'
        pipeline['PREPROCESS_TRIM_LENGTH'] = 'dummytrimlength'
        options = OPTIONS.copy()
        options['experiment_id'] = os.path.split(options['location'])[-1]
        options['description'] = 'dummydescription'
        command = get_pipeline_script_command(accession, pipeline, options)
        self.failUnless(" -bioreplicate 1 " in command)
        self.failUnless(" -host dummyhost " in command)
        self.failUnless(" -run_description 'dummydescription' " in command)
        self.failUnless(" -preprocess 'dummypreprocess' " in command)
        self.failUnless(" -preprocess_trim_length dummytrimlength" in command)

    def test_empty_cluster(self):
        """
        Test the get_pipeline_script_command method with empty cluster
        """
        os.chdir(PATH)
        buildout = BUILDOUT.copy()
        accession = buildout['TestRun']
        pipeline = BUILDOUT['pipeline'].copy()
        pipeline['CLUSTER'] = ''
        options = OPTIONS.copy()
        options['experiment_id'] = os.path.split(options['location'])[-1]
        self.failUnlessRaises(AttributeError,
                              get_pipeline_script_command,
                              accession,
                              pipeline,
                              options)

    def test_cluster_given(self):
        """
        Test the get_pipeline_script_command method with cluster
        """
        os.chdir(PATH)
        buildout = BUILDOUT.copy()
        accession = buildout['TestRun']
        pipeline = BUILDOUT['pipeline'].copy()
        pipeline['CLUSTER'] = 'dummy'
        options = OPTIONS.copy()
        options['experiment_id'] = os.path.split(options['location'])[-1]
        command = get_pipeline_script_command(accession, pipeline, options)
        self.failUnless(" -cluster dummy " in command)


class RunPythonTests(unittest.TestCase):
    """
    Test the RestrictedPython part
    """

    def test_with_prefix(self):
        """
        Run it with an unexpected 'python:' prefix
        """
        self.failUnlessRaises(AttributeError, run_python, "python:", {})

    def test_echo(self):
        """
        Just a string should be echoed
        """
        self.failUnless(run_python("'dummy'", {}) == 'dummy')

    def test_using_accession(self):
        """
        A list of uses of the accession dictionary returns the values.
        """
        code = "accession['cell'], accession['replicate']"
        accession = {'cell': 'Cell', 'replicate': 'Replicate'}
        self.failUnless(run_python(code, accession) == "Cell Replicate")


def test_suite():
    """
    Run the test suite
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
