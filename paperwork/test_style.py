"""
Use pylint to check style. Test cases are dynamically generated.
Isn't it cool?
"""

import os
import sys
import errno
import re

from django.test import TestCase
from pylint import epylint as lint

def mkdir_p(path):
    """ creates a directory if necessary """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

PYTHON_EXTENSION = '.py'
PYLINT_OUT = "./paperwork/pylint_out"
ENABLE_DIRS = ["./paperwork"]
DISABLE_DIRS = ["./paperwork/migrations", PYLINT_OUT]
EXTRA_OPTIONS = " ".join([
    # need an empty string for that leading space.
    "",

    # first, Django's subclassing of Models, etc. give lotsa errors.
    # Make Pylint smart about django.
    '--load-plugins="pylint_django,linecount"',

    "--max-line-length=80", # be rigorous in line length

    # test names are OK long because they aren't called in code.
    "--method-rgx (([a-z_][a-z0-9_]{2,30})|" +
    "((test|assert)_[a-z_][a-z0-9_]{2,50}))$",
])

class StyleTestsMeta(type):
    """
    Metaclass that creates a test for each style check.
    Mostly borrowed from
    # pylint disable=max-line-length
    https://chris-lamb.co.uk/posts/generating-dynamic-python-tests-using-metaclasses
    # pylint enable=max-line-length
    """
    def __new__(mcs, name, bases, attrs):
        """ tbh not sure when this function is called. """
        # setup
        threshold_score = 8

        # walk through the files, making test classes for each file.
        for enabled_dir in ENABLE_DIRS:
            for root, _, files in os.walk(enabled_dir, topdown=True):
                for fname in files:
                    is_ignored = any([root.startswith(i) for i in DISABLE_DIRS])
                    if not is_ignored and fname.endswith(PYTHON_EXTENSION):
                        # make a test case for it!
                        name_no_extension = fname[:-len(PYTHON_EXTENSION)]
                        big_path = os.path.join(root, name_no_extension)
                        underscored_path = big_path[2:].replace("/", "_")
                        test_name = 'test_%s' % underscored_path
                        attrs[test_name] = mcs.gen(root, fname, threshold_score)

        return super(StyleTestsMeta, mcs).__new__(mcs, name, bases, attrs)

    @classmethod
    def gen(mcs, root, name, threshold_score):
        # Return a testcase that checks the style of file with path.
        def generated_function(self):
            mkdir_p(os.path.join(PYLINT_OUT, root))
            target_filename = os.path.join(root, name)
            (pylint_stdout, _) = lint.py_run(
                target_filename + EXTRA_OPTIONS,
                return_std=True)

            output_filename = target_filename[:-len(PYTHON_EXTENSION)] + '.txt'
            output_filename = os.path.join(PYLINT_OUT, output_filename)

            full_output = pylint_stdout.getvalue()
            with open(output_filename, 'w') as output_file:
                output_file.write(full_output)
            regex = r"Your code has been rated at (-?[\d\.]+)/10"
            matches = re.findall(regex, full_output)
            self.assertLessEqual(len(matches), 1)
            # sometimes, no matches are made if pylint is parsing an empty file
            if matches:
                score = float(matches[0])
                self.assertGreaterEqual(score, threshold_score)

        return generated_function

class StyleTests(TestCase):
    __metaclass__ = StyleTestsMeta

    @classmethod
    def setUpClass(cls):
        super(StyleTests, cls).setUpClass()
        # make sure you can reach the linecount checker
        sys.path.append('./paperwork/')
