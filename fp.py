# File: fp.py
# Author: Samuel McFalls
# Description: See README.md

import argparse
from sys import exit
from math import log10, floor

args = None # Args available to all functions

# From http://stackoverflow.com/a/9147327/3287359
def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val

# From http://stackoverflow.com/a/12946226/3287359
def bindigits(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)

# From http://stackoverflow.com/a/13662978/3287359
def parse_bin(s):
    t = s.split('.')
    return int(t[0], 2) + int(t[1], 2) / 2.**len(t[1])

# From http://stackoverflow.com/a/3413529/3287359
def round_sig(x, sig=2):
    if (x < 0):
        x = -x
        return -round(x, sig-int(floor(log10(x)))-1)
    elif (x == 0):
        return x
    return round(x, sig-int(floor(log10(x)))-1)

def hexToDec(hexVal):
    try:
        binToDec(bin(int(hexVal, 16))[2:])
    except:
        print("Error: VALUE is not valid")
        exit(1)

def binToDec(binVal):
    if len(binVal) > 32:
        print("Error: VALUE more than 32 bits")
        exit(1)
    if len(binVal) < 32:
        binVal = binVal.zfill(32)
        if (args.verbose):
            print("\nPadded to " + binVal)
    try:
        sign = int(binVal[0]);
        exponent = twos_comp(int(binVal[1:8], 2), 7)
        mantissa = parse_bin("0." + binVal[8:])
    except:
        print("Error: VALUE is not valid")
        exit(1)

    if (args.verbose):
        signStr = "+ Positive" if (binVal[0] == "0") else "- Negative"
        print("\nSign: 1'b" + binVal[0] + " -> " + signStr)
        print("Exponent: 7'b" + binVal[1:8] + " -> " + str(exponent))
        print("Mantissa: 24'b" + binVal[8:] + " -> " + str(mantissa))
        print("(-1) ^ (" + str(sign) + ") * 16 ^ (" + str(exponent) + ") * "
            + str(mantissa) + " =")
    dec = ((-1) ** sign) * (16 ** exponent) * mantissa
    try:
        decSigFigs = round_sig(dec, 6); # Six significant figures
    except:
        if (args.verbose):
            print("\nWarning: Significant Figure conversion failed")
        print(dec)
        return
    print(decSigFigs)

def decToFP(decVal):
    # Convert to float and check the sign
    try:
        decVal = float(decVal)
    except:
        print("Error: VALUE is not valid")

    if (decVal < 0):
        sign = 1
        decVal = abs(decVal)
    else:
        sign = 0

    # Determine the proper exponent
    # Iterate through, starting with -64 and ending with +63
    # It would be more efficient to start with 0 and check as in a binary
    # search, but I won't prematurely optimize
    prev = None
    exponent = None
    for exponent in range(-64, 64):
        if decVal < 16 ** exponent:
            if prev is not None:
                if (decVal >= 16 ** prev):
                    break;
            else:
                break; # The value is less than 16^-64
    # If nothing is found, we must be at or above 16^63

    # Determine the mantissa
    # Again, probably more effecient ways than using parse_bin, such as
    # keeping a running total, but I won't prematurely optimize
    mantissa = list("0.000000000000000000000000")
    for bitNum in range(0, 24):
        mantissa[bitNum + 2] = "1"
        if (parse_bin("".join(mantissa)) * (16 ** exponent) > decVal):
            mantissa[bitNum + 2] = "0"

    expStr = bindigits(exponent, 7)
    manStr = "".join(mantissa[2:])
    manVal = parse_bin("".join(mantissa))

    if (args.verbose):
        signStr = "+ Positive" if (sign == 0) else "- Negative"
        print("\nSign: " + signStr + " -> " + "1'b" + str(sign))
        print("Exponent: " + str(exponent) + " -> " + "7'b" + expStr)
        print("Mantissa: " + str(manVal) + " -> " + "24'b" + manStr)
        print("(-1) ^ (" + str(sign) + ") * 16 ^ (" + str(exponent) + ") * "
            + str(manVal) + " =")
        dec = ((-1) ** sign) * (16 ** exponent) * manVal
        print(dec)
        error = abs(abs(dec) - abs(decVal)) / abs(decVal)
        print("This calculation has error of " + str(error) + "\n")

    print("32'b" + str(sign) + expStr + manStr)


parser = argparse.ArgumentParser(description=
                                "Converts DD2 Format FP <-> Decimal")
parser.add_argument("value", metavar="VALUE", help="The value to convert from")
base = parser.add_mutually_exclusive_group(required=True)
base.add_argument("-x", "--hex", help="Specifies that VALUE is in hex",
                    action="store_true")
base.add_argument("-b", "--bin", help="Specifies that VALUE is in binary",
                    action="store_true")
base.add_argument("-d", "--dec", help="Specifies that VALUE is in decimal",
                    action="store_true")
parser.add_argument("-v", "--verbose", help="Enables more verbose output",
                    action="store_true")

args = parser.parse_args()

if (args.hex):
    hexToDec(args.value)
elif (args.bin):
    binToDec(args.value)
elif (args.dec):
    decToFP(args.value)
