# brightness adjuster
change screen brightness according to environment light level

## What's the purpose of this project? 
Very bright screen in dim places, and dim screen in bright places. These combinations tire eyes. This project aims to automatically adjust your screen brightness to environment brightness, like what cell phones do. 

## How does it work? 
Every 0.1 second, it takes an image from the environment with your webcam and a screenshot. Then it computes two numbers for each image; average and standard deviation of pixels brightness. Then it computes the following factor: 

<p align='center'>
<a href="https://www.codecogs.com/eqnedit.php?latex=ratio&space;=&space;\frac{avg_{env}&space;&plus;&space;std_{env}}{avg_{scr}&space;&plus;&space;2&space;\times&space;std_{scr}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?ratio&space;=&space;\frac{avg_{env}&space;&plus;&space;std_{env}}{avg_{scr}&space;&plus;&space;2&space;\times&space;std_{scr}}" title="ratio = \frac{avg_{env} + std_{env}}{avg_{scr} + 2 \times std_{scr}}" /></a>
</p>

And finally, it changes the screen brightness to this factor. 

## What on earth is that ratio formula? 
I had intended to find the best formula by considering biological experiments on eyes and different screen hardware, but that requires a lot of research and I simply didn't have enough free time. So, I just implemented the first idea that came to my mind. 

That formula is meant to find the ratio that adjusts 97% of the screen pixels brightness to 80% of the environment pixels brightness. Assuming that the pixels brightness of the screen and the environment form two Gaussian distributions, which is obviously a completely wrong assumption :), about 80% of the pixels have a brightness below mean+std, and 97% below mean+2*std. 

## features
1. **smooth brightness change**: just like cell phones 

2. **ignoring short sudden environment changes**: Short sudden changes in the environment can make short sudden changes in screen brightness, but this code can ignore these changes and only respond to real changes in the environment. 

## How can you use it? 
1. **supported OSes: Linux, Mac(maybe)** </br>
I used `xrandr` terminal command for changing the screen brightness. Wherever that works, my code works too. 

2. **requirements**: numpy, imageio, pyscreenshot </br>
requirements installation: `bash ui.sh install`

3. **Find your screen name** </br>
If code said `output eDP-1-1 not found`, you need to change "eDP-1-1", which is an input for `xrandr` that refers to the screen you want to change its brightness. For listing your screens names, type `xrandr--output` in the terminal and click TAB twice; autocomplete will list all your screens. Notice that `xrandr` can control your VGA and HDMI output too. 

4. **Don't use your webcam while it's running** </br>
Only one process can use the webcam at a time. If you try to connect to a webcam with another application is using it, either the new or the old application will lose its connection. So you can't use this code while you're on a video chat. 

5. **You can use your own formula** </br> 
Don't you like the result of my formula? Change it to whatever you like. You only need to change the `get_adjustment_ratio` method. If you need more than just mean and std, you can change the `get_env_brightness_info` and `get_scr_brightness_info` methods. 

6. **start it with `bash ui.sh on` and stop it with `bash ui.sh off`** </br>
You can also make `ui.sh` executable by running `chmod +x ui.sh` and then use it like this: `ui.sh on` and `ui.sh off` </br> 
Also, you can create a link/shortcut of `ui.sh` in a folder in your system's PATH, like `/usr/bin/`, and use this command like a normal terminal command. 


## Known issues: 
1. high CPU usage: it uses almost 10% of my CPU. About 7% is spent waiting for screenshots and 4% for taking images with the webcam.

2. a better formula: I'm mostly satisfied with the result of my formula, but sometimes I feel it could work better, for example by taking into account the time of the day which determines that the viewer is tired after a long workday or he/she has just woke up and is full of energy. 
