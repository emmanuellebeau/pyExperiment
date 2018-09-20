from psychopy import gui, visual, event, core
import sys, logging, os
from controller import *
from psychopy import logging
logging.console.setLevel(logging.CRITICAL)

"""
A selection of experiment classes
"""
def shutdown(class_obj):
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


def progressBar(class_obj, i, n, load_txt='Loading'):
    """
    Progress bar
    """
    load_info = visual.TextStim(class_obj.win, text=load_txt, pos=(0, 1), height=0.6)
    # make progress bar
    percentage_done = i/n*100
    w = percentage_done/10
    x_pos = -4.5 + w*0.5
    progress_bar = visual.Rect(class_obj.win, width=w, height=0.5, pos=(x_pos, -4), fillColor="white")
    # print percentage done
    percent_text = f'{percentage_done:.2f} % done'
    percentage = visual.TextStim(class_obj.win, text=percent_text, pos=(0, -1), height=0.6)
    load_info.draw()
    progress_bar.draw()
    percentage.draw()
    class_obj.win.flip()

class bareBoneExperiment(Controller):
    """
    Bare minimum of attributes and methods needed to be compatible with
    the Experiment-class
    """
    def __init__(self, **args):
        super().__init__(**args)
        self.trials = []

    def runTrials():
        pass

    def clearTrials(self):
        self.trials = []


class AB(Controller):
    """
    Todo:
        Write this doc string
    """
    def __init_(self, **args):
        Controller().__init__(self, **args)

    def initTrialLog(self):
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
                      tp['t1_hit'], tp['t2_hit']]
        trial_info = [str(x) for x in trial_info]
        with open(self.trial_log_name, 'a') as f:
            f.write('\t'.join(trial_info) + '\n')

    def drawAndWait(self, obj_list, responses=[], max_time=False):
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
            for obj in obj_list:
                obj.draw()
            self.win.flip()

    def runTrial(self, tp):
        """
        Parameters
            tp: dict
                contains fields for the following:
                    trial_sequence (list of drawable objects)
                    fixation time (in secs)
                    imgdur (in secs)
                    SOA (in secs)
                    T1 (int/str)
                    T2 (int/str)
                    T1 options (list of options for the menu)
                    T2 options (list of options for the menu)
                    T1 menu (list of drawable object)
                    T2 menu (list of drawable object)
                    T1 responses (list of keys)
                    T2 responses (list of keys)
                    T1 correct respons (str)
                    T2 correct respons (str)
        Todo:
            Make sure timing is correct depending on refresh rate
        """
        # start trial clock
        trial_start = core.Clock()

        # log trial start
        self.log(f'Start of trial - {self.trial} - run - {self.run}  - '\
                 f'run start - {self.run_start.getTime()} - '\
                 f'run start - {self.run_start.getTime()}')

        # show fixation
        fixation = visual.GratingStim(win=self.win, size=0.4, pos=[0,0], sf=0, rgb=-1)
        fixation.draw()
        self.win.flip()
        core.wait(tp['fixation time'])

        # begin RSVP
        for i, im in enumerate(tp['trial sequence']):
            get_keypress(self)
            im.draw()
            self.win.flip()
            self.log(f'RSVP - {im.name} - trial - {self.trial} - run - '\
                     f'{self.run}  - trial start - {trial_start.getTime()}'\
                     f' - run start - {self.run_start.getTime()} - '\
                     f'run start - {self.run_start.getTime()}')
            core.wait(tp['imgdur'])
            self.win.flip()
            core.wait(tp['SOA'])

        # fixation before menu
        fixation.draw()
        self.win.flip()
        core.wait(0.5)

        # draw menu
        timer = core.Clock()
        self.log(f'T1 menu - {self.subject_id} - {self.trial} -  '\
                 f'{self.run} - {self.run_start.getTime()} - '\
                 f'{trial_start.getTime()}')
        self.t1_response = self.drawAndWait(tp['T1 menu'],
                                            responses=tp['T1 responses'],
                                            max_time=tp['max response time'])
        self.t1_rt = timer.getTime()

        timer = core.Clock()
        self.log(f'T2 menu - {self.subject_id} - {self.trial} -  '\
                 f'{self.run} - {self.run_start.getTime()} - '\
                 f'{trial_start.getTime()}')
        self.t2_response = self.drawAndWait(tp['T2 menu'],
                                            responses=tp['T2 responses'],
                                            max_time=tp['max response time'])
        self.t2_rt = timer.getTime()

        tp['t1_hit'] = tp['T1 correct response'] == self.t1_response
        tp['t2_hit'] = tp['T2 correct response'] == self.t2_response

        # save trial data
        self.updateTrialLog(tp)

        self.log(f'End of trial - {self.trial} - run - {self.run}  - '\
                 f'run start - {self.run_start.getTime()} - '\
                 f'run start - {self.run_start.getTime()}')
