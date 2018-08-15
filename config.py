# CHANGE THIS FIELD OR IT WON'T WORK WITH HIGH PROBABILITY
# what's your screen's name?
SCREEN_NAME = 'eDP-1'

ENV_RECALL_FACTOR = 0.8

# max and min brightness ratio
MIN_BRIGHTNESS_RATIO = 0.2
MAX_BRIGHTNESS_RATIO = 1.0

# every <delay> seconds, the code takes image and screen shot
PERIOD = 0.1
SMOOTH_ADJUSTMENT_N_STEPS = 10
SMOOTH_ADJUSTMENT_PERIOD = 0.1

DARKNESS_LEVEL = 0.5


def get_new_adjustment_ratio(env, scr):
    ratio = (env['mean'] + env['std']) / (scr['mean'] + DARKNESS_LEVEL * scr['std'])

    ratio = max(ratio, MIN_BRIGHTNESS_RATIO)
    ratio = min(ratio, MAX_BRIGHTNESS_RATIO)

    return ratio
