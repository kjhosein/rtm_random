#!/usr/bin/env python2.7
"""
Randomizes an ordered list of n numbers starting at 1.
    e.g.: [1, 2, 3, 4] may become [3, 1, 4, 2]

On MacOS, it speaks the output, pausing after each set of 3 numbers.
"""

import sys
from random import shuffle
from subprocess import call
from sys import platform


# Either accept the # as an argument or prompt the user
if len(sys.argv) == 2:
    num_items = sys.argv[1]
else:
    num_items = input("How many items in your list? ")


# Note that the use of range() here to create a list is Python2-specific.
list_of_items = range(1, int(num_items)+1)

shuffle(list_of_items)
print "\nYour randomized list is: "
print "\t", list_of_items, "\n"


# On MacOS, 'speak' the new sequence broken up into groups of 'chunk_size' (default = 3)
chunk_size = 3
if platform == "darwin":
    chunked_data = [
        list_of_items[i:i + chunk_size]
        for i in range(0, len(list_of_items), chunk_size)
    ]

    # print(chunked_data)
    print "Hit any key to continue hearing the sequence."

    for chunk in chunked_data:
        cmd = ('say {x}')
        cmd = cmd.format(x=chunk)
        call(cmd, shell=True)
        cmd = 'read -n 1 -s'
        call(cmd, shell=True)
