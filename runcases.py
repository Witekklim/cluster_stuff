"""
this is master script making use of scheme-generating scripts and running case names as defined in command line arguments

example use:

python3 runcases.py case1 case2 case3


to do:
- merge funcitonality with parser.py to allow multiple flags, hence exteded command line arguments option
"""


from schemegen import scheme3d, qsubgen
import os
import sys

cases = sys.argv[1:]

print('cases considered: {}'.format(cases))
for case in cases:
	for alpha in range(-2,8,2):
		case_i = '{},{}'.format(case,alpha)
		print(case_i)
		scheme3d('scheme_{}.jou'.format(case_i), alpha, 30, case_i, case, "/home/WK5521/Documents/mesh_study/mesh2/")
		qsubgen("/home/WK5521/Documents/mesh_study/mesh2/que_{}.pbs".format(case_i), "/home/WK5521/Documents/mesh_study/mesh2/scheme_{}.jou".format(case_i), "/home/WK5521/Documents/mesh_study/mesh2/output_{}.txt".format(case_i) , 1)
		command = 'qsub que_{}.pbs'.format(case_i)	
		os.system(command)
