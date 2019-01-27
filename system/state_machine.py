import random
from system.condition import Condition
from util import defaults
from psychopy import visual, core, monitors


class StateMachine(object):
    """
    The Experiment State Machine.
    """

    def __init__(self, config={}):
        """
        Initialize
        :param config:
        """
        self.params = defaults.load_params(config)
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
                                 screen=self.screen_number, rgb=self.screen_rgb)
        self.fixation = visual.GratingStim(self.win, tex=None, mask='cross',
                                           sf=0, size=1, name='fixation', autoLog=False)
        self.stimulus = visual.Circle(self.win, radius=self.stimulus_radius, fillColor='white')
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

    # TODO: this depends on the task, should be a function that's passed in to method.
    def generate_conditions(self):
        conditions = []
        x = self.min_x
        while x <= self.max_x:
            y = self.min_y
            while y <= self.max_y:
                if not (-self.fixation_cross_size < x < self.fixation_cross_size or
                        -self.fixation_cross_size < y < self.fixation_cross_size):
                    for n in range(self.n_trials_per_location):
                        conditions.append(Condition(x, y))
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

    def draw_fixation(self):
        self.fixation.draw()

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
