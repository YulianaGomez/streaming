#!/soft/libraries/anaconda/bin/python

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

print(rank)
cd ~/home/yzamora/globusconnectpersonal-2.3.3
./globusconnectpersonal -start -dir /home/yzamora/globusconnectpersonal-2.3.3/globus_config/ep0$rank
