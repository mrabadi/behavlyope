# behavelyope

A behavioral research engine for neuroscience research... with ambylopes.

## By Amblyopes For Amblyopes

Some say that the developer is an amblyope. He says he doesn't know.

## Installation Instructions

1. Get conda (python 2.7)
2. Run the following commands:
```bash
conda update conda 
conda update anaconda
conda config --add channels https://conda.binstar.org/erik
conda install -c erik psychopy
conda create -n behavelyope psychopy
```

Done, you now have a conda environment called `behavelyope` that has everything you need.
If you are silly enough to run components of this yourself, then you can go ahead and activate 
the conda environment with `source activate behavelyope`.  Otherwise you can use the binaries.

## Running the Experiment:

If you are happy with the defaults, then you just need to navigate to the directory that you downloaded the files are run the following:

```bash
bash behavlyope
```

## Setting Parameters in the Config File:

You can pass your own config file to behavelyope by running the following:

```bash
bash behavlyope config.txt
```

You can set your own experimental parameters in `config.txt`.

```text
isi_ms: 200, 300
timeout_ms: 500
presentation_time: 100, 200, 300
x_size: 9
y_size: 6
grid_size: 3
stimulus_radius: 1.5
fixation_cross_size: 1
prob_catch_trial: .1
n_trials_per_location: 10
distance_from_screen: 
participant_id: 
experiment_notes: put your notes and ideas here!
save_location: data
```

## DEMOS:

There are two demos for different tasks.

### Demo1:

This demo is a simple binary detection task. White dots are presented randomly on the screen. The user is expected to push 'f' for not seen and 'j' for seen (a stimulus may or may not appear on the screen).

```
bash runDemo1
```

### Demo2:

This demo is a color detection task. Red, blue, or purple dots are presented randomly on the screen. The user is expected to push 'f' for not seen, 'j' for red, 'k' for blue, and 'l' for purple. A stimulus may or may not appear on the screen.

```
bash runDemo2
```
