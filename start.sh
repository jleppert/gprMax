#!/bin/bash

export PATH=$PATH:$CUDA_HOME/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64
export CUDA_HOME=/usr/local/cuda
export QT_AUTO_SCREEN_SCALE_FACTOR=0
conda activate gprMax-devel

# GPU_DEVICE_ID=0 python ./user_models/rover_xy_scan_sim.py <name>
# GPU_DEVICE_ID=1 python ./user_models/rover_xy_scan_sim.py <name>
# GPU_DEVICE_ID=2 python ./user_models/rover_xy_scan_sim.py <name>

# python -m tools.plot_Ascan ./user_models/rover_sim_1645528962/rover_xy_scan_sim-x0-y0.h5 --outputs Ey --outputs Ey
# python -m tools.outputfiles_merge ./user_models/rover_sim_1645528962/rover_xy_scan_sim-x
# python -m tools.plot_Bscan ./user_models/rover_sim_1645528962/rover_xy_scan_sim-x_merged.h5 Ey
