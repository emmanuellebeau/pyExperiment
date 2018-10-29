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
"""

# define trial settings
fix_time = 0.5
img_dur = 0.02
SOA = 0.1
n_trials = 5 # per block
t1_pos = 5
t2_pos = 7
RSVP_len = 12
n_masks = 20
im_size = 8 # in degrees
n_blocks = 2
max_response_time = 2.5

"""
Keys should be in order for your response menu
the first key corresponds to the first alternative in the menu
here z corresponds to the left object, and m to the right in the menu
"""
keys = ['z', 'm']
trial_dict = {
            'trial sequence':None, # list of named psychopy objects to draw
            'fixation time': fix_time,
            'img duration': img_dur,
            'SOA': SOA,
            'max response time': max_response_time,
            'T1': None, # T1 identifier
            'T2': None, # T2 identifier
            'T1 options': None, # list of keys
            'T2 options': None, # list of keys
            'T1 menu': None, # list of drawable objects shown as alternatives
            'T2 menu': None, # list of drawable objects shown as alternatives
            # at what position to draw the menu items
            # first two are images, last position is for the text
            'Menu pos': ([-6, 0], [6, 0], [0, 6]),
            'Response keys': keys, # possible key responses
            'T1 correct response': None, # correct key response for T1
            'T2 correct response': None  # correct key response for T2
            }

# initiate AB class
ab = AB(distance_to_screen=200, name='AB')

"""
Preload images and the masks turn them into textures
"""
info_txt = RU.loadInfoTxt('instructions.txt')

# Load images
images = RU.load_images()
n_images = len(images)

img_textures = []
for i in range(n_images):
    progressBar(ab.win, i, n_images,
                load_txt=f'Loading images')
    img_textures.append(ImageStim(ab.win, images[i], name=f'{i}',
                                  size=im_size,  flipVert=True))
# load masks
masks = RU.createImageMasks(images, n_masks, 25)
mask_textures = []
for i in range(n_masks):
    progressBar(ab.win, i, n_masks,
                load_txt=f'Loading masks')
    mask_textures.append(ImageStim(ab.win, masks[i], name=f'mask',
                                  size=im_size,  flipVert=True))
# Start looping over blocks
for block in range(n_blocks):
    if block == 0:
        # if the first block, show instructions
        info_message = visual.TextStim(ab.win, text=info_txt,
                                       pos=(0, 0), height=0.5)
        params = {'class_obj': ab, 'obj_list': [info_message], 'responses': ['space']}
        drawAndWait(**params)

    # Create all the trials for the block
    for i in range(n_trials):
        # Pick targets and create RSVP sequence
        T1 = rchoice(range(n_images), 1)[0]
        T2 = rchoice(range(n_images), 1)[0]

        # Randomly pick RSVP_len number of masks
        trial_sequence = [mask_textures[np.random.randint(n_masks)]
                                        for x in range(RSVP_len)]

        # Replace the T1 and T2 positions with the targets
        t1img = img_textures[T1]
        t1img.name = f'T1 {T1}'
        t2img = img_textures[T2]
        t2img.name = f'T2 {T2}'
        trial_sequence[t1_pos] = t1img
        trial_sequence[t2_pos] = t2img

        # Make menu options
        possible_menu_options = np.setdiff1d(range(n_images), [T1, T2])

        T1_opt = np.append(rchoice(possible_menu_options, 1), T1)
        np.random.shuffle(T1_opt)

        T2_opt = np.append(rchoice(possible_menu_options, 1), T2)
        np.random.shuffle(T2_opt)

        # create text instances for menu
        menu_txt = visual.TextStim(ab.win,
                text='Which one was the first target', height=0.7)
        menu_txt2 = visual.TextStim(ab.win,
                text='Which one was the second target', height=0.7)

        T1_menu = [img_textures[x] for i, x in enumerate(T1_opt)]
        T1_menu.append(menu_txt)

        T2_menu = [img_textures[x] for i, x in enumerate(T2_opt)]
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
    params = {'class_obj': ab, 'obj_list': [info_message], 'responses': ['space']}
    ab.start(run_after=[(drawAndWait, params)])
    ab.formattedLog(f'T1 accuracy {ab.T1_accuracy*100:.2f} % correct')
    ab.T1_accuracy = 0
