import sys
import os
import datetime
from util.util import Util
from system.state_machine import StateMachine
from util.beeper import Beeper
from psychopy import event
from abc import ABCMeta, abstractmethod


class Task:
    """
    Task abstract class.
    """

    __metaclass__ = ABCMeta

    def __init__(self, config_file):
        self.config = {}
        if config_file is not None:
            if not os.path.exists(config_file):
                sys.exit('config file path %s does not exist'%config_file)
            self.config = Util.load_config(config_file)
        self.stim_colors = self.get_stim_colors()
        self.state_machine = StateMachine(self.config, self.stim_colors)
        self.task_name = self.set_task_name()
        self.stim_contrasts = self.calibrate_stim()
        self.state_machine.set_stim_contrasts(self.stim_contrasts)
        self.audio_volume = self.state_machine.audio_volume
        self.audio_ms = self.state_machine.audio_ms
        self.save_location = self.state_machine.save_location
        self.save_file = None
        self.quit_task = False
        self.trial_num = 0
        self.beeper = Beeper(volume=self.audio_volume, duration=self.audio_ms / 1000.)

    def write_trial_data(self, trial_data):
        if self.save_file is not None:
            self.save_file.write(str(trial_data) + "\n")

    @abstractmethod
    def set_task_name(self):
        raise NotImplementedError('subclasses must override set_task_name()!')

    @abstractmethod
    def calibrate_stim(self):
        raise NotImplementedError('subclasses must override calibrate_stim()!')

    @abstractmethod
    def get_stim_colors(self):
        raise NotImplementedError('subclesses must override get_stim_colors()!')

    @abstractmethod
    def experiment_step(self):
        raise NotImplementedError('subclassees must override experiment_step()!')

    def cleanup(self):
        if self.save_file is not None:
            self.save_file.close()
            self.save_file = None
        self.state_machine.reset()
        self.quit_task = False
        self.trial_num = 0

    def run(self):
        self.cleanup()
        start_time = datetime.datetime.now().strftime('%Y%m%d:%H%M%S')
        save_file_path = os.path.join(self.save_location, start_time)
        if not os.path.exists(self.save_location):
            os.makedirs(self.save_location)
        self.save_file = open(save_file_path, "w")
        self.state_machine.params['start_time'] = start_time
        params = self.state_machine.params
        params['task_name'] = self.task_name
        self.save_file.write('params: ' + str(params) + "\n")
        while self.state_machine.trial_number < self.state_machine.num_conditions and not self.quit_task:
            all_keys = event.getKeys()
            # quit task if q is pushed.
            if 'q' in all_keys:
                self.quit_task = True
                break
            self.trial_num += 1
            trial_data = self.experiment_step()
            self.write_trial_data(trial_data)
        self.cleanup()
