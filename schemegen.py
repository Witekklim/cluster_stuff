import math as m
def scheme3d(filename, alpha, v, casename, meshname, path, savecase = False):
    x_comp = m.cos(m.radians(alpha))
    y_comp = m.sin(m.radians(alpha))
	
    with open(filename, 'w') as f:
        f.write('file/read-case "{}{}.msh"\n'.format(path,meshname))
        f.write('/mesh/scale 1 1 1\n')
        f.write('/define/models/steady\n')
        f.write('/define/models/solver/pressure-based y\n')
        f.write('/define/models/viscous/kw-sst y\n')
        f.write('/define/models/energy y n n n y\n')
        f.write('/define/materials/change-create air air y ideal-gas n n y constant 1.78e-05 n n n\n')
        f.write('/define/boundary-conditions/modify-zones/zone-type wing wall\n')
        f.write('/define/boundary-conditions/modify-zones/zone-type te wall\n')
        f.write('/define/boundary-conditions/modify-zones/zone-type inlet velocity-inlet\n')
        f.write('/define/boundary-conditions/modify-zones/zone-type interior--fluid interior\n')
        f.write('/define/boundary-conditions/modify-zones/zone-type symmetry symmetry\n')
        f.write('/define/boundary-conditions/modify-zones/zone-type outlet pressure-outlet\n')
        
        f.write('/define/boundary-conditions/velocity-inlet inlet y y n {} n 0 y n {} n 0 n {} n 300 n n y 5 10\n'.format(v, x_comp, y_comp))
        
        f.write('/report/reference-values/compute velocity-inlet inlet\n')
        f.write('/report/reference-values/area 1.8\n')
        f.write('/report/reference-values/length 0.6\n')
        f.write('/solve/set/p-v-coupling 24\n')
        f.write('/solve/set/discretization-scheme k 1\n')
        f.write('/solve/set/discretization-scheme omega 1\n')
        
        f.write('/solve/report-definitions/add lift lift force-vector {} 0 {} thread wing te () q\n'.format(-y_comp, x_comp))
        f.write('/solve/report-definitions/add drag drag force-vector {} 0 {} thread wing te () q\n'.format(x_comp, y_comp))
        
        f.write('/solve/monitors/residual convergence-criteria 1e-8 1e-4 1e-4 1e-4 1e-4 1e-4 1e-4\n')
        f.write('/solve/report-files add report report-defs lift drag () q\n')
        f.write('/solve/report-files/edit/report file-name "{}/reports/{}.out" q \n'.format(path, casename))
        
        f.write('/solve/initialize/hyb-initialization\n')
        f.write('/solve/iterate 500\n')
        if savecase:
            f.write('/file/write-case-data "{}{}.cas"\n'.format(path, casename))
        f.write('exit y\n')

# =========================================================================
def qsubgen(filename, scheme, console_output, nodes = 1, jobname = 'CDQ'):
	""" all: filename, scheme and console_output need full path with extension   """
	with open(filename, 'w') as f:
		f.write('#!/bin/tcsh\n')
		f.write('#PBS -N {}\n'.format(jobname))
		f.write('#PBS -l nodes={}:ppn=20\n'.format(nodes))
		f.write('#PBS -l walltime=57:12:43\n')
		f.write('#PBS -r n\n')
		f.write('#PBS -o $PBS_O_WORKDIR\n')

		f.write('echo Job started\n')
		f.write('echo "  " at `date`\n')
		f.write('echo "  " on host `hostname`\n')
		f.write('echo "  " working directory is $PBS_O_WORKDIR\n')
		f.write('echo "  " will run on `cat < $PBS_NODEFILE`\n')

		f.write('tty\n')

		f.write('cd $PBS_O_WORKDIR/\n')

		f.write('/home/opt/ansys192/v192/fluent/bin/fluent 3ddp -g -t{} -cnf=$PBS_NODEFILE -i {} > {}\n'.format(nodes*20,scheme, console_output))

		f.write('echo Job finished at `date`\n')


if __name__=='__main__':        
	scheme3d('scheme.jou', 5, 30, 'case1', "/home/WK5521/Documents/mesh_study/mesh2/")
	qsubgen("/home/WK5521/Documents/mesh_study/mesh2/que.pbs", "/home/WK5521/Documents/mesh_study/mesh2/case1.jou", "/home/WK5521/Documents/mesh_study/mesh2/output_case1.txt",2)
          
