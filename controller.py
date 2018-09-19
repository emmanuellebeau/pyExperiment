from psychopy import gui, visual, event, core
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

class Experiment(EEGLogging, PupilLogging):
    def __init__(self, name='my_experiment', n_sessions=2, n_runs=8):
        """
        Parent class for any type of experiment. Your experiment class needs a
        runTrial-method that will be called from this parent class. Your
        experimental class also need a trials attribute, which is a list
        of dictionaries containing the specific trial parameters that will
        be sent to the runTrial method.

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
        self.experiment_name = name
        self.n_sessions = n_sessions
        self.n_runs = n_runs
        self.subject_info = self.subjectInfo()
        if not self.subject_info:
            sys.exit('User cancelled!')
        self.subject_id = self.subject_info[0]
        self.age = self.subject_info[1]
        self.session = self.subject_info[2]
        self.run = self.subject_info[3]
        self.logger = self._initLogger()
        self.trial = 1
        self.run_start = core.Clock()

        start_str = f'Starting {self.experiment_name} for subject '\
                    f'{self.subject_id} age {self.age} session '\
                    f'{self.session} run {self.run}'
        self.log(start_str)


    def subjectInfo(self):
        myDlg = gui.Dlg(title=f"{self.experiment_name} experiment")
        myDlg.addText('Subject info')
        myDlg.addField('Subject ID:', 'sub-')
        myDlg.addField('Age:')
        myDlg.addText('Experiment Info')
        myDlg.addField('Session:', choices=list(range(1, self.n_sessions+1)))
        myDlg.addField('Run:', choices=list(range(1, self.n_runs+1)))
        ok_data = myDlg.show()  # show dialog and wait for OK or Cancel

        if myDlg.OK:  # or if ok_data is not None
            return ok_data
        else:
            return False


    def _initLogger(self):
        """
        Setups the logger used by the experiment
        """
        if not os.path.exists('logs'):
            os.mkdir('logs')
        logname = f'logs/{self.subject_id}_task-{self.experiment_name}_'\
                  f'ses-{self.session:02d}_run-{self.run:02d}_log.log'

        LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
        logging.basicConfig(filename=logname,
                            level=10, format=LOG_FORMAT)

        return logging.getLogger()

    def log(self, text, level='info'):
        """
        Todo
            add EEG and eyelink logging
        """
        if level=='info':
            self.logger.info(text)
        elif level=='warning':
            self.logger.warning(text)
        elif level=='error':
            self.logger.error(text)

    def start(self, runBefore=False, runAfter=False):
        """
        parameters
            runBefore / runAfter: list [(function, dict of parameters)]
                can be specific functions to run before/after looping over
                the trials. For example, a function that displays information
                regarding the experiment or other.
        """
        if runBefore:
            for f, para in runBefore:
                f(**para)

        # loop over trials
        self.log(f'Start of block - {self.block}')
        self.block_start = core.Clock()
        for this_trial in self.trials:
            self.runTrial(this_trial)
            self.trial += 1

        if runAfter:
            for f, para in runAfter:
                f(**para)

        log_str = f'End of block - {self.block} - '\
                  f'block duration - {self.block_start.getTime()}'
        self.log(log_str)
        self.block += 1
        # should we save the trial list as a pkl?
        self.clearTrials()
