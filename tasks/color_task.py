import time
import sys
import argparse
from task import Task
from psychopy import event


class ColorTask(Task):
    """
    The color task.
    """

    COLOR_MAP = {'red': (1, 0, 0),
                 'green': (-1, 1, -1),
                 'yellow': (1, 1, -1)}

    def get_stim_colors(self):
        """
        Get the list of stim colors (red, green, yellow)
        :return: list of stim colors.
        """
        return ['red', 'green', 'yellow']

    def calibrate_color(self, color):
        self.state_machine.wait(.5)
        self.state_machine.flip_window()
        contrast = 1.0
        step_size = 0.05
        response = None
        while response is not 'quit' and response is not 'done':
            self.state_machine.set_stimulus_position(0, 0)
            self.state_machine.stimulus.setUseShaders(True)
            self.state_machine.stimulus.setLineColor(self.COLOR_MAP[color], colorSpace='rgb')
            self.state_machine.stimulus.setFillColor(self.COLOR_MAP[color], colorSpace='rgb')
            self.state_machine.stimulus.setContrast(contrast)
            self.state_machine.draw_stimulus()
            self.state_machine.flip_window()
            all_keys = event.getKeys()
            if len(all_keys) > 0:
                if 'right' in all_keys:
                    contrast += step_size
                elif 'left' in all_keys:
                    contrast -= step_size
                elif 'q' in all_keys:
                    response = 'quit'
                elif 'enter' in all_keys or 'return' in all_keys:
                    response = 'done'
                else:
                    response = None
            event.clearEvents()
            contrast = max(0.0, contrast)
            contrast = min(1.0, contrast)
        if response == 'quit':
            sys.exit('user quit during calibration!')
        if contrast == 0:
            sys.exit('user calibrated stimulus to 0!')
        self.state_machine.flip_window()
        self.state_machine.wait(1)
        return contrast

    def set_task_name(self):
        return 'color_task'

    def calibrate_stim(self):
        stim_contrasts = {}
        for color in self.stim_colors:
            stim_contrasts[color] = self.calibrate_color(color)
        return stim_contrasts

    def experiment_step(self):
        """
        Run one step in the experiment
        """
        trial_condition = self.state_machine.get_trial_condition()
        presentation_time = self.state_machine.get_presentation_time()
        timeout_ms = self.state_machine.get_timeout_ms()
        isi = self.state_machine.get_isi()
        trial_data = {'trial_num': self.trial_num,
                      'x': trial_condition.x,
                      'y': trial_condition.y,
                      'color': trial_condition.color,
                      'isi': isi,
                      'presentation_time': presentation_time,
                      'catch_trial': False}

        self.state_machine.draw_fixation()
        self.state_machine.flip_window()
        self.state_machine.wait(isi / 1000.)
        self.beeper.play_locking_start_tone()
        present_stimulus = True
        if self.state_machine.is_catch_trial():
            trial_data['catch_trial'] = True
            trial_data['x'] = -999
            trial_data['y'] = -999
            present_stimulus = False
        else:
            self.state_machine.increment_trial_number()

        stim_start = time.time()
        response = None
        while (time.time() - stim_start) < (presentation_time / 1000.) and response is None:
            self.state_machine.draw_fixation()
            if present_stimulus:
                self.state_machine.set_stimulus_position(trial_condition.x, trial_condition.y)
                self.state_machine.set_stimulus_color(trial_condition.color)
                self.state_machine.draw_stimulus()
            self.state_machine.flip_window()
            all_keys = event.getKeys()
            if len(all_keys) > 0:
                if 'f' in all_keys:
                    response = 'red'
                elif 'j' in all_keys:
                    response = 'green'
                elif 'space' in all_keys:
                    response = 'yellow'
                elif 'return' in all_keys or 'enter' in all_keys:
                    response = 'not_seen'
                elif 'q' in all_keys:
                    response = 'quit'
                    self.quit_task = True
                else:
                    response = 'invalid'
            event.clearEvents()

        while (time.time() - stim_start) < (timeout_ms / 1000.) and response is None and not self.quit_task:
            self.state_machine.draw_fixation()
            self.state_machine.flip_window()
            all_keys = event.getKeys()
            if len(all_keys) > 0:
                if 'f' in all_keys:
                    response = 'red'
                elif 'j' in all_keys:
                    response = 'green'
                elif 'space' in all_keys:
                    response = 'yellow'
                elif 'return' in all_keys or 'enter' in all_keys:
                    response = 'not_seen'
                elif 'q' in all_keys:
                    response = 'quit'
                    self.quit_task = True
                else:
                    response = 'invalid'
            event.clearEvents()

        end_time = time.time()
        reaction_time = int((end_time - stim_start) * 1000)
        self.beeper.play_locking_end_tone()

        self.state_machine.draw_fixation()
        self.state_machine.flip_window()
        trial_data['response'] = response if response is not None else 'TIMEOUT'
        trial_data['reaction_time'] = reaction_time if (response is not None and response is not 'quit') else -999
        event.clearEvents()
        return trial_data


def main():
    parser = argparse.ArgumentParser(description='The Color Task')
    parser.add_argument('-c', '--config_file', default=None, help='optional path to config file')
    args = parser.parse_args()
    ColorTask(config_file=args.config_file).run()


if __name__ == "__main__":
    main()
