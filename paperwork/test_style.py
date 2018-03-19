from pylint import epylint as lint
import os, errno, re
from django.test import TestCase

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

python_extension = '.py'
pylint_out = "./paperwork/pylint_out"
ignore_dirs = ["./paperwork/migrations", pylint_out]

class StyleTestCase(TestCase):
    def test_run(self):
        # keep a list of failing style files
        threshold_score = 8
        failing_style_files = []

        mkdir_p(pylint_out)
        for root, dirs, files in os.walk("./paperwork", topdown=True):
            for name in files:
                score = self.lint_file(root, name)
                if score is not None and score < threshold_score:
                    failing_style_files.append(os.path.join(root, name))

        if failing_style_files:
            self.assertEqual(
                len(failing_style_files), 
                0, 
                "{l} style checks failed: {cases}".format(
                    l=len(failing_style_files),
                    cases=failing_style_files))

    def lint_file(self, root, name):
        is_ignored = any([root.startswith(i) for i in ignore_dirs])
        if not is_ignored and name.endswith(python_extension):
            mkdir_p(os.path.join(pylint_out, root))
            target_filename = os.path.join(root, name)
            (pylint_stdout, pylint_stderr) = lint.py_run(
                target_filename + " --load-plugins pylint_django", 
                return_std=True)

            output_filename = target_filename[:-len(python_extension)] + '.txt'
            output_filename = os.path.join(pylint_out, output_filename)

            full_output = pylint_stdout.getvalue()
            with open(output_filename, 'w') as file:
                file.write(full_output)
            regex = r"Your code has been rated at (-?[\d\.]+)/10"
            matches = re.findall(regex, full_output)
            self.assertLessEqual(len(matches), 1)
            if len(matches) == 1:
                return float(matches[0])
                