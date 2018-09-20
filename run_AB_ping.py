from psychopy.visual import RadialStim, GratingStim #import some libraries from PsychoPy
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
def loadInfoTxt():
    b = ''
    with open('instructions.txt', 'r') as f:
        for line in f.readlines():
            b += line + '\n'
    return b

def createMasks(win, n_masks):
    """
    Takes a list of images and makes masks
    """
    masks = []
    for i in range(n_masks):
        mask = RadialStim(win, mask='gauss', size=6, radialCycles=5,
                         angularCycles=5, ori=np.random.randint(360), name='mask')
        masks.append(mask)
    return masks

def createTrialSequence(AB, T1, T2, t1_pos, t2_pos, masks, n_masks, RSVP_len):
    # Create trial_sequence
    bgcolor = [0.5, 0.5, 0.5]
    trial_sequence = [rchoice(range(n_masks)) for x in range(RSVP_len)]
    trial_sequence = [masks[x]for x in trial_sequence]
    # convert to ImageStims
    # pick a random T1 and T2
    trial_sequence[t1_pos] = GratingStim(AB.win,  mask='gauss', pos=(0, 0),
                             name=f'T1 {T1}', size=6, ori=T1, sf=3)
    trial_sequence[t2_pos] = GratingStim(AB.win,  mask='gauss', pos=(0, 0),
                             name=f'T2 {T2}', size=6, ori=T2, sf=3)
    return trial_sequence

# load images
info_txt = loadInfoTxt()
n_trials = 3
t1_pos = 3
t2_pos = 5
RSVP_len = 12
n_masks = 20
im_size = 5 # in degrees
n_blocks = 1
max_response_time = 2.5 # secs

#AB = AB(n_sessions=2, n_runs=1)
AB = AB(name='AB_ping')
AB.initTrialLog()
print('initated AB')
win = visual.Window([800,600], fullscr=True, monitor="testMonitor", units="deg")
AB.win = win
# generate trials

trial_dict = {
            'trial sequence':None, # list of named psychopy objects to draw
            'fixation time': 0.5,
            'imgdur': 0.02,
            'SOA': 0.1,
            'max response time': max_response_time,
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

empty = visual.GratingStim(AB.win, size=0, name='empty')
ping = RadialStim(AB.win, mask='circle', size=6, radialCycles=0,
                 angularCycles=0, color=(-1, -1, -1), name='ping')
for block in range(n_blocks):
    if block == 0:
        # if the first block, show instructions
        info_message = visual.TextStim(win, text=info_txt, pos=(0, 0), height=0.5)
        params = {'obj_list': [info_message], 'responses': ['space']}
        AB.drawAndWait(**params)
    masks = createMasks(win, n_masks)
    for i in range(n_trials):
        T1 = rchoice((45, -45), 1)[0]
        T2 = rchoice((45, -45), 1)[0]
        trial_sequence = createTrialSequence(AB, T1, T2, t1_pos, t2_pos, masks, n_masks, RSVP_len)
        addage = [empty, empty, empty, ping]
        trial_sequence.extend(addage)
        # Make menu options
        T1_opt = np.array([45, -45])
        np.random.shuffle(T1_opt)
        T2_opt = np.array([45, -45])
        np.random.shuffle(T2_opt)

        # create image instances for menu
        pos = ([-4, 0], [4, 0])
        menu_txt = visual.TextStim(win, text='Which one was the first target', pos=(0, 4), height=0.5)
        menu_txt2 = visual.TextStim(win, text='Which one was the second target', pos=(0, 4), height=0.5)

        T1_menu = [GratingStim(AB.win,  mask='gauss', pos=pos[i],
                                 name=f'Menu {x}', size=6, ori=x, sf=3) for i, x in enumerate(T1_opt)]
        T1_menu.append(menu_txt)
        T2_menu = [GratingStim(AB.win,  mask='gauss', pos=pos[i],
                                 name=f'Menu {x}', size=6, ori=x, sf=3) for i, x in enumerate(T2_opt)]
        T2_menu.append(menu_txt2)
        # Add specifics to trial_dict
        trial_dict['trial sequence'] = trial_sequence
        trial_dict['trial type'] = 'ping'
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
        block_txt = f'End of block {block+1}/{n_blocks}\nPress space to continue'
        info_message = visual.TextStim(win, text=block_txt, pos=(0, 0), height=0.5)
    params = {'obj_list': [info_message], 'responses': ['space']}
    AB.start(run_after=[(AB.drawAndWait, params)])
