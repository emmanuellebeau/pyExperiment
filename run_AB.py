from psychopy.visual import ImageStim #import some libraries from PsychoPy
from psychopy import visual, event, core
import matplotlib.pyplot as plt
import os
import numpy as np
from experiments import *
from numpy.random import choice as rchoice

"""
TODO:
    fix monitor
    fix dialogue box for getting responses
"""

def load_images():
    STIM_FOLDER = 'stim/'
    images = []
    for im in range(1, 41):
        path = os.path.join(STIM_FOLDER, f'image_{im:02d}.jpg')
        img = plt.imread(path).astype(float)
        # if image is not scaled between 0-1
        if img.max() > 1:
            img *= 1.0/255.0
        images.append(img)
    return images

def loadInfoTxt():
    b = ''
    with open('instructions.txt', 'r') as f:
        for line in f.readlines():
            b += line + '\n'
    return b

def createMasks(images, n_masks, size=10):
    """
    Takes a list of images and makes masks
    """
    n_images = len(images)
    img_size = images[0].shape

    assert img_size[0] == img_size[1], 'Images need to be square'
    assert (img_size[0]/size).is_integer(), f'{img_size[0]} not dividable with {size}'

    n_boxes = int(img_size[0]/size)

    masks = []
    for i in range(n_masks):
        mask = np.zeros(img_size)
        row = 0
        for i in range(n_boxes):
            col = 0
            for j in range(n_boxes):
                img_idx = rchoice(range(n_images), 1)[0]
                img = images[img_idx]
                box = img[row:row+size, col:col+size, :]
                mask[row:row+size, col:col+size, :] = box
                col += size
            row += size
        masks.append(mask)
    return masks

def createTrialSequence(AB, T1, T2, t1_pos, t2_pos, images, masks, n_masks, RSVP_len, im_size):
    # Create trial_sequence
    bgcolor = [0.5, 0.5, 0.5]
    trial_sequence = [rchoice(range(n_masks)) for x in range(RSVP_len)]
    trial_sequence = [ImageStim(AB.win, masks[x], name=f'Mask {x}', color=bgcolor,
                      size=im_size, flipVert=True) for x in trial_sequence]
    # convert to ImageStims
    # pick a random T1 and T2

    trial_sequence[t1_pos] = ImageStim(AB.win, images[T1], name=f'T1 {T1}', color=bgcolor,
                                       size=im_size,  flipVert=True)
    trial_sequence[t2_pos] = ImageStim(AB.win, images[T2], name=f'T2 {T2}', color=bgcolor,
                                       size=im_size,  flipVert=True)
    return trial_sequence

# load images
images = load_images()
info_txt = loadInfoTxt()
n_images = len(images)
n_trials = 3
t1_pos = 5
t2_pos = 7
RSVP_len = 12
n_masks = 20
im_size = 5 # in degrees
n_blocks = 2

#AB = AB(n_sessions=2, n_runs=1)
AB = AB(name='AB')
AB.initTrialLog()
print('initated AB')
win = visual.Window([800,600], monitor="testMonitor", units="deg")
AB.win = win
# generate trials


trial_dict = {
            'trial sequence':None, # list of named psychopy objects to draw
            'fixation time': 0.5,
            'imgdur': 0.02,
            'SOA': 0.1,
            'T1': None,
            'T2': None,
            'T1 options': None,
            'T2 options': None,
            'T1 menu': None,
            'T2 menu': None,
            'T1 responses': None, # possible key responses
            'T2 responses': None, # possible key responses
            'T1 correct response': None,
            'T2 correct response': None
            }

for block in range(n_blocks):
    if block == 0:
        # if the first block, show instructions
        info_message = visual.TextStim(win, text=info_txt, pos=(0, 0), height=0.5)
        params = {'obj_list': [info_message], 'responses': ['space']}
        AB.drawAndWait(**params)
    
    masks = createMasks(images, n_masks)
    for i in range(n_trials):
        T1 = rchoice(range(n_images), 1)[0]
        T2 = rchoice(range(n_images), 1)[0]
        trial_sequence = createTrialSequence(AB, T1, T2, t1_pos, t2_pos, images,
                                             masks, n_masks, RSVP_len, im_size)
        # Make menu options
        possible_menu_options = np.setdiff1d(range(n_images), [T1, T2])
        T1_opt = np.append(rchoice(possible_menu_options, 1), T1)
        np.random.shuffle(T1_opt)

        T2_opt = np.append(rchoice(possible_menu_options, 1), T2)
        np.random.shuffle(T2_opt)

        # create image instances for menu
        pos = ([-4, 0], [4, 0])
        menu_txt = visual.TextStim(win, text='Which one was the first target', pos=(0, 4), height=0.5)
        menu_txt2 = visual.TextStim(win, text='Which one was the second target', pos=(0, 4), height=0.5)
        T1_menu = [ImageStim(AB.win, images[x], name=f'T1 menu {x}',
                             size=im_size, pos=pos[i],  flipVert=True) for i, x in enumerate(T1_opt)]
        T1_menu.append(menu_txt)
        T2_menu = [ImageStim(AB.win, images[x], name=f'T2 menu {x}',
                             size=im_size, pos=pos[i],  flipVert=True) for i, x in enumerate(T2_opt)]
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
        trial_dict['T1 responses'] = ['z', 'm']
        trial_dict['T2 responses'] = ['z', 'm']
        if T1_opt[0] == T1:
            trial_dict['T1 correct response'] = 'z'
        else:
            trial_dict['T1 correct response'] = 'm'

        if T2_opt[0] == T2:
            trial_dict['T2 correct response'] = 'z'
        else:
            trial_dict['T2 correct response'] = 'm'
        AB.addTrial(trial_dict.copy())

    if block == n_blocks-1:
        block_txt = f'End of run {AB.run}\npress space to continue'
        info_message = visual.TextStim(win, text=block_txt, pos=(0, 0), height=0.5)
    else:
        print('this block', block)
        block_txt = f'End of block {block+1}/{n_blocks}\nPress space to continue'
        info_message = visual.TextStim(win, text=block_txt, pos=(0, 0), height=0.5)
    params = {'obj_list': [info_message], 'responses': ['space']}
    AB.start(run_after=[(AB.drawAndWait, params)])
