import unittest
import os.path
from deps import *
import json

testdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')
repodir = os.path.join(testdir, "simplerepo")
bgendata = False                # True to regenerate test data

class TestDependencies(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def __check(self, expfilename, actual, overwrite):
        if overwrite:
            print 'Overwriting %s' % expfilename
            with open(expfilename, 'w') as expfile:
                expfile.write(actual)
            self.assertTrue(False)
        else:
            with open(expfilename) as expfile:
                self.assertMultiLineEqual(expfile.read(), actual)

    def test_import_tree_creation(self):
        expfilename = os.path.join(repodir, 'import_tree.exp.json')
        deps = import_tree_for_project(repodir)
        self.__check(expfilename, json.dumps(deps.to_dict(), indent=4, sort_keys=True), bgendata)

    def test_leaves(self):
        expfilename = os.path.join(repodir, 'imports.exp.txt')
        deps = import_tree_for_project(repodir)
        actual = '\n'.join(deps.leaves())
        self.__check(expfilename, actual, bgendata)

    def test_root_modules_defined_in(self):
        expfilename = os.path.join(repodir, 'root_modules.exp.txt')
        actual = '\n'.join(root_modules_defined_in(repodir))
        self.__check(expfilename, actual, bgendata)

    def test_modules_defined_in(self):
        expfilename = os.path.join(repodir, 'modules.exp.txt')
        actual = '\n'.join(modules_defined_in(repodir))
        self.__check(expfilename, actual, bgendata)

    def test_external_import_tree(self):
        expfilename = os.path.join(repodir, 'ext_import_tree.exp.json')
        ext_deps = external_import_tree_for_project(repodir)
        self.__check(expfilename, json.dumps(ext_deps.to_dict(), indent=4, sort_keys=True), bgendata)

    def test_python_version(self):
        # Because this library looks through the standard lib, test
        # that the version of python is correct.  Only tested in
        # Python 2.7.5
        import sys
        self.assertTrue(sys.version_info > (2, 7))
