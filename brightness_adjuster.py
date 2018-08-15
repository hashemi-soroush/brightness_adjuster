#!/usr/bin/python3

import os
import re
import time
import numpy as np
import imageio
import pyscreenshot
import subprocess

from config import *

env_info_history = None


def get_env_info():
    global env_info_history
    while True:
        try:
            env_reader = imageio.get_reader('<video0>')
            env_im = env_reader.get_next_data()

            mean = env_im.mean()
            std = env_im.std()

            env_reader.close()

            if env_info_history is None:
                env_info_history = {
                    'mean': mean,
                    'std': std
                }
            else:
                env_info_history = {
                    'mean': ENV_RECALL_FACTOR * env_info_history['mean'] + (1 - ENV_RECALL_FACTOR) * mean,
                    'std': ENV_RECALL_FACTOR * env_info_history['std'] + (1 - ENV_RECALL_FACTOR) * std
                }
            return env_info_history
        except:
            pass


def get_scr_info():
    scr_im = pyscreenshot.grab()

    scr_im = np.array(scr_im)

    scr_info = {
        'mean': scr_im.mean(),
        'std': scr_im.std()
    }
    return scr_info


def get_cur_ratio():
    p = subprocess.Popen(['xrandr', '--verbose'], stdout=subprocess.PIPE)
    cur_status = p.stdout.read().decode('utf-8')

    cur_ratio = re.findall('brightness\s*:\s*(\d\.\d+)\s', cur_status.lower())
    if len(cur_ratio) == 0:
        raise Exception("Can't read current brightness ratio from xrandr")
    cur_ratio = float(cur_ratio[0])
    return cur_ratio


def adjust_screen_brightness(target_ratio):
    target_ratio = round(target_ratio, 1)

    cur_ratio = get_cur_ratio()

    if cur_ratio is None:
        os.system('xrandr --output {0} --brightness {1}'.format(SCREEN_NAME, target_ratio))
        return

    for i in range(SMOOTH_ADJUSTMENT_N_STEPS):
        new_ratio = cur_ratio + (i + 1.) / SMOOTH_ADJUSTMENT_N_STEPS * (target_ratio - cur_ratio)
        os.system('xrandr --output {0} --brightness {1}'.format(SCREEN_NAME, new_ratio))
        time.sleep(SMOOTH_ADJUSTMENT_PERIOD / SMOOTH_ADJUSTMENT_N_STEPS)


def main():
    while True:
        env = get_env_info()
        scr = get_scr_info()
        ratio = get_new_adjustment_ratio(env, scr)
        adjust_screen_brightness(ratio)
        time.sleep(PERIOD)


if __name__ == '__main__':
    main()
