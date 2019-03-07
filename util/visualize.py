import os
import matplotlib.pyplot as plt
import argparse
import json
import sys


def le_re_split(data):
    left_eye = []
    right_eye = []
    for d in data:
        if d["fixation_color"] == "red":
            left_eye.append(d)
        elif d["fixation_color"] == "green":
            right_eye.append(d)
    return left_eye, right_eye


def plot_rg_eye(data, x_scale, y_scale):
    hit_x = []
    hit_y = []
    wrong_x = []
    wrong_y = []
    miss_x = []
    miss_y = []
    for d in data:
        if not d["catch_trial"] and d["response"] != "invalid":
            x = d["x"] / x_scale
            y = d["y"] / y_scale
            if d["response"] == d["color"]:
                hit_x.append(x)
                hit_y.append(y)
            elif d["response"] == "TIMEOUT" or d["response"] == "not_seen":
                miss_x.append(x)
                miss_y.append(y)
            else:
                wrong_x.append(x)
                wrong_y.append(y)
    plt.tick_params(axis='both', which='both', left=False, right=False, bottom=False, top=False, labelbottom=False,
                    labelleft=False)
    plt.plot(hit_x, hit_y, linestyle='None', marker='.', markersize=10, color=d["color"]);
    plt.plot(wrong_x, wrong_y, linestyle='None', marker='.', markersize=10, color='black');
    plt.plot(miss_x, miss_y, linestyle='None', marker='.', markersize=10, color='gray');


def plot_yellow_eye(data, x_scale, y_scale):
    red_x = []
    red_y = []
    green_x = []
    green_y = []
    yellow_x = []
    yellow_y = []
    miss_x = []
    miss_y = []
    for d in data:
        if not d["catch_trial"] and d["response"] != "invalid":
            x = d["x"] / x_scale
            y = d["y"] / y_scale
            if d["response"] == "red":
                red_x.append(x)
                red_y.append(y)
            elif d["response"] == "green":
                green_x.append(x)
                green_y.append(y)
            elif d["response"] == "yellow":
                yellow_x.append(x)
                yellow_y.append(y)
            elif d["response"] == "TIMEOUT" or d["response"] == "not_seen":
                miss_x.append(x)
                miss_y.append(y)
    plt.tick_params(axis='both', which='both', left=False, right=False, bottom=False, top=False, labelbottom=False,
                    labelleft=False)
    plt.plot(red_x, red_y, linestyle='None', marker='.', markersize=10, color='red');
    plt.plot(green_x, green_y, linestyle='None', marker='.', markersize=10, color='green');
    plt.plot(yellow_x, yellow_y, linestyle='None', marker='.', markersize=10, color='yellow');
    plt.plot(miss_x, miss_y, linestyle='None', marker='.', markersize=10, color='gray');


def visualize_color_task(params, data, save_dir):
    x_scale = params["screen_x"]
    y_scale = params["screen_y"]
    red_trials = []
    green_trials = []
    yellow_trials = []
    for d in data:
        if d["color"] == "red":
            red_trials.append(d)
        elif d["color"] == "green":
            green_trials.append(d)
        elif d["color"] == "yellow":
            yellow_trials.append(d)
    ratio = float(y_scale) / float(x_scale)
    plt.figure(figsize=(20, int(10.0 * ratio * 3)))
    plt.title('color task for participant %s' % params['participant_id']);
    # red
    red_left_eye, red_right_eye = le_re_split(red_trials)
    plt.subplot(3, 2, 1);
    plot_rg_eye(red_left_eye, x_scale, y_scale)
    plt.title('Red LE');
    plt.subplot(3, 2, 2);
    plot_rg_eye(red_right_eye, x_scale, y_scale)
    plt.title('Red RE');
    # green
    green_left_eye, green_right_eye = le_re_split(green_trials)
    plt.subplot(3, 2, 3);
    plt.title('Green LE');
    plot_rg_eye(green_left_eye, x_scale, y_scale)
    plt.subplot(3, 2, 4);
    plt.title('Green RE');
    plot_rg_eye(green_right_eye, x_scale, y_scale)
    # yellow
    yellow_left_eye, yellow_right_eye = le_re_split(yellow_trials)
    plt.subplot(3, 2, 5);
    plt.title('Yellow LE')
    plot_yellow_eye(yellow_left_eye, x_scale, y_scale)
    plt.subplot(3, 2, 6);
    plt.title('Yellow RE')
    plot_yellow_eye(yellow_right_eye, x_scale, y_scale)
    plt.savefig(os.path.join(save_dir, 'color.png'))


def visualize_perimetry_task(params, data, save_dir):
    x_scale = params["screen_x"]
    y_scale = params["screen_y"]
    seen_x = []
    seen_y = []
    not_seen_x = []
    not_seen_y = []
    for d in data:
        if not d["catch_trial"] and d["response"] != "invalid":
            x = d["x"] / x_scale
            y = d["y"] / y_scale
            if d["response"] == "seen":
                seen_x.append(x)
                seen_y.append(y)
            else:
                not_seen_x.append(x)
                not_seen_y.append(y)
    ratio = float(y_scale) / float(x_scale)
    plt.figure(figsize=(10, int(10.0 * ratio)));
    plt.tick_params(axis='both', which='both', left=False, right=False, bottom=False, top=False, labelbottom=False,
                    labelleft=False)
    plt.title('perimetry task for participant %s' % params['participant_id']);
    plt.plot(seen_x, seen_y, linestyle='None', marker='.', markersize=10, color='gray');
    plt.plot(not_seen_x, not_seen_y, linestyle='None', marker='.', markersize=10, color='black');
    plt.savefig(os.path.join(save_dir, 'perimetry.png'))


def visualize(fn, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    params = None
    data = []
    with open(fn) as f:
        for line in f:
            parsed = line.strip().replace("'", '"').replace("False", "false").replace("True", "true")
            if parsed.startswith('params: '):
                parsed = parsed.replace('params: ', '')
                params = json.loads(parsed)
            else:
                data.append(json.loads(parsed))
    if params is None:
        sys.exit('nothing i can do with this file: %s' % fn)
    if params['task_name'] == 'perimetry_task':
        visualize_perimetry_task(params, data, save_dir)
    elif params['task_name'] == 'color_task':
        visualize_color_task(params, data, save_dir)
    else:
        sys.exit('task %s cannot be visualized because it is unknown' % params['task_name'])


def main():
    parser = argparse.ArgumentParser(description='The visualizer.')
    parser.add_argument('-f', '--file_name', default=None, help='The data file to use.', required=True)
    parser.add_argument('-s', '--save_path', default=None, help='Path to save files.', required=True)
    args = parser.parse_args()
    visualize(args.file_name, args.save_path)


if __name__ == "__main__":
    main()
