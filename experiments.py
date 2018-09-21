from psychopy import gui, visual, event, core
import sys, logging, os
from controller import *
from psychopy import logging
logging.console.setLevel(logging.CRITICAL)

"""
A selection of experiment classes
"""
def shutdown(class_obj):
    print('Aborted by user!')
    class_obj.win.close()
    core.quit()

def get_keypress(class_obj):
    keys = event.getKeys()
    if keys:
        if keys[0] in ['q', 'esc']:
            shutdown(class_obj)
        return keys[0]
    else:
        return False

def progressBar(win, i, n, load_txt='Loading'):
    """
    Progress bar
    """
    load_info = visual.TextStim(win, text=load_txt, pos=(0, 1), height=0.6)
    # make progress bar
    percentage_done = i/n*100
    w = percentage_done/10
    x_pos = -4.5 + w*0.5
    progress_bar = visual.Rect(win, width=w, height=0.5,
                               pos=(x_pos, -4), fillColor="white")
    # print percentage done
    percent_text = f'{percentage_done:.2f} % done'
    percentage = visual.TextStim(win, text=percent_text,
                                 pos=(0, -1), height=0.6)
    load_info.draw()
    progress_bar.draw()
    percentage.draw()
    win.flip()

class bareBoneExperiment(Controller):
    """
    Bare minimum of attributes and methods needed to be compatible with
    the Experiment-class
    """
    def __init__(self, **args):
        super().__init__(**args)

    def runTrials():
        pass


class AB(Controller):
    """
    Todo:
        Write this doc string
    """
    def __init__(self, distance_to_screen=60, monitor='testMonitor',
                 fullscr=True, **args):
        super(AB, self).__init__(**args)
        self.win = visual.Window([1024,768], fullscr=fullscr, screen=1,
                                 monitor=monitor, units="deg")
        self.win.mouseVisible = False
        self._initTrialLog()

    def _initTrialLog(self):
        """
        A more specific log for only saving necessary
        trial by trial information
        """
        print('init trial log')
        self.trial_log_name = f'results/{self.subject_id}_task-'\
                              f'{self.experiment_name}_ses-{self.session:02d}_'\
                              f'run-{self.run:02d}_events.tsv'

        # create folder
        if not os.path.exists('results'):
            os.mkdir('results')

        # create log file
        header = ['Subject', 'TrialType', 'Session', 'run', 'Trial', 'T1',
                  'T2', 'T1menu', 'T2menu', 'T1rest', 'T2resp',
                  'T1RT', 'T2RT', 'T1hit', 'T2hit']
        with open(self.trial_log_name, 'w') as f:
            f.write('\t'.join(header) + '\n')

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

    def drawAndWait(self, obj_list, responses=[], max_time=False, pos=False):
        """
        parameters
            obj: list of psychopy object with draw method
            responses: list
                list of keywords that will exit the loop
        todo:
            add possibility of time limit
        """
        event.clearEvents()
        start = core.Clock()
        while True:
            if max_time:
                if start.getTime() > max_time:
                    return 'time out'
            key = get_keypress(self)
            if key and key in responses:
                return key
            event.clearEvents()
            for i, obj in enumerate(obj_list):
                if pos:
                    obj.setPos(pos[i])
                obj.draw()
            self.win.flip()

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

        # begin RSVP
        self.formattedLog('Start of RSVP')
        for i, im in enumerate(tp['trial sequence']):
            get_keypress(self)
            im.setPos((0, 0))
            im.draw()
            self.win.flip()
            self.formattedLog(f'RSVP {im.name}')
            core.wait(tp['img duration'])
            self.win.flip()
            core.wait(tp['SOA'])

        self.formattedLog('End of RSVP')

        # fixation before menu
        fixation.draw()
        self.win.flip()
        core.wait(0.5)

        # draw menu for T1
        timer = core.Clock()
        self.formattedLog('T1 menu')
        self.t1_response = self.drawAndWait(tp['T1 menu'],
                                            responses=tp['Response keys'],
                                            max_time=tp['max response time'],
                                            pos=tp['Menu pos'])
        self.t1_rt = timer.getTime()
        self.formattedLog(f'T1 response {self.t1_response}')

        # draw menu for T2
        timer = core.Clock()
        self.formattedLog('T2 menu')
        self.t2_response = self.drawAndWait(tp['T2 menu'],
                                            responses=tp['Response keys'],
                                            max_time=tp['max response time'],
                                            pos=tp['Menu pos'])
        self.t2_rt = timer.getTime()
        self.formattedLog(f'T2 response {self.t2_response}')

        self.t1_hit = tp['T1 correct response'] == self.t1_response
        self.t2_hit = tp['T2 correct response'] == self.t2_response

        # save trial data
        self.updateTrialLog(tp)
        self.formattedLog('End of trial')
