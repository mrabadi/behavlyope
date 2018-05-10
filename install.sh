conda update conda 
conda update anaconda
conda update conda
conda update anaconda
conda config --add channels https://conda.binstar.org/erik
conda install -c erik psychopy
conda create -n behavlyope psychopy
source activate behavlyope 
conda install -c conda-forge pyglet
source deactivate behavlyope

