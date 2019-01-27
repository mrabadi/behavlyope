import sys
import os
import datetime
import time
import random
import util
from util import defaults
from psychopy import visual, core, event

COLORS = ['red', 'green', 'yellow']

config = {}
if len(sys.argv) == 2:
    config_file = sys.argv[1]
    if not os.path.exists(config_file):
        sys.exit('config file path %s does not exist'%config_file)
    config = util.load_config(config_file)

params = defaults.load_params(config)

if not os.path.exists(params['save_location']):
    os.makedirs(params['save_location'])

start_time = datetime.datetime.now().strftime('%Y%m%d.%H%M%S')
params['start_time'] = start_time

# Initialize data file writer
save_file_path = os.path.join(params['save_location'], start_time)
save_file = open(save_file_path, "w")

# Write params
save_file.write('params: ' + str(params) + '\n')

# Set up conditions
class condition(object):
    def __init__(self, x, y, color=[1,1,1]):
        self.x = x
        self.y = y
        self.color = color

conditions = []
fixation_cross_size = params['fixation_cross_size']
stimulus_radius = params['stimulus_radius']
max_x = params['x_size'] - stimulus_radius
min_x = -max_x
max_y = params['y_size'] - stimulus_radius
min_y = -max_y
grid_size = params['grid_size']

for color in COLORS:
    x = min_x
    while x <= (max_x - grid_size):
        y = min_y
        while y <= (max_y - grid_size):
            if not (-fixation_cross_size < x < fixation_cross_size or -fixation_cross_size < y < fixation_cross_size):
                for n in range(params['n_trials_per_location']):
                    conditions.append(condition(x, y, color))
            y += grid_size
        x += grid_size
random.shuffle(conditions)  # shuffle the conditions

# initialize window
# TODO: This uses the 'testMonitor' and needs to be fixed!
win = visual.Window([params['screen_x'],params['screen_y']], monitor="testMonitor", units="deg", screen=params['screen_number'], rgb=params['screen_rgb'])
fixation = visual.GratingStim(win, tex=None, mask='cross', sf=0, size=fixation_cross_size,
        name='fixation', autoLog=False)

trial_number = 0
num_conditions = len(conditions)
fixation = visual.GratingStim(win, tex=None, mask='cross', sf=0, size=1,
            name='fixation', autoLog=False)
stimulus = visual.Circle(win, radius=stimulus_radius, fillColor='white')

clock = core.Clock()
quit = False
while trial_number < num_conditions and not quit:
    trial_condition = conditions[trial_number]
    presentation_time = random.choice(params['presentation_time'])
    isi = random.choice(params['isi_ms']) / 1000.
    trial_data = {'trial_num': trial_number,
                  'x': trial_condition.x,
                  'y': trial_condition.y,
                  'color': trial_condition.color,
                  'isi': isi,
                  'presentation_time': presentation_time,
                  'catch_trial': False}
    allKeys = event.waitKeys()
    # Exit if q pushed
    if 'q' in allKeys:
        break
    
    # present fixation
    fixation.draw()
    win.flip()

    # wait isi_ms before presenting stimulus
    core.wait(isi)

    # present stimulus if not a catch trial
    present_stimulus = True
    if random.random() < params['prob_catch_trial']:
        trial_data['catch_trial'] = True
        present_stimulus = False
    else:
        trial_number += 1 # only increment trial if stimulus presented
    
    stim_start = time.time()
    response = None
    while (time.time() - stim_start) < (presentation_time / 1000.) and response is None:
        fixation.draw()
        if present_stimulus:
            stimulus.setPos([trial_condition.x, trial_condition.y])
            stimulus.lineColor = trial_condition.color
            stimulus.fillColor = trial_condition.color
            stimulus.draw()
        win.flip()
        allKeys = event.getKeys()
        if len(allKeys) > 0:
            if 'j' in allKeys:
                response = 'red'
            elif 'k' in allKeys:
                response = 'blue'
            elif 'l' in allKeys:
                response = 'purple'
            elif 'f' in allKeys:
                response = 'not_seen'
            elif 'q' in allKeys:
                response = 'quit'
                quit = True
            else:
                response = 'invalid'
        event.clearEvents()
    while (time.time() - stim_start) < (params['timeout_ms'] / 1000.) and response is None:
        fixation.draw()
        win.flip()
        allKeys = event.getKeys()
        if len(allKeys) > 0:
            if 'j' in allKeys:
                response = 'red'
            elif 'k' in allKeys:
                response = 'blue'
            elif 'l' in allKeys:
                response = 'purple'
            elif 'f' in allKeys:
                response = 'not_seen'
            elif 'q' in allKeys:
                response = 'quit'
                quit = True
            else:
                response = 'invalid'
        event.clearEvents()
    print('\a')
    fixation.draw()
    win.flip()
    trial_data['response'] = response if response is not None else 'TIMEOUT'
    event.clearEvents()
    save_file.write(str(trial_data) + '\n')

save_file.close()

