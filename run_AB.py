from psychopy.visual import ImageStim #import some libraries from PsychoPy
from psychopy import visual, event, core
import matplotlib.pyplot as plt
import os
import numpy as np
from numpy.random import choice as rchoice
from experiments import *
import runUtils as RU

"""
TODO:
    fix monitor
    fix dialogue box for getting responses
"""

# load images
images = RU.load_images()
info_txt = RU.loadInfoTxt()
n_images = len(images)
# define trial settings
fix_time = 0.5
img_dur = 0.02
SOA = 0.1
n_trials = 10
t1_pos = 5
t2_pos = 7
RSVP_len = 12
n_masks = 20
im_size = 5 # in degrees
n_blocks = 2
max_response_time = 2.5
"""
Keys should be in order for your response menu
the first key corresponds to the first alternative in the menu
here z corresponds to the left object, and m to the right in the menu
"""
keys = ['z', 'm']
# initiate
ab = AB(name='AB', distance_to_screen=100)

# generate trials
trial_dict = {
            'trial sequence':None, # list of named psychopy objects to draw
            'fixation time': fix_time,
            'imgdur': img_dur,
            'SOA': SOA,
            'max response time': max_response_time,
            'T1': None, # T1 identifier
            'T2': None, # T2 identifier
            'T1 options': None, # list of keys
            'T2 options': None, # list of keys
            'T1 menu': None, # list of drawable objects shown as alternatives
            'T2 menu': None, # list of drawable objects shown as alternatives
            'Response keys': keys, # possible key responses
            'T1 correct response': None, # correct key response for T1
            'T2 correct response': None  # correct key response for T2
            }

for block in range(n_blocks):
    if block == 0:
        # if the first block, show instructions
        info_message = visual.TextStim(ab.win, text=info_txt,
                                       pos=(0, 0), height=0.5)
        params = {'obj_list': [info_message], 'responses': ['space']}
        ab.drawAndWait(**params)

    masks = RU.createImageMasks(images, n_masks)
    for i in range(n_trials):
        progressBar(ab.win, i, n_trials,
                    load_txt=f'Loading trials for block {block+1}')
        # Pick targets and create RSVP sequence
        T1 = rchoice(range(n_images), 1)[0]
        T2 = rchoice(range(n_images), 1)[0]
        trial_sequence = RU.createRSVP(ab.win, T1, T2, t1_pos, t2_pos, images,
                                       masks, n_masks, RSVP_len, im_size)
        # Make menu options
        possible_menu_options = np.setdiff1d(range(n_images), [T1, T2])
        T1_opt = np.append(rchoice(possible_menu_options, 1), T1)
        np.random.shuffle(T1_opt)

        T2_opt = np.append(rchoice(possible_menu_options, 1), T2)
        np.random.shuffle(T2_opt)

        # create image instances for menu
        pos = ([-4, 0], [4, 0])
        menu_txt = visual.TextStim(ab.win,
                text='Which one was the first target', pos=(0, 4), height=0.5)
        menu_txt2 = visual.TextStim(ab.win,
                text='Which one was the second target', pos=(0, 4), height=0.5)
        T1_menu = [ImageStim(ab.win, images[x], name=f'T1 menu {x}',
                             size=im_size, pos=pos[i],  flipVert=True)
                             for i, x in enumerate(T1_opt)]
        T1_menu.append(menu_txt)
        T2_menu = [ImageStim(ab.win, images[x], name=f'T2 menu {x}',
                             size=im_size, pos=pos[i],  flipVert=True)
                             for i, x in enumerate(T2_opt)]
        T2_menu.append(menu_txt2)
        # Add specifics to trial_dict

        trial_dict['trial sequence'] = trial_sequence
        trial_dict['trial type'] = 'lag 2'
        trial_dict['T1'] = T1
        trial_dict['T2'] = T2
        trial_dict['T1 options'] = T1_opt
        trial_dict['T2 options'] = T2_opt
        trial_dict['T1 menu'] = T1_menu
        trial_dict['T2 menu'] = T2_menu
        trial_dict['T1 correct response'] = RU.getCorrectResponse(T1_opt,
                                                                  T1, keys)
        trial_dict['T2 correct response'] = RU.getCorrectResponse(T2_opt,
                                                                  T2, keys)
        ab.addTrial(trial_dict.copy())

    if block == n_blocks-1: # if last block
        block_txt = f'End of run {ab.run}\npress space to continue'
        info_message = visual.TextStim(ab.win, text=block_txt,
                                       pos=(0, 0), height=0.5)
    else:
        block_txt = f'End of block {block+1}/{n_blocks}\n'\
                     f'Press space to continue'
        info_message = visual.TextStim(ab.win, text=block_txt,
                                       pos=(0, 0), height=0.5)
    params = {'obj_list': [info_message], 'responses': ['space']}
    ab.start(run_after=[(ab.drawAndWait, params)])
