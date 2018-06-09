#!/usr/bin/python3

import os
import time
import numpy as np
import imageio
import pyscreenshot

def get_env_brightness_info(count=1):
	mean_list, std_list = [], []
	done = False
	while not done: 
		try: 
			env_reader = imageio.get_reader('<video0>')
			for i in range(count):
				env_im = env_reader.get_next_data()
				mean_list.append(env_im.mean())
				std_list.append(env_im.std())
			env_reader.close()
			done = True
		except: 
			pass
	env_brightness_info = {
		'mean': env_im.mean(), 
		'std': env_im.std()
	}
	return env_brightness_info

def get_scr_brightness_info():
	scr_im = pyscreenshot.grab()
	scr_im = np.array(scr_im)
	scr_brightness_info = {
		'mean': scr_im.mean(), 
		'std': scr_im.std()
	}
	return scr_brightness_info

def get_adjustment_ratio(env, scr):
	ratio = (env['mean'] + env['std']) / (scr['mean'] + 2*scr['std'])
	if ratio < 0.2:
		ratio = 0.2
	if ratio > 1.:
		ratio = 1.
	return ratio

def adjust_screen_brightness(ratio):
	ratio = round(ratio, 1)
	os.system('xrandr --output eDP-1-1 --brightness {0}'.format(ratio))

def main():
	while True: 
		env = get_env_brightness_info()
		scr = get_scr_brightness_info()
		ratio = get_adjustment_ratio(env, scr)
		adjust_screen_brightness(ratio)
		time.sleep(0.2)

if __name__ == '__main__':
	main()
