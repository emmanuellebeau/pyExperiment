from psychopy.visual import ImageStim, RadialStim, GratingStim
from psychopy import visual, event, core
import matplotlib.pyplot as plt
import os
import numpy as np
from numpy.random import choice as rchoice

"""
TODO:
    fix monitor
    fix dialogue box for getting responses
"""
def create_run_trials(cond_dict, n_blocks, n_reps):
    """
    cond_dict:  dictionary describing name of the cond and how many levels
                exempel: {'Lag': 3, 'Similarity': 2}
    n_blocks:   int
                number of blocks
    n_reps:     int
                number of total repetitions of each level
    Returns a dict of blocks comprising of
    a list with dicts, each dict correspond to a trial describing
    which level it should be for each condition

    Example:
    block_dict =  {'Block 0': [
                  {'Lag': 2, 'Similarity': 1},
                  {'Lag': 1, 'Similarity': 0},
                  {'Lag': 2, 'Similarity': 0},
                  {'Lag': 2, 'Similarity': 1},
                  {'Lag': 1, 'Similarity': 0}],

                 'Block 1': [
                  {'Lag': 0, 'Similarity': 0},
                  {'Lag': 0, 'Similarity': 1},
                  {'Lag': 1, 'Similarity': 1},
                  {'Lag': 0, 'Similarity': 1},
                  {'Lag': 1, 'Similarity': 1}]}
    """
    conds = list(cond_dict.keys())
    n_conds = len(conds)
    # total amount of trials
    tot_trials = np.prod(list(cond_dict.values()))*n_reps

    assert tot_trials % n_blocks == 0, \
            'Total number of trials most be possible to spread equally across blocks.'\
            '\nTotal amount of trials: {0}\nNumber of blocks: {1}'.format(
            tot_trials,n_blocks)
    trials_per_block = tot_trials // n_blocks

    level_list = [np.arange(x) for x in cond_dict.values()]

    # Create trials
    trial_list = []
    for _ in range(n_reps):
        for trial in itertools.product(*level_list):
            trial_list.append({conds[x]: trial[x] for x in range(n_conds)})

    # in place shuffle trials
    np.random.shuffle(trial_list)

    # divide into blocks
    block_dict = {}
    for block in range(n_blocks):
        start_ind = trials_per_block * block
        end_ind = start_ind + trials_per_block
        block_dict['Block {0}'.format(block)] = trial_list[start_ind:end_ind]

    return block_dict

def load_images(stim_folder='stim/'):
    """
    images should be numbered and named: image_xx.jpg
    """
    images = []
    for im in range(1, 41):
        path = os.path.join(stim_folder, f'image_{im:02d}.jpg')
        img = plt.imread(path).astype(float)
        # if image is not scaled between 0-1
        if img.max() > 1:
            img *= 1.0/255.0
        images.append(img)
    return images

def getCorrectResponse(opt, t, keys):
    return keys[list(opt).index(t)]

def loadInfoTxt(directory=None,file='instructions.txt'):
    b = ''        
    if directory is not None:
        with open(os.path.join(directory,file), 'r') as f:
            for line in f.readlines():
                b += line + '\n'        
    else:
        with open(file, 'r') as f:
            for line in f.readlines():
                b += line + '\n'
    return b


def createImageMasks(images, n_masks, size=10):
    """
    Takes a list of images and makes masks by dividing a mask into squares
    and randomly sample from the pool of images
    Parameters:
        images: list of np.array images
        n_masks: int
            number of masks
        size: int
            size of square
    """
    n_images = len(images)
    img_size = images[0].shape

    if not img_size[0] == img_size[1]:
        raise ValueError('Images need to be square')
    if not (img_size[0]/size).is_integer():
        raise ValueError(f'{img_size[0]} not dividable with {size}')

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

def createRadialMasks(win, n_masks):
    """
    Creates radial masks with random orientation
    """
    masks = []
    for i in range(n_masks):
        mask = RadialStim(win, mask='gauss', size=6, radialCycles=5,
                         angularCycles=5, ori=np.random.randint(360),
                         name='mask')
        masks.append(mask)
    return masks

def createRSVP(win, T1, T2, t1_pos, t2_pos,
               images, masks, RSVP_len, im_size):
    # Create trial_sequence
    bgcolor = [0.5, 0.5, 0.5]
    n_masks = len(masks)
    trial_sequence = [rchoice(range(n_masks)) for x in range(RSVP_len)]
    trial_sequence = [ImageStim(win, masks[x], name=f'Mask {x}', color=bgcolor,
                      size=im_size, flipVert=True) for x in trial_sequence]
    # convert to ImageStims
    # pick a random T1 and T2

    trial_sequence[t1_pos] = ImageStim(win, images[T1], name=f'T1 {T1}', color=bgcolor,
                                       size=im_size,  flipVert=True)
    trial_sequence[t2_pos] = ImageStim(win, images[T2], name=f'T2 {T2}', color=bgcolor,
                                       size=im_size,  flipVert=True)
    return trial_sequence
    
def define_pairs(n_images, lags):
    
    n_reps = 4 #multiply the number of images by this value to have your total number of pairs
    trial_pairs = []
    
    for j in range(n_images):
        pool = np.setdiff1d(range(n_images), j)
        choices = np.random.choice(pool, n_reps, replace=False)
        pairs = np.asarray([(j, x) for x in choices])
        trial_pairs.append(pairs)

    trial_pairs = np.vstack(trial_pairs)

    all_lags = [
        np.c_[
            trial_pairs,
            np.tile(x, n_images*n_reps)] for x in lags]

    all_lags = np.vstack(all_lags)
    
    
    return all_lags
