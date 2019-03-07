import random
import math
from system.condition import Condition
from util import defaults
from psychopy import visual, core, monitors


class StateMachine(object):
    """
    The Experiment State Machine.
    """

    COLOR_MAP = {'white': (1, 1, 1),
                 'red': (1, 0, 0),
                 'green': (-1, 1, -1),
                 'yellow': (1, 1, -1)}

    def __init__(self, config={}, stim_colors=['white'], fixation_colors=['white']):
        """
        Initialize
        :param config:
        """
        self.params = defaults.load_params(config)
        self.stim_colors = stim_colors
        self.fixation_colors = fixation_colors
        self.stim_contrasts = None
        self.distance_from_screen = self.params['distance_from_screen']
        self.monitor_width = self.params['monitor_width']
        self.monitor_pixels_x = self.params['monitor_pixels_x']
        self.monitor_pixels_y = self.params['monitor_pixels_y']
        self.screen_x = self.params['screen_x']
        self.screen_y = self.params['screen_y']
        self.x_half = float(self.params['x_size']) / 2.0
        self.y_half = float(self.params['y_size']) / 2.0
        self.screen_number = self.params['screen_number']
        self.screen_rgb = self.params['screen_rgb']
        self.fixation_cross_size = self.params['fixation_cross_size']
        self.stimulus_radius = self.params['stimulus_radius']
        self.stimulus_offset = self.params['stimulus_offset']
        self.max_x = self.x_half
        self.min_x = -self.max_x
        self.max_y = self.y_half
        self.min_y = -self.max_y
        self.grid_size = self.params['grid_size']
        self.n_trials_per_location = self.params['n_trials_per_location']
        # set up monitor
        self.monitor = monitors.Monitor('elo')
        self.monitor.setDistance(self.distance_from_screen)
        self.monitor.setWidth(self.monitor_width)
        self.monitor.setSizePix((self.monitor_pixels_x, self.monitor_pixels_y))
        self.conditions = self.generate_conditions()
        self.win = visual.Window((self.screen_x, self.screen_y), monitor=self.monitor, units="deg",
                                 screen=self.screen_number, color=self.screen_rgb, colorSpace='rgb')
        self.fixation = visual.GratingStim(self.win, tex=None, mask='cross',
                                           sf=0, size=1, name='fixation', autoLog=False)
        self.stimulus = visual.Circle(self.win, radius=self.stimulus_radius, fillColor=self.COLOR_MAP['white'], fillColorSpace='rgb')# fillColor='white')
        self.clock = core.Clock()
        self.trial_number = 0
        self.num_conditions = len(self.conditions)
        # set up experimental conditions
        self.presentation_time = self.params['presentation_time']
        self.isi_ms = self.params['isi_ms']
        self.prob_catch_trial = self.params['prob_catch_trial']
        self.timeout_ms = self.params['timeout_ms']
        # set up other info
        self.save_location = self.params['save_location']
        self.audio_volume = self.params['audio_volume']
        self.audio_ms = self.params['audio_ms']

    def set_stim_contrasts(self, stim_contrasts):
        self.stim_contrasts = stim_contrasts
        for color in list(self.stim_contrasts):
            self.params[color] = self.stim_contrasts[color]

    # TODO: this depends on the task, should be a function that's passed in to method.
    def generate_conditions(self):
        conditions = []
        x = self.min_x
        while x <= self.max_x:
            y = self.min_y
            while y <= self.max_y:
                if not (-self.fixation_cross_size < x < self.fixation_cross_size or
                        -self.fixation_cross_size < y < self.fixation_cross_size):
                    for color in self.stim_colors:
                        for fixation_color in self.fixation_colors:
                            v = random.uniform(0, 1) + 2 * math.pi
                            for n in range(self.n_trials_per_location):
                                theta = (2.0 * math.pi * (n + 1) / self.n_trials_per_location + v)
                                x_offset = x - self.stimulus_offset * math.cos(theta)
                                y_offset = y + self.stimulus_offset * math.sin(theta)
                                conditions.append(Condition(x_offset, y_offset, color=color, fixation_color=fixation_color))
                y += self.grid_size
            x += self.grid_size
        random.shuffle(conditions)  # shuffle the conditions
        return conditions

    @staticmethod
    def wait(ms):
        core.wait(ms)

    def is_catch_trial(self):
        if random.random() < self.prob_catch_trial:
            return True
        return False

    def get_trial_condition(self):
        return self.conditions[self.trial_number]

    def get_presentation_time(self):
        return random.choice(self.presentation_time)

    def get_timeout_ms(self):
        return self.timeout_ms

    def get_isi(self):
        return random.choice(self.isi_ms)

    def increment_trial_number(self):
        self.trial_number += 1

    def set_fixaction_color(self, color):
        self.fixation.setUseShaders(True)
        self.fixation.setContrast(self.stim_contrasts[color])
        self.fixation.setColor(color=self.COLOR_MAP[color])

    def draw_fixation(self):
        self.fixation.draw()

    def set_stimulus_color(self, color):
        self.stimulus.setUseShaders(True)
        self.stimulus.setContrast(self.stim_contrasts[color])
        self.stimulus.setLineColor(color=self.COLOR_MAP[color])
        self.stimulus.setFillColor(color=self.COLOR_MAP[color])

    def set_stimulus_position(self, x, y):
        self.stimulus.setPos((x, y))

    def draw_stimulus(self):
        self.stimulus.draw()

    def flip_window(self):
        self.win.flip()

    def reset(self):
        self.flip_window()
        self.trial_number = 0
        if 'start_time' in self.params:
            self.params.pop('start_time', None)
