"""Tests for the file_path module.

"""
# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2005, Enthought, Inc.
# License: BSD Style.

# Standard library imports.
import unittest
import os
import sys
from os.path import abspath, dirname, basename, join
import StringIO

# Enthought library imports.
from apptools.persistence import state_pickler
from apptools.persistence import file_path

class Test:
    def __init__(self):
        self.f = file_path.FilePath()


class TestFilePath(unittest.TestCase):
    def test_relative(self):
        """Test if relative paths are set correctly.
        """
        fname = 't.vtk'
        f = file_path.FilePath(fname)
        cwd = os.getcwd()
        # Trivial case of both in same dir.
        f.set_relative(abspath(join(cwd, 't.mv2')))
        self.assertEqual(f.rel_pth, fname)
        # Move one directory deeper.
        f.set_relative(abspath(join(cwd, 'tests', 't.mv2')))
        self.assertEqual(f.rel_pth, join(os.pardir, fname))
        # Move one directory shallower.
        f.set_relative(abspath(join(dirname(cwd), 't.mv2')))
        diff = basename(cwd)
        self.assertEqual(f.rel_pth, join(diff, fname))
        # Test where the path is relative to the root.
        f.set(abspath(join('data', fname)))
        f.set_relative('/tmp/test.mv2')
        if sys.platform.startswith('win'):
            expect = os.pardir + abspath(join('data', fname))[2:]
        else:
            expect = os.pardir + abspath(join('data', fname))
        self.assertEqual(f.rel_pth, expect)

    def test_absolute(self):
        """Test if absolute paths are set corectly.
        """
        fname = 't.vtk'
        f = file_path.FilePath(fname)
        cwd = os.getcwd()
        # Easy case of both in same dir.
        f.set_absolute(join(cwd, 'foo', 'test', 't.mv2'))
        self.assertEqual(f.abs_pth, join(cwd, 'foo', 'test', fname))
        # One level lower.
        fname = join(os.pardir, 't.vtk')
        f.set(fname)
        f.set_absolute(join(cwd, 'foo', 'test', 't.mv2'))
        self.assertEqual(f.abs_pth, abspath(join(cwd, 'foo', 'test', fname)))
        # One level higher.
        fname = join('test', 't.vtk')
        f.set(fname)
        f.set_absolute(join(cwd, 'foo', 't.mv2'))
        self.assertEqual(f.abs_pth, abspath(join(cwd, 'foo', fname)))

    def test_pickle(self):
        """Test if pickler works correctly with FilePaths.
        """
        t = Test()
        t.f.set('t.vtk')
        cwd = os.getcwd()

        # Create a dummy file in the parent dir.
        s = StringIO.StringIO()
        # Spoof its location.
        s.name = abspath(join(cwd, os.pardir, 't.mv2'))
        # Dump into it
        state_pickler.dump(t, s)

        # Rewind the stream
        s.seek(0)
        # "Move" the file elsewhere
        s.name = join(cwd, 'foo', 'test', 't.mv2')
        state = state_pickler.load_state(s)
        self.assertEqual(state.f.abs_pth,
                         join(cwd, 'foo', 'test', 'tests', 't.vtk'))


        # Create a dummy file in a subdir.
        s = StringIO.StringIO()
        # Spoof its location.
        s.name = abspath(join(cwd, 'data', 't.mv2'))
        # Dump into it.
        state_pickler.dump(t, s)

        # Rewind the stream
        s.seek(0)
        # "Move" the file elsewhere
        s.name = join(cwd, 'foo', 'test', 't.mv2')
        state = state_pickler.load_state(s)
        self.assertEqual(state.f.abs_pth,
                         join(cwd, 'foo', 't.vtk'))



def test_suite():
    """Collects all the tests to be run."""
    suites = []
    suites.append(unittest.makeSuite(TestFilePath, 'test_'))
    total_suite = unittest.TestSuite(suites)
    return total_suite

def test(verbose=2):
    """Useful when you need to run the tests interactively."""
    all_tests = test_suite()
    runner = unittest.TextTestRunner(verbosity=verbose)
    result = runner.run(all_tests)
    return result, runner

if __name__ == "__main__":
    unittest.main()
