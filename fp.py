# File: fp.py
# Author: Samuel McFalls
# Description: See README.md

import argparse
from sys import exit

def hexToDec(hex):
    print("hexToDec")

def binToDec(bin):
    print("binToDec")

def decToFP(dec):
    print("decToFP")

parser = argparse.ArgumentParser(description="Converts DD2 Format FP <-> Decimal")
parser.add_argument("value", metavar="VALUE", help="The value to convert from")
base = parser.add_mutually_exclusive_group(required=True)
base.add_argument("-x", "--hex", help="Specifies that VALUE is in hex",
                    action="store_true")
base.add_argument("-b", "--bin", help="Specifies that VALUE is in binary",
                    action="store_true")
base.add_argument("-d", "--dec", help="Specifies that VALUE is in decimal",
                    action="store_true")

args = parser.parse_args()

if (args.hex):
    hexToDec(args.value)
elif (args.bin):
    binToDec(args.value)
elif (args.dec):
    decToFP(args.value)
