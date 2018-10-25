import util

def load_params(config):
    params = {}
    params['timeout_ms'] = int(util.get_param(config, 'timeout_ms', 2000))
    params['grid_size'] = int(util.get_param(config, 'grid_size', 3))
    params['x_size'] = int(util.get_param(config, 'x_size', 9))
    params['y_size'] = int(util.get_param(config, 'y_size', 9))
    params['stimulus_radius'] = float(util.get_param(config, 'stimulus_radius', .5))
    params['fixation_cross_size'] = float(util.get_param(config, 'fixation_cross_size', 1))
    params['prob_catch_trial'] = float(util.get_param(config, 'prob_catch_trial', 0.1))
    params['n_trials_per_location'] = int(util.get_param(config, 'n_trials_per_location', 10))
    params['isi_ms'] = util.get_param_list(config, 'isi_ms', [200, 300])
    params['presentation_time'] = util.get_param_list(config, 'presentation_time', [100, 200, 300])

    # TODO: distance_from_screen not yet used.
    params['distance_from_screen'] = util.get_param(config, 'distance_from_screen', 3)
    params['participant_id'] = util.get_param(config, 'participant_id', 'test')
    params['experiment_notes'] = util.get_param(config, 'experiment_notes', 'No Notes Given')
    params['save_location'] = util.get_param(config, 'save_location', 'data')
    return params

