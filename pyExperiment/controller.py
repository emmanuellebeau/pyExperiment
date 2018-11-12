from psychopy import core
import sys, logging, os


"""
This is a standard controller environment for experiments
"""

class EEGLogging():
    def __init__(self):
        pass
        """
        Todo:
            fix connection for sending triggers
        """

class PupilLogging():
    def __init__(self):
        pass
        """
        Todo:
            fix connection for messages to eyelink
        """

def createFolderHierarchy(folders):
    p = os.path.normpath(folders)
    p = p.split(os.sep)
    paths = p[0]
    for i in range(len(paths)):
        if not os.path.isdir(paths):
            os.mkdir(paths)
        if i < len(p)-1:
            paths = os.path.join(paths, p[i+1])

def getSubjectInfo(experiment_name='my name', n_sessions=2, n_runs=2):
    # info = gui.GetSubjectInfo(experiment_name)
    # return info.info
    subject_data = {}
    print(experiment_name)
    subject_data['subject_id'] = input('sub: ')
    subject_data['age'] = int(input('age: '))
    subject_data['run'] = int(input('run: '))
    subject_data['session'] = int(input('session: '))
    return subject_data

    """
    For some reason, psychopy crashes if I get my info using their GUI
    """
    # myDlg = gui.Dlg(title=f"{experiment_name} experiment")
    # myDlg.addText('Subject info')
    # myDlg.addField('Subject ID:', 'sub-')
    # myDlg.addField('Age:')
    # myDlg.addText('Experiment Info')
    # myDlg.addField('Session:', choices=list(range(1, n_sessions+1)))
    # myDlg.addField('Run:', choices=list(range(1, n_runs+1)))
    # ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
    #
    # if myDlg.OK:  # or if ok_data is not None
    #     myDlg.close()
    #     subject_data = {'subject_id': ok_data[0],
    #                     'age':ok_data[1],
    #                     'session':ok_data[2],
    #                     'run':ok_data[3]}
    #     return subject_data
    # else:
    #     sys.exit('User cancelled!')



class Controller(EEGLogging, PupilLogging):
    """
    Parent class for any type of experiment. Your experiment class needs a
    runTrial-method that will be called from this parent class.

    Automatic initialization of logging events
    and fetching subject information.

    Parameters:
        name: str
            name of the experiment
        n_sessions: int
        n_runs: int
    Todo:
        * TODO - a lot
    """
    def __init__(self, name='my_experiment', n_sessions=2, n_runs=8):
        self.experiment_name = name
        self.n_sessions = n_sessions
        self.n_runs = n_runs
        subject_info = getSubjectInfo(name, n_sessions, n_runs)
        self.subject_id = subject_info['subject_id']
        self.age = subject_info['age']
        self.session = subject_info['session']
        self.run = subject_info['run']
        self.logger = self._initLogger()
        self.block = 1
        self.trial = 1
        self.trials = []
        self.win = False
        self.run_start = core.Clock()

        start_str = f'Starting {self.experiment_name} - subject - '\
                    f'{self.subject_id} - age - {self.age} - run - '\
                    f'{self.run} - session - {self.session}'
        self.log(start_str)


    def _initLogger(self):
        """
        Setups the logger used by the experiment
        """
        
        createFolderHierarchy(os.path.join('tasks','logs',f'{self.experiment_name}'))
        logname = os.path.join('tasks','logs',f'{self.experiment_name}',f'sub-{self.subject_id}_task-{self.experiment_name}_ses-{self.session:02d}_run-{self.run:02d}_log.log')

        LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filename=logname, level=20, format=LOG_FORMAT)

        return logging.getLogger()


    def log(self, text):
        """
        Todo
            add EEG and eyelink logging
        """
        self.logger.info(text)


    def start(self, run_before=False, run_after=False):
        """
        parameters
            runBefore / runAfter: list [(function, dict of parameters)]
                can be specific functions to run before/after looping over
                the trials. For example, a function that displays information
                regarding the experiment or other.
        """
        if run_before:
            for f, para in run_before:
                f(**para)

        # loop over trials
        self.log(f'Start of block - {self.block}')
        self.block_start = core.Clock()
        for this_trial in self.trials:
            self.runTrial(this_trial)
            self.trial += 1

        if run_after:
            for f, para in run_after:
                f(**para)

        log_str = f'End of block - {self.block} - '\
                  f'block duration - {self.block_start.getTime()}'
        self.log(log_str)
        self.block += 1
        # should we save the trial list as a pkl?
        self.clearTrials()

    def addTrial(self, tp):
        self.trials.append(tp)

    def clearTrials(self):
        self.trials = []
