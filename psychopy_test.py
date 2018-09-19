from psychopy import visual, core, event #import some libraries from PsychoPy
import matplotlib.pyplot as plt
import os
#create a window


STIM_FOLDER = 'stim/'
images = []
for im in range(1, 41):
    path = os.path.join(STIM_FOLDER, f'image_{im:02d}.jpg')
    img = plt.imread(path).astype(float)
    # if image is not scaled between 0-1
    if img.max() > 1:
        img *= 1.0/255.0
    images.append(img)

win = visual.Window([800,600],monitor="testMonitor", units="deg")
im1 = visual.ImageStim(win=win, image=images[0], pos=[-4,0], size=(5,5), flipVert=True)
im2 = visual.ImageStim(win=win, image=images[5], pos=[4,0], size=(5,5), flipVert=True)
im1.draw()
im2.draw()
win.flip()

core.wait(3)
