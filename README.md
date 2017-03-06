# dd2-fp
Custom 32-bit floating bit converter for ECE 4514 Digital Design II at Virginia Tech.
***This project was developed on Python 3.6.0***

Converts from decimal numbers to our custom Floating Point format.
Converts hex or binary numbers in our custom Floating Point format to decimal.

    usage: fp.py [-h] (-x | -b | -d) [-v] VALUE


Use the flags -x, -b, or -d to specify the input base as hex, binary, or decimal respectively. Exactly one of these flags is required. In the future, I hope to update the script to be smart enough to guess your input base.

Use the -v flag to enable verbose output which provides details about the conversion.

##How it works
###Floating Point to Decimal
The input string is checked for errors and split into sign, exponent, and fractional mantissa. The value is then calculated as (-1) ^ sign * 16 ^ exponent * mantissa.
###Decimal to Floating Point
The input string is checked for errors and converted to a float. If it is less than 0, the sign is set to 1 and the value changed to its absolute value.
Next each exponent from -64 to 63 is checked until one is found such that the input value is less than 16 raised to the current exponent and greater than or equal to 16 raised to the previous exponent. This ensures that the best match is found. This algorithm could certainly be optimized by way of a binary search, but I'll quote Knuth on this one:
 `Premature optimization is the root of all evil`
 The algorithm works well enough so for the time being, there's no reason to change it.
 Next the mantissa is determined by setting each bit to 1 and checking if that causes (mantissa * 16 ^ exponent) to be greater than the input value. If it does, the value is set back to zero. Again, this can certainly be optimized, but I'll point you to the previous paragraph.

##References
Two's Complement value from Integer: http://stackoverflow.com/a/9147327/3287359
Integer to Two's Complement binary string: http://stackoverflow.com/a/12946226/3287359
Binary Number with radix point to Float: http://stackoverflow.com/a/13662978/3287359
Significant Figure calculation: http://stackoverflow.com/a/3413529/3287359

##Libraries

 - argparse
 - sys
 - math

 All of these should be included in a standard Python environment.

##Version
This project was developed on Python 3.6.0
