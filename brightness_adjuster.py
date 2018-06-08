#!/usr/bin/python3

import os
import time
import numpy as np
import imageio
import pyscreenshot

def get_environment_light_info(count=1):
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
	env_light_info = {
		'mean': env_im.mean(), 
		'std': env_im.std()
	}
	return env_light_info

def get_scr_light_info():
	scr_im = pyscreenshot.grab()
	scr_im = np.array(scr_im)
	scr_light_info = {
		'mean': scr_im.mean(), 
		'std': scr_im.std()
	}
	return scr_light_info

def get_adjustment_ratio(env, scr):
	ratio = max(0.25, min(1., (env['mean'] - 0.01*env['std']) / (scr['mean'] + scr['std'])))
	return ratio

def adjust_screen_light(ratio):
	ratio = round(ratio, 1)
	os.system('xrandr --output eDP-1-1 --brightness {0}'.format(ratio))

def main():
	while True: 
		env = get_environment_light_info()
		scr = get_scr_light_info()
		ratio = get_adjustment_ratio(env, scr)
		adjust_screen_light(ratio)
		time.sleep(0.2)

if __name__ == '__main__':
	main()
