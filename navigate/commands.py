"""
navigate: Navigation software

Usage:
  navigate [--plot] [--min-depth=DEPTH] <inputfile>
  navigate -h | --help
  navigate --version

Options:
  -h --help             show this help
  --version             show version info
  -d --min-depth=DEPTH  compute using this minimum ship depth
  -p --plot             plot results (assumes `pip install navigate[plot]`)
"""
import docopt


def parse_command_line():
    """parse command line options"""
    options = docopt.docopt(__doc__)
    return options


def main():
    """run the main program"""
    options = parse_command_line()
    print(options)
