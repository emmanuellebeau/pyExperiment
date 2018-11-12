from functools import partial
from pyExperiment.utils import wait_secs, clock

class Keyboard(object):
    """Retrieve presses from various devices.

    Public metohds:
        __init__
        listen_presses
        get_presses
        wait_one_press
        wait_for_presses
        check_force_quit

    Methods to override by subclasses:
        _get_timebase
        _clear_events
        _retrieve_events
    """
    key_event_types = {'presses': ['press'], 'releases': ['release'],
                       'both': ['press', 'release']}

    def __init__(self, ec, force_quit_keys):
        self.master_clock = ec._master_clock
        self.log_presses = ec._log_presses
        self.force_quit_keys = force_quit_keys
        self.listen_start = None
        ec._time_correction_fxns['keypress'] = self._get_timebase
        self.get_time_corr = partial(ec._get_time_correction, 'keypress')
        self.time_correction = self.get_time_corr()
        self.win = ec._win
        # always init pyglet response handler for error (and non-error) keys
        self.win.on_key_press = self._on_pyglet_keypress
        self.win.on_key_release = self._on_pyglet_keyrelease
        self._keyboard_buffer = []

    ###########################################################################
    # Methods to be overridden by subclasses
    def _clear_events(self):
        self._clear_keyboard_events()

    def _retrieve_events(self, live_keys, kind='presses'):
        return self._retrieve_keyboard_events(live_keys, kind)

    def _get_timebase(self):
        """Get keyboard time reference (in seconds)
        """
        return clock()

    def _clear_keyboard_events(self):
        self.win.dispatch_events()
        self._keyboard_buffer = []

    def _retrieve_keyboard_events(self, live_keys, kind='presses'):
        # add escape keys
        if live_keys is not None:
            live_keys = [str(x) for x in live_keys]  # accept ints
            live_keys.extend(self.force_quit_keys)
        self.win.dispatch_events()  # pump events on pyglet windows
        targets = []

        for key in self._keyboard_buffer:
            if key[2] in self.key_event_types[kind]:
                if live_keys is None or key[0] in live_keys:
                    targets.append(key)
        return targets

    def _on_pyglet_keypress(self, symbol, modifiers, emulated=False,
                            isPress=True):
        """Handler for on_key_press pyglet events"""
        key_time = clock()
        if emulated:
            this_key = str(symbol)
        else:
            from pyglet.window import key
            this_key = key.symbol_string(symbol).lower()
            this_key = this_key.lstrip('_').lstrip('NUM_')
        press_or_release = {True: 'press', False: 'release'}[isPress]
        self._keyboard_buffer.append((this_key, key_time, press_or_release))

    def _on_pyglet_keyrelease(self, symbol, modifiers, emulated=False):
        self._on_pyglet_keypress(symbol, modifiers, emulated=emulated,
                                 isPress=False)

    def listen_presses(self):
        """Start listening for keypresses."""
        self.time_correction = self.get_time_corr()
        self.listen_start = self.master_clock()
        self._clear_events()

    def get_presses(self, live_keys, timestamp, relative_to, kind='presses',
                    return_kinds=False):
        """Get the current entire keyboard / button box buffer."""
        if kind not in self.key_event_types.keys():
            raise ValueError('Kind argument must be one of: '+', '.join(
                             self.key_event_types.keys()))
        events = []
        if timestamp and relative_to is None:
            if self.listen_start is None:
                raise ValueError('I cannot timestamp: relative_to is None and '
                                 'you have not yet called listen_presses.')
            relative_to = self.listen_start
        events = self._retrieve_events(live_keys, kind)
        events = self._correct_presses(events, timestamp, relative_to, kind)
        events = [e[:-1] for e in events] if not return_kinds else events
        return events

    def wait_one_press(self, max_wait, min_wait, live_keys, timestamp,
                       relative_to):
        """Return the first button pressed after min_wait."""
        relative_to, start_time = self._init_wait_press(
            max_wait, min_wait, live_keys, relative_to)
        pressed = []
        while (not len(pressed) and
               self.master_clock() - start_time < max_wait):
            pressed = self._retrieve_events(live_keys)

        # handle non-presses
        if len(pressed):
            pressed = self._correct_presses(pressed, timestamp, relative_to)
            pressed = pressed[0][:2] if timestamp else pressed[0][0]
        else:
            pressed = (None, None) if timestamp else None
        return pressed

    def wait_for_presses(self, max_wait, min_wait, live_keys,
                         timestamp, relative_to):
        """Return all button presses between min_wait and max_wait."""
        relative_to, start_time = self._init_wait_press(
            max_wait, min_wait, live_keys, relative_to)
        pressed = []
        while (self.master_clock() - start_time < max_wait):
            pressed = self._retrieve_events(live_keys)
        pressed = self._correct_presses(pressed, timestamp, relative_to)
        pressed = [p[:2] if timestamp else p[0] for p in pressed]
        return pressed

    def check_force_quit(self, keys=None):
        """Compare key buffer to list of force-quit keys and quit if matched.

        This function always uses the keyboard, so is part of abstraction.
        """
        if keys is None:
            # only grab the force-quit keys
            keys = self._retrieve_keyboard_events([])
        else:
            if isinstance(keys, string_types):
                keys = [keys]
            if isinstance(keys, list):
                keys = [k for k in keys if k in self.force_quit_keys]
            else:
                raise TypeError('Force quit checking requires a string or '
                                ' list of strings, not a {}.'
                                ''.format(type(keys)))
        if len(keys):
            raise RuntimeError('Quit key pressed')

    def _correct_presses(self, events, timestamp, relative_to, kind='presses'):
        """Correct timing of presses and check for quit press."""
        events = [(k, s + self.time_correction, r) for k, s, r in events]
        self.log_presses(events)
        keys = [k[0] for k in events]
        self.check_force_quit(keys)
        events = [e for e in events if e[2] in self.key_event_types[kind]]
        if timestamp:
            events = [(k, s - relative_to, t) for (k, s, t) in events]
        else:
            events = [(k, t) for (k, s, t) in events]
        return events

    def _init_wait_press(self, max_wait, min_wait, live_keys, relative_to):
        """Prepare for ``wait_one_press`` and ``wait_for_presses``."""
        if np.isinf(max_wait) and live_keys == []:
            raise ValueError('max_wait cannot be infinite if there are no live'
                             ' keys.')
        if not min_wait <= max_wait:
            raise ValueError('min_wait must be less than max_wait')
        start_time = self.master_clock()
        relative_to = start_time if relative_to is None else relative_to
        wait_secs(min_wait)
        self.check_force_quit()
        self._clear_events()
        return relative_to, start_time