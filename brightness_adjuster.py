#!/usr/bin/python3

import os
import re
import time
import numpy as np
import imageio
import pyscreenshot
import subprocess

# settings: 
alpha = 0.8 # forget factor for environment image
ratio_min, ratio_max = 0.2, 1.0 
screen_name = 'eDP-1-1' # what is your screen's name?
delay = 0.1 # every <delay> seconds, this code takes image and screenshot 
smoothness_n_steps = 10
smoothness_delay = 0.1

def get_adjustment_ratio(env, scr):
	ratio = (env['mean'] + env['std']) / (scr['mean'] + 2*scr['std'])
	ratio = max(ratio, ratio_min)
	ratio = min(ratio, ratio_max)
	return ratio

env_info_history = None
def get_env_info():
	global env_info_history
	done = False
	while not done: 
		try:
			env_reader = imageio.get_reader('<video0>')
			env_im = env_reader.get_next_data()
			mean = env_im.mean()
			std = env_im.std()
			env_reader.close()
			done = True
		except:
			pass
	if env_info_history is None:
		env_info_history = {
			'mean': mean, 
			'std': std
		}
	else: 
		env_info_history = {
			'mean': alpha*env_info_history['mean'] + (1 - alpha)*mean, 
			'std': alpha*env_info_history['std'] + (1 - alpha)*std
		}
	return env_info_history

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
		return None
	cur_ratio = float(cur_ratio[0])
	return cur_ratio

def adjust_screen_brightness(ratio):
	ratio = round(ratio, 1)
	cur_ratio = get_cur_ratio()
	if cur_ratio is None:
		os.system('xrandr --output {0} --brightness {1}'.format(screen_name, ratio))
	else: 
		n_steps = smoothness_n_steps
		delay = smoothness_delay
		for i in range(n_steps):
			new_ratio = cur_ratio + (i+1.)/smoothness_n_steps*(ratio - cur_ratio)
			os.system('xrandr --output {0} --brightness {1}'.format(screen_name, new_ratio))
			time.sleep(smoothness_delay/smoothness_n_steps)

def main():
	while True: 
		env = get_env_info()
		scr = get_scr_info()
		ratio = get_adjustment_ratio(env, scr)
		adjust_screen_brightness(ratio)
		time.sleep(delay)

if __name__ == '__main__':
	main()
