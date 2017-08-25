#!/usr/bin/python
"""
Simple visualizer for the location of data points in a specified range
for the IEEE 754 single-precision representation.

NOTE: Especially with ranges near 0, the density of data points can be very
high. As a rule of thumb, the closer to 0 your ranges are, the smaller those
ranges should be (both for performance and to make the resulting plots
understandable.
"""
import argparse
import math
import struct
import sys
import numpy as np
import matplotlib.pyplot as plt

def nextf(x):
    """ Get the floating point value right after x """
    if math.isnan(x) or (math.isinf(x) and x > 0):
        return x

    # Set a potentially negative 0.0 to a positive 0.0
    if x == 0.0:
        x = 0.0

    # Interpret the float as a 32-bit integer and increment/decrement
    # Note: the decrement is because a negative number becomes greater
    # by decreasing its absolute value
    n = struct.unpack('=i', struct.pack('=f', x))[0]
    if n >= 0:
        n += 1
    else:
        n -= 1
    return struct.unpack('=f', struct.pack('=i', n))[0]

def prevf(x):
    """ Get the floating point value right before x """
    return -nextf(-x)

def nextafterf(x ,y):
    """ Get the floating point value right after x, in the direction towards y """
    if math.isnan(x):
        return x
    if math.isnan(y):
        return y

    if y == x:
        return y
    elif y > x:
        return nextf(x)
    else:
        return prevf(x)

def floatrange(x, y):
    """ Get the range of floats from x to y """
    l = [x]

    z = nextafterf(x, y)
    while x < z:
        l.append(z)
        x = z
        z = nextafterf(x, y)

    return l

def barheight(x):
    frac = math.modf(x)[0]

    if frac == 0:
        return .75
    for i in range(1, 23):
        if math.modf(frac/(2**(-i)))[0] == 0:
            return 1/(i+1)

    return .03

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="""Script to display the potential values of a IEEE 754
            single-precision floats within a given range.""",
            epilog="""Written by Alex Khouderchah, 2017""")
    parser.add_argument('xMin', metavar='rangeMin', type=float,
            help='the lower bound of the provided range')
    parser.add_argument('xMax', metavar='rangeMax', type=float,
            help='the upper bound of the provided range')
    parser.add_argument('-w', '--widthFactor', type=float, default=1,
            help='a factor to scale the width of the bars')
    parser.add_argument('-n', '--noTitle', action='store_true')
    parser.add_argument('-t', '--title', default='', type=str,
            help='custom title for the generated plot')

    args = parser.parse_args()

    if args.xMin > args.xMax:
        print("The lower bound of the range cannot be greater than the upper bound!")
        sys.exit()

    x = floatrange(args.xMin, args.xMax)
    y = [barheight(x) for x in x]

    x.extend(x)
    y.extend([-y for y in y])

    xDiff = args.xMax - args.xMin

    plt.bar(x, y, xDiff * args.widthFactor / len(x))
    plt.yticks([])
    plt.xticks(np.arange(args.xMin, args.xMax, xDiff/8))
    if not args.noTitle:
        if args.title:
            plt.title(args.title, fontsize=20)
        else:
            plt.title('IEEE 754 single-precision data points in [%f, %f]' % 
                (args.xMin, args.xMax), fontsize=20)

        plt.gca().title.set_position([.5, 1.05])
    plt.show()
