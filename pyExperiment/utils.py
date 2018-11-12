from psychopy import gui, visual, event, core
import sys, logging, os

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
        if keys[0] in ['lctrl', 'rctrl']:
            shutdown(class_obj)
        return keys[0]
    else:
        return None

def drawAndWait(class_obj, obj_list, responses=[], max_time=False, pos=False):
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
        key = get_keypress(class_obj)
        if key and key in responses:
            return key
        event.clearEvents()
        for i, obj in enumerate(obj_list):
            if pos:
                obj.setPos(pos[i])
            obj.draw()
        class_obj.win.flip()

def initTrialLog(log_name, column_headers):
    """
    A more specific log for only saving necessary
    trial by trial information
    parameters:
        log_names: str
            path to log (folder hierarchy will be checked)
        column_headers: list of strings
            list of each columns header (need to be in correct order)
    """
    result_folder = os.path.dirname(log_name)
    if result_folder != '':
        assert os.path.isdir(result_folder), f'{result_folder} does not exist'

    with open(log_name, 'w') as f:
        f.write('\t'.join(column_headers) + '\n')

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