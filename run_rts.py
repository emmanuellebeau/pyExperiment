from psychopy import visual, event, core
from psychopy.visual import ImageStim
import os
import numpy as np
from numpy.random import choice as rchoice
from numpy.random import random
from experiments import *
import runUtils as RU

"""
TODO:
    fix monitor
    fix dialogue box for getting responses

You exit the experiment by pressing q

"""

# define trial settings
img_dur = 0.1
im_size = 8 # in degrees
n_blocks = 2
max_response_time = 1.5
trial_length  = 2
keys = ['z', 'm']

"""
Response options:
here z corresponds to Category 1, and m to Category 2
"""
trial_dict = {
            'target image':None, # list of named psychopy objects to draw
            'img duration': img_dur,
            'trial length': trial_length,
            'max response time': max_response_time,
            'correct response': None , # correct key response
            'possible responses': keys # yes
            }

# initiate RTs class
exp = RTs(distance_to_screen=200, name='rts')

"""
Load the instructions and images 
"""
info_txt = RU.loadInfoTxt('instructions_rts.txt')

# Load images
images = RU.load_images()
n_images = len(images)

# define a vector with length len(images) that specifies categoryLabels
class_1_idn = range(20)#...

img_textures = []
for i in range(n_images):
    progressBar(exp.win, i, n_images,
                load_txt=f'Loading images')
    img_textures.append(ImageStim(exp.win, images[i], name=f'{i}',
                                  size=im_size,  flipVert=True))

# Start looping over blocks
for block in range(n_blocks):
    if block == 0:
        # if the first block, show instructions
        info_message = visual.TextStim(exp.win, text=info_txt,
                                       pos=(0, 0), height=0.5)
        params = {'class_obj': exp, 'obj_list': [info_message], 'responses': ['space']}
        drawAndWait(**params)

    # Make a list of numbers representing which order each image will be
    # presented in. For simplicity I'm just gonna present each image of the
    # 40 images 3 times per block, and shuffle it

    trial_order = np.repeat(range(n_images),3)
    n_trials = len(trial_order)
    np.random.shuffle(trial_order)

    print(f'######\n######\n trial order: \n {trial_order} \n######\n######\n')

    # Create all the trials for the block
    for i in trial_order.astype(int):
        # Add specifics to trial_dict
        trial_dict['target image'] = img_textures[i]
        trial_dict['image ID'] = i
        
        if i in class_1_idn:
	        trial_dict['category'] = 'z'
        else:
	        trial_dict['category'] = 'm'        

        # add some jitter and update trial_dict
        jitter = random() * (0 - 0.5) + 0.5  # generate a number between 0 and 0.5
        jitISI = round(jitter, 1)

        trial_dict['trial length'] = trial_length - jitISI

        exp.addTrial(trial_dict.copy())

    if block == n_blocks-1: # if last block
        block_txt = f'End of run {exp.run}\nPress space to continue'
        info_message = visual.TextStim(exp.win, text=block_txt,
                                       pos=(0, 0), height=0.5)
    else:
        block_txt = f'End of block {block+1}/{n_blocks}\n'\
                    f'Press space to continue'
        info_message = visual.TextStim(exp.win, text=block_txt,
                                       pos=(0, 0), height=0.5)
    params = {'class_obj': exp, 'obj_list': [info_message], 'responses': ['space']}
    exp.start(run_after=[(drawAndWait, params)])
