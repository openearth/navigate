"""
navigate: Navigation software

Usage:
  navigate [--plot] [--min-depth=DEPTH] <inputfile>
  navigate -h | --help
  navigate --version

Options:
  -h --help             show this help
  --version             show version info
  -d --min-depth=DEPTH  compute using this minimum ship depth [default: 0]
  -p --plot             plot results (assumes `pip install navigate[plot]`)
"""
import os
import logging

import docopt

from .io import get_last_depth, to_geojson
from .algorithms import navigate

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def parse_command_line():
    """parse command line options"""
    options = docopt.docopt(__doc__)
    logger.info('options: %s', options)
    # parse and check input files
    options['filename'] = options['<inputfile>']
    assert os.path.isfile(options['filename']), 'file should exist'
    options['min-depth'] = float(options['--min-depth'])
    return options


def main():
    """run the main program"""
    options = parse_command_line()
    filename = options['filename']
    data = get_last_depth(filename)
    navigation_results = navigate(data, options)
    print(to_geojson(navigation_results['xy']))
