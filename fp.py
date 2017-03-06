# File: fp.py
# Author: Samuel McFalls
# Description: See README.md

import argparse
from sys import exit
from math import log10, floor

# From http://stackoverflow.com/a/9147327/3287359
def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val

# From http://stackoverflow.com/a/13662978/3287359
def parse_bin(s):
    t = s.split('.')
    return int(t[0], 2) + int(t[1], 2) / 2.**len(t[1])

# From http://stackoverflow.com/a/3413529/3287359
def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(x)))-1)

def hexToDec(hexVal):
    try:
        binToDec(bin(int(hexVal, 16))[2:].zfill(32))
    except:
        print("Error: VALUE is not valid")
        exit(1)

def binToDec(binVal):
    if len(binVal) > 32:
        print("Error: VALUE more than 32 bits")
        exit(1)
    if len(binVal) < 32:
        binVal = binVal.zfill(32)
    try:
        sign = int(binVal[0]);
        exponent = twos_comp(int(binVal[1:8], 2), 7)
        mantissa = parse_bin("0." + binVal[8:])
    except:
        print("Error: VALUE is not valid")
        exit(1)

    dec = ((-1) ** sign) * (16 ** exponent) * mantissa
    decSigFigs = round_sig(dec, 6); # Six significant figures
    print(decSigFigs)

def decToFP(decVal):
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
