# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 18:48:17 2020

@author: WK5521

add simple parser for arguments to define parameters from command line
includes flags:
    -v for velocity
    -aoa for angle of attack
    -c for case name
    

"""

  
import sys
import argparse
print (sys.argv)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("-c", "--casename", dest = "casename", default = "case1",
                    help="Case name", nargs = '+')
parser.add_argument("-aoa", "--angleofattack",dest = "aoa", default = '0',
                    help="Angle of attack", nargs = '+')
parser.add_argument("-v", "--velocity",dest = "v", default = '0',
                    help="Velocity", nargs = '+')

args = parser.parse_args()
try:
    aoas = list(map(float, args.aoa))
except TypeError:
    pass
try:
    vs = list(map(float, args.v))
except TypeError:
    pass
try:
    casesnames = args.casename
except TypeError:
    pass
print(f'aoas: {aoas}')
print(f'vs: {vs}')
print(f'casenames: {args.casename}')





