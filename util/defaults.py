from util import Util


def load_params(config):
    """
    Load the parameters with defaults..
    :param config: The config dictionary.
    :return: The params.
    """
    params = {}
    params['timeout_ms'] = int(Util.get_param(config, 'timeout_ms', 2000))
    params['grid_size'] = int(Util.get_param(config, 'grid_size', 3))
    params['x_size'] = int(Util.get_param(config, 'x_size', 25))
    params['y_size'] = int(Util.get_param(config, 'y_size', 15))
    params['stimulus_radius'] = float(Util.get_param(config, 'stimulus_radius', .5))
    params['fixation_cross_size'] = float(Util.get_param(config, 'fixation_cross_size', 1))
    params['prob_catch_trial'] = float(Util.get_param(config, 'prob_catch_trial', 0.1))
    params['n_trials_per_location'] = int(Util.get_param(config, 'n_trials_per_location', 10))
    params['isi_ms'] = [int(c) for c in Util.get_param_list(config, 'isi_ms', [200, 300])]
    params['presentation_time'] = [int(c) for c in Util.get_param_list(config, 'presentation_time', [100, 200, 300])]
    params['distance_from_screen'] = int(Util.get_param(config, 'distance_from_screen', 50))
    params['participant_id'] = Util.get_param(config, 'participant_id', 'test')
    params['experiment_notes'] = Util.get_param(config, 'experiment_notes', 'No Notes Given')
    params['save_location'] = Util.get_param(config, 'save_location', 'data').strip()
    params['screen_number'] = int(Util.get_param(config, 'screen_number', 1))
    params['screen_x'] = int(Util.get_param(config, 'screen_x', 1920))
    params['screen_y'] = int(Util.get_param(config, 'screen_y', 1080))
    params['monitor_width'] = float(Util.get_param(config, 'monitor_width', 52.7))
    params['monitor_pixels_x'] = int(Util.get_param(config, 'monitor_pixels_x', 1920))
    params['monitor_pixels_y'] = int(Util.get_param(config, 'monitor_pixels_y', 1080))
    params['screen_rgb'] = [int(c) for c in Util.get_param(config, 'screen_rgb', "0, 0, 0").split(",")]
    params['audio_volume'] = float(Util.get_param(config, 'audio_volume', 0.1))
    params['audio_ms'] = int(Util.get_param(config, 'audio_ms', 500))
    return params
