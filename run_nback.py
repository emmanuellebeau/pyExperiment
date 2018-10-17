from psychopy import visual, event, core
from psychopy.visual import ImageStim
import os
import numpy as np
from numpy.random import choice as rchoice
from experiments import *
import runUtils as RU

"""
TODO:
    fix monitor
    fix dialogue box for getting responses

You exit the experiment by pressing q

"""

# define trial settings
img_dur = 0.5
im_size = 8 # in degrees
n_blocks = 2
max_response_time = 1.5
trial_length  = 2

"""
Response options:
here z corresponds to Yes, and m to No
"""
keys = ['z', 'm']
trial_dict = {
            'target image':None, # list of named psychopy objects to draw
            'img duration': img_dur,
            'trial length': trial_length,
            'max response time': max_response_time,
            'correct response': None , # correct key response
            'possible responses': ['z', 'm'] # yes and no
            }

# initiate AB class
nback = NBackExperiment(distance_to_screen=200, name='n_back')

"""
Preload images and the masks turn them into textures
"""
info_txt = RU.loadInfoTxt('instructions_nback.txt')

# Load images
images = RU.load_AB_images()
n_images = len(images)

img_textures = []
for i in range(n_images):
    progressBar(nback.win, i, n_images,
                load_txt=f'Loading images')
    img_textures.append(ImageStim(nback.win, images[i], name=f'{i}',
                                  size=im_size,  flipVert=True))

# Start looping over blocks
for block in range(n_blocks):
    if block == 0:
        # if the first block, show instructions
        info_message = visual.TextStim(nback.win, text=info_txt,
                                       pos=(0, 0), height=0.5)
        params = {'obj_list': [info_message], 'responses': ['space']}
        nback.drawAndWait(**params)

    # Make a list of numbers representing which order each image will be
    # presented in. For simplicity I'm just gonna present image of the
    # 40 images 3 times per block, and shuffle it

    trial_order = np.repeat(range(n_images),3)
    n_trials = len(trial_order)
    np.random.shuffle(trial_order)
    # lets randomly add a few n_backs
    for i in range(20):
        randt = np.random.choice(range(1, n_trials),1)[0]
        trial_order[randt] = trial_order[randt-1]

    # Create all the trials for the block
    for i in range(n_trials):
        # Add specifics to trial_dict
        trial_dict['target image'] = img_textures[trial_order[i]]
        # first trial can't be n-back
        if i == 0:
            trial_dict['n back'] = False
            trial_dict['correct response'] = 'm'
        else:
            # if this image is the same as previous trial
            if trial_order[i] == trial_order[i-1]:
                trial_dict['n back'] = True
                trial_dict['correct response'] = 'z'
            else:
                trial_dict['n back'] = False
                trial_dict['correct response'] = 'm'

        nback.addTrial(trial_dict.copy())

    if block == n_blocks-1: # if last block
        block_txt = f'End of run {nback.run}\nPress space to continue'
        info_message = visual.TextStim(nback.win, text=block_txt,
                                       pos=(0, 0), height=0.5)
    else:
        block_txt = f'End of block {block+1}/{n_blocks}\n'\
                    f'Press space to continue'
        info_message = visual.TextStim(nback.win, text=block_txt,
                                       pos=(0, 0), height=0.5)
    params = {'obj_list': [info_message], 'responses': ['space']}
    nback.start(run_after=[(nback.drawAndWait, params)])
