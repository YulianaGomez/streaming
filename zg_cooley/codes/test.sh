#!/bin/sh

APP=/home/yzamora/streaming/zg_cooley/codes/end-point-attach.py

MV2_ENABLE_AFFINITY=0 MV2_CPU_BINDING_LEVEL=socket mpirun -f $COBALT_NODEFILE -ppn 1 $APP 
