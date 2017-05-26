#! /usr/bin/env python

import numpy as np
import h5py as h5
import sys
import math
import time

if len(sys.argv)!=9:
  print "Usage: python " + sys.argv[0] + " <number-of-projections> <number-of-rows> <number-of-columns> <degree-range> <time-interval> <number-of-files> <output-file> <prefix>"
  exit(0)


nproj = int(sys.argv[1])
nrows = int(sys.argv[2])
ncols = int(sys.argv[3])
degree = int(sys.argv[4])
interval = float(sys.argv[5])
nfiles = int(sys.argv[6])
if nfiles < 1: nfiles = 10  # Default value for the nfile is 10
prefix = sys.argv[8]
output_f = sys.argv[7]

if nproj%nfiles!=0 : 
  print "#proj/#files should be int"
  exit(0)

nprojstep = nproj/nfiles
degreestep = degree/nfiles*1.

start = time.time()

for i in range(0,nfiles):
  fpath = output_f + "/" + prefix + "-" + str(i) + ".h5"
  print "Generating file: " + fpath
  time.sleep(interval) #  Note that this does not consider data generation and I/O, thus is lower-bound for the elapsed time

  ntheta = np.linspace(i*degreestep, i*degreestep+degreestep, nprojstep, endpoint=False, dtype="float32")
  pdata = np.random.random_sample((nprojstep, nrows, ncols))
  pdata = np.array(pdata, dtype='f')

  ofptr = h5.File(fpath, 'w')
  ofptr.create_group('exchange')
  ofptr.create_dataset('exchange/theta', data=ntheta)
  ofptr.create_dataset('exchange/data', data=pdata)

  ofptr.close()

ttime = time.time()-start
total_size_mb = 4*nfiles*nprojstep*nrows*ncols/(1024*1024.)

print "Total dataset size=" + str(total_size_mb) + "; Elapsed time=" + str(ttime) + "; Average file generation rate=" + str(ttime/nfiles) + " files/sec (" + str(total_size_mb/ttime) + "MB/sec)"
