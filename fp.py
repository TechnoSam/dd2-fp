# File: fp.py
# Author: Samuel McFalls
# Description: See README.md

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-x", "--hex", help="Specifies that the input is in hex",
                    action="store_true")
parser.add_option("-b", "--bin", help="Specifies that the input is in binary",
                    action="store_true")
parser.add_option("-d", "--dec", help="Specifies that the input is in decimal",
                    action="store_true")
parser.add_option("-f", "--file", dest="file",
                    help="Reads input from FILENAME", metavar="FILENAME");

(options, args) = parser.parse_args()

# options is a dictionary of parameter-value pairs corresponding to the
# switches or flags (eg -t test, -l). Flags are set to True.
# args is a list of positional arguments

# Determine the type of input (no conflicts allowed)
