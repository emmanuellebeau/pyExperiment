from psychopy import gui, visual, event, core
import numpy as np
import sys, logging, os
from pyExperiment.controller import *
from pyExperiment.utils import shutdown, get_keypress, drawAndWait, initTrialLog, progressBar
from psychopy import logging
logging.console.setLevel(logging.CRITICAL)

class bareBoneExperiment(Controller):
    """
    Bare minimum of attributes and methods needed to be compatible with
    the Experiment-class
    """
    def __init__(self, **args):
        super().__init__(**args)

    def runTrials():
        pass

class RTs(Controller):
    """
    Todo:
        Very simple class enabling the collection of reaction times when
        perceiving visual images
    """
    def __init__(self, distance_to_screen=60, monitor='testMonitor',
                 fullscr=True, **args):
        super(RTs, self).__init__(**args)
        self.win = visual.Window([1024,768], fullscr=fullscr, screen=1,
                                 monitor=monitor, units="deg")
        self.win.mouseVisible = False
        self.secs_per_frame = 1/self.win.getActualFrameRate()

        # setup trial log
        folder = os.path.join('tasks','results','RTs')
        createFolderHierarchy(folder)
        log_name = f'sub-{self.subject_id}_task-'\
                   f'{self.experiment_name}_ses-{self.session:02d}_'\
                   f'run-{self.run:02d}_events.tsv'
        self.trial_log_name = os.path.join(folder, log_name)
        header = ['Subject', 'Category', 'Session', 'run', 'Trial', 'Image','Category','Onset','Duration',
                  'Response', 'RT', 'hit']
        initTrialLog(self.trial_log_name, header)


    def updateTrialLog(self, tp):
        """
        Updates the trial log used

        Notice that trial_info must follow the header defined in initTrialLog

        """
        trial_info = [self.subject_id, tp['category'], self.session,
                      self.run, self.trial, tp['image ID'], tp['category'], self.onset,self.duration, self.response,
                      self.rt, self.hit]
        trial_info = [str(x) for x in trial_info]
        with open(self.trial_log_name, 'a') as f:
            f.write('\t'.join(trial_info) + '\n')


    def formattedLog(self, msg):
        self.log(f'{msg} - trial - {self.trial} - '\
                 f'{self.trial_start.getTime()} - block - {self.block} - '\
                 f'{self.block_start.getTime()} - run - {self.run} - '\
                 f'{self.run_start.getTime()}')

    def runTrial(self, tp):
        """
        Parameters
            tp: dict
                contains fields for the following:
                        'target image':None, # list of named psychopy objects to draw
                        'img duration' # how long to show each image
                        'trial length' # length of trial
                        'max response time' # length of response period
                        'category': # target key
                        'possible responses' # list of possible responses
        """
        # fixation object
        fixation = visual.GratingStim(win=self.win, size=0.4,
                                      pos=[0,0], sf=0, rgb=-1)
        
        stimIsOn = False
        fixIsOn  = False
        event.clearEvents()
        response_made = False
        self.response = None
        self.rt = -1
        
        # define the image id
        image_id = tp['image ID']
        
        # start trial clock
        self.trial_start = core.Clock()              
        
        while True:
            # key logger
            if not response_made and self.trial_start.getTime() < tp['max response time']:
                key = get_keypress(self)
                if key and key in tp['possible responses']:
                    self.rt = round(self.trial_start.getTime(),4)
                    self.response = key
                    response_made = True

            # if trial is over here
            if self.trial_start.getTime() > tp['trial length']:
                break

            # Only draw the image during the defined image duration
            if self.trial_start.getTime() <= tp['img duration']:                
                if not stimIsOn:
                    im = tp['target image']
                    im.setPos((0, 0))
                    im.draw()
                    # this is really where the trial start!
                     # log trial start
                    self.formattedLog('Start of trial')
                    self.formattedLog(f'Showing image {image_id}')

                    # onset
                    self.onset = round(self.run_start.getTime(),4)    
                    self.win.flip()
                    stimIsOn = True

            # otherwise draw a fixation
            else:
                if not fixIsOn:
                    fixation.draw()
                    self.duration = round(self.trial_start.getTime(),4)
                    self.win.flip()
                    fixIsOn = True
            
        self.formattedLog('End of trial')

        self.hit = tp['category'] == self.response
        
        # save trial data
        self.updateTrialLog(tp)


