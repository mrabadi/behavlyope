# behavelyope

A behavioral research engine for neuroscience research... with ambylopes.

## By Amblyopes For Amblyopes

Some say that the developer is an amblyope. He says he doesn't know.

## Installation Instructions

1. Get conda (python 2.7)
2. Run the following commands:
```bash
bash install.sh
```

Done, you now have a conda environment called `behavelyope` that has everything you need.
If you are silly enough to run components of this yourself, then you can go ahead and activate 
the conda environment with `source activate behavelyope`.  Otherwise you can use the binaries.

## Getting the behavlyope package

Download the behavlyope git repo and cd into it.

```bash
git clone https://github.com/mrabadi/behavlyope.git && cd behavlyope
```

## Running Perimetry Task

You can run the perimetry task and specify the config file. First, cd into the behavlyope directory.

```bash
bash perimetryTask -c config.txt
```

Note, you can specify your own config file.

### Perimetry Task Instructions

The participant must specify if (s)he sees or doesn't see the stimulus. 

* SPACE: participant can see stimulus.
* RETURN: participant can NOT see stimulus.
* q: quit the experiment.

## Running the Color Task

```bash
bash colorTask -c config.txt
```

### Color Task Instructions

Begin by adjusting the contrast for each stimulus color. The participant will see 
each color in sequence:
 
1. Stimulus 1: (red) participant must push left and right 
arrows until (s)he can no longer see the stimulus in right eye, then push RETURN. 
2. Stimulus 2: (green) participant must push left and right arrows until (s)he
can no longer see the stimulus in  left eye, then push RETURN.
3. Stimulus 3: (yellow) participant can just push RETURN.

The participant must specify if (s)he sees stimulus in left eye (red), right eye (green),
or both eyes (yellow):

* f: (left-hand) - (s)he can see stimulus with left eye only.
* j: (right-hand) - (s)he can see stimulus with right eye only.
* SPACE: (s)he can see stimulus with both eyes.
* RETURN: (s)he can NOT see stimulus.
* q: quit the experiment.

## Convering data to csv

You can convert the saved data into a csv file with the `convert_data.py` script.

```
python convert_data.py input_data_file_name output_file_name
```

where `input_data_file_name` is a file generated by behavelyope and `output_file_name` is where you want to save the csv version of the data.

## Visualization

You can visualize the data by simply specifying the file path.

```bash
bash visualize -f path_to_data_file -s path_to_save_directory
```
