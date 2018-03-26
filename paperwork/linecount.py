import tokenize

from pylint.interfaces import ITokenChecker
from pylint.checkers import BaseChecker

# This is our checker class.
# Checkers should always inherit from `BaseChecker`.
class LineCountChecker(BaseChecker):
    """Add class member attributes to the class locals dictionary."""

    # This class variable defines the type of checker that we are implementing.
    # In this case, we are implementing an Token checker.
    __implements__ = ITokenChecker

    # The name defines a custom section of the config for this checker.
    name = 'custom'
    # The priority indicates the order that pylint will run the checkers.
    priority = -1
    # This class variable declares the messages (ie the warnings and errors)
    # that the checker can emit.
    msgs = {
        # Each message has a code, a message that the user will see,
        # a unique symbol that identifies the message,
        # and a detailed help message
        # that will be included in the documentation.
        'C4401': ('Method is too long (%s/%s)',
                  'method-line-count',
                  'Used when a method is longer than a given number of lines.')
    }
    # This class variable declares the options
    # that are configurable by the user.
    options = (
        # Each option definition has a name which is used on the command line
        # and in config files, and a dictionary of arguments
        # (similar to those to those to
        # argparse.ArgumentParser.add_argument).
        ('line-count-limit',
         {'default': 40, 'type' : "int", 'metavar' : '<int>',
          'help': ('Maximum number of lines with code in a method.'),
         },
        ),
    )

    def process_tokens(self, tokens):
        relevant_defs = []
        for tok_type, token, start, _, _ in tokens:
            # if it's a name, let's see what it's called
            if tok_type == tokenize.NAME and token == "def":
                # great, it's a def token, let's start counting.
                relevant_defs.append({
                    "def_line" : start[0],
                    "indent_count" : 0,
                    "line_count" : 0})

            # if it's a newline,
            elif tok_type == tokenize.NEWLINE:
                # count it in all levels
                for def_level in relevant_defs:
                    def_level["line_count"] += 1

            # if it's an indent,
            elif tok_type == tokenize.INDENT:
                # increase the indentation count
                for def_level in relevant_defs:
                    def_level["indent_count"] += 1

            # if it's a dedent
            elif tok_type == tokenize.DEDENT:
                # decrease the indentation count
                for def_level in relevant_defs:
                    def_level["indent_count"] -= 1

                # see if a def finished:
                if relevant_defs and relevant_defs[-1]["indent_count"] == 0:
                    finished_def = relevant_defs.pop()
                    # check its newline count
                    line_count = finished_def["line_count"]
                    if line_count > self.config.line_count_limit:
                        # make a call to raise a complaint
                        self.add_message(
                            'method-line-count',
                            args=(line_count, self.config.line_count_limit),
                            line=finished_def["def_line"])

def register(linter):
    """This required method auto registers the checker.

    :param linter: The linter to register the checker to.
    :type linter: pylint.lint.PyLinter
    """
    linter.register_checker(LineCountChecker(linter))