class AB(Controller):
    """
    Todo:
        Write this doc string
    """
    def __init__(self, distance_to_screen=60, monitor='testMonitor',
                 fullscr=True, save_video=False, **args):
        super(AB, self).__init__(**args)
        self.win = visual.Window([1024,768], fullscr=fullscr, screen=1,
                                 monitor=monitor, units="deg")
        self.win.mouseVisible = False
        self.secs_per_frame = 1/self.win.getActualFrameRate()
        self.T1_accuracy = 0
        self.save_video = save_video

        if self.save_video:
            if not os.path.exists('frames'):
                os.mkdir('frames')

        # setup trial file
        folder = 'results/AB'
        createFolderHierarchy(folder)
        log_name = f'sub-{self.subject_id}_task-'\
                   f'{self.experiment_name}_ses-{self.session:02d}_'\
                   f'run-{self.run:02d}_events.tsv'
        self.trial_log_name = os.path.join(folder, log_name)
        header = ['Subject', 'TrialType', 'Session', 'run', 'Trial', 'T1',
                  'T2', 'T1menu', 'T2menu', 'T1resp', 'T2resp',
                  'T1RT', 'T2RT', 'T1hit', 'T2hit']
        initTrialLog(self.trial_log_name, header)

    def updateTrialLog(self, tp):
        """
        Updates the trial log used
        """
        trial_info = [self.subject_id, tp['trial type'], self.session,
                      self.run, self.trial, tp['T1'], tp['T2'],
                      tp['T1 options'], tp['T2 options'], self.t1_response,
                      self.t2_response, self.t1_rt, self.t2_rt,
                      self.t1_hit, self.t2_hit]
        trial_info = [str(x) for x in trial_info]
        with open(self.trial_log_name, 'a') as f:
            f.write('\t'.join(trial_info) + '\n')


    def formattedLog(self, msg):
        self.log(f'{msg} - trial - {self.trial} - '\
                 f'{self.trial_start.getTime()} - block - {self.block} - '\
                 f'{self.block_start.getTime()} - run - {self.run} - '\
                 f'{self.run_start.getTime()}')

    def runTrial(self, tp):
        """
        Parameters
            tp: dict
                contains fields for the following:
                    trial_sequence (list of drawable objects)
                    fixation time (in secs)
                    img duration (in secs)
                    SOA (in secs)
                    T1 (int/str)
                    T2 (int/str)
                    T1 options (list of options for the menu)
                    T2 options (list of options for the menu)
                    T1 menu (list of drawable object)
                    T2 menu (list of drawable object)
                    Menu pos (list of position to draw every object in the menu lists)
                    Response keys (list of keys)
                    T1 correct respons (str)
                    T2 correct respons (str)
        Todo:
            Make sure timing is correct depending on refresh rate
        """
        # start trial clock
        self.trial_start = core.Clock()

        # log trial start
        self.formattedLog('Start of trial')

        # show fixation
        fixation = visual.GratingStim(win=self.win, size=0.4,
                                      pos=[0,0], sf=0, rgb=-1)
        fixation.draw()
        self.win.flip()
        core.wait(tp['fixation time'])


        # frames per image
        f_per_img = int(tp['img duration']/self.secs_per_frame)
        # frames per SOA
        f_SOA = int(tp['SOA']/self.secs_per_frame)
        # total frames
        n_frames = f_SOA*len(tp['trial sequence'])
        frames = np.arange(n_frames)
        img_frames = np.array([np.arange(f_per_img)+x for x in frames[::f_SOA]]).flatten()
        # lets jitter image onsets
        #img_frames = img_frames + np.random.choice([-1, 0, 1], len(img_frames))
        # begin RSVP
        i = 0
        # just to make sure we aren't sending the same log message twice
        _i = -1

        """
        # if save_video:
        #     win.getMovieFrame(buffer='back')
        #     win.saveMovieFrames(fileName=f'frames/frame_{co}.png')
        Make movie in terminal
        ffmpeg -framerate 30 -i frames/frame_%d.png -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p video/SFM_illusion.mp4
        """
        self.formattedLog('Start of RSVP')
        for frame in frames:
            if frame in img_frames:
                im = tp['trial sequence'][i]
                im.setPos((0, 0))
                im.draw()
                if _i != i:
                    self.formattedLog(f'RSVP {im.name}')
                    _i = i
            if frame in frames[f_per_img::f_SOA]:
                i += 1
            
            if self.save_video:
                self.win.getMovieFrame(buffer='back')
                self.win.saveMovieFrames(fileName=f'frames/frame_{frame}.png')
            self.win.flip()
        self.formattedLog('End of RSVP')

        # fixation before menu
        fixation.draw()
        self.win.flip()
        core.wait(0.5)

        # draw menu for T1
        timer = core.Clock()
        self.formattedLog('T1 menu')
        self.t1_response = drawAndWait(self, tp['T1 menu'],
                                            responses=tp['Response keys'],
                                            max_time=tp['max response time'],
                                            pos=tp['Menu pos'])
        self.t1_rt = timer.getTime()
        self.formattedLog(f'T1 response {self.t1_response}')

        # draw menu for T2
        timer = core.Clock()
        self.formattedLog('T2 menu')
        self.t2_response = drawAndWait(self, tp['T2 menu'],
                                            responses=tp['Response keys'],
                                            max_time=tp['max response time'],
                                            pos=tp['Menu pos'])
        self.t2_rt = timer.getTime()
        self.formattedLog(f'T2 response {self.t2_response}')

        self.t1_hit = tp['T1 correct response'] == self.t1_response
        self.t2_hit = tp['T2 correct response'] == self.t2_response

        # calculate T1 accuracy so far
        self.T1_accuracy = (self.T1_accuracy*(self.trial-1)+int(self.t1_hit))/self.trial

        # save trial data
        self.updateTrialLog(tp)
        self.formattedLog('End of trial')

class NBackExperiment(Controller):
    """
    Todo:
        Write this doc string
    """
    def __init__(self, distance_to_screen=60, monitor='testMonitor',
                 fullscr=False, **args):
        super(NBackExperiment, self).__init__(**args)
        self.win = visual.Window([1024,768], fullscr=fullscr, screen=1,
                                 monitor=monitor, units="deg")
        self.win.mouseVisible = False
        self.secs_per_frame = 1/self.win.getActualFrameRate()

        # setup trial file
        folder = os.path.join('tasks','results','nback')
        createFolderHierarchy(folder)
        log_name = f'sub-{self.subject_id}_task-'\
                   f'{self.experiment_name}_ses-{self.session:02d}_'\
                   f'run-{self.run:02d}_events.tsv'
        self.trial_log_name = os.path.join(folder, log_name)
        header = ['Subject', 'Nback', 'Session', 'run', 'Trial', 'Image', 'Onset',
                  'Response', 'RT', 'hit']
        initTrialLog(self.trial_log_name, header)

    def updateTrialLog(self, tp):
        """
        Updates the trial log used

        Notice that trial_info must follow the header defined in _initTrialLog

        """
        trial_info = [self.subject_id, tp['n back'], self.session,
                      self.run, self.trial, tp['image ID'], self.onset, self.response,
                      self.rt, self.hit]
        trial_info = [str(x) for x in trial_info]
        with open(self.trial_log_name, 'a') as f:
            f.write('\t'.join(trial_info) + '\n')

    def formattedLog(self, msg):
        self.log(f'{msg} - trial - {self.trial} - '\
                 f'{self.trial_start.getTime()} - block - {self.block} - '\
                 f'{self.block_start.getTime()} - run - {self.run} - '\
                 f'{self.run_start.getTime()}')

    def runTrial(self, tp):
        """
        Parameters
            tp: dict
                contains fields for the following:
                        'target image':None, # list of named psychopy objects to draw
                        'img duration' # how long to show each image
                        'trial length' # length of trial
                        'max response time' # length of response period
                        'correct response': # target key
                        'possible responses' # list of possible responses
        """
        # fixation object
        fixation = visual.GratingStim(win=self.win, size=0.4,
                                      pos=[0,0], sf=0, rgb=-1)

        image_id = tp['image ID']                                      
        response_made = False
        self.response = None
        self.rt = -1
        event.clearEvents()

        # start trial clock
        self.trial_start = core.Clock()
        
        self.onset = round(self.run_start.getTime(),4)
        # log trial start
        self.formattedLog('Start of trial')
        self.formattedLog(f'Showing image {image_id}')
        
        while True:
            # key logger
            if not response_made and self.trial_start.getTime() < tp['max response time']:
                key = get_keypress(self)
                if key and key in tp['possible responses']:
                    self.rt = round(self.trial_start.getTime(),4)
                    self.response = key
                    response_made = True

            # if trial is over here
            if self.trial_start.getTime() > tp['trial length']:
                break

            # Only draw the image during the defined image duration
            if self.trial_start.getTime() < tp['img duration']:
                im = tp['target image']
                im.setPos((0, 0))
                im.draw()

            # otherwise draw a fixation
            else:
                fixation.draw()
            self.win.flip()
        self.formattedLog('End of trial')

        self.hit = tp['correct response'] == self.response

        # save trial data
        self.updateTrialLog(tp)
