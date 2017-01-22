import inspect
import time
import functools
import logging

from utils import get_last_n_levels_of_path

try:
    import settings
except:
    # mock django settings with project path
    class settings(object):
        PROJ_PATH = ''

log = logging.getLogger(__name__)
CALLER_DEPTH = 2


class Timer(object):
    """Used for timing blocks of code.

    Args:
        message (boolean): If true will log.info the message plus the delta in seconds
        print_message (boolean): If true will print the `__str__` to std out

    Examples:

        # Access the timing stats
        with Timer() as timer:
            import time; time.sleep(1) # do something slow
        print 'Sleep for 1 second took %.03f secs' % timer.delta

        >> Sleep for 1 second took 1.003 secs

        ...

        # If you provide a message the timer outputs
        # to Log file with INFO level
        with Timer('sleep 1') as timer:
            import time; time.sleep(1) # do something slow

        >> [INFO] sleep 1 :: 1.003 secs

        ...

        # Print the message to STDOUT as well as log file with `print_message=True`
        with Timer('sleep 1', print_message=True) as timer:
            import time; time.sleep(1) # do something slow

        >> sleep 1 :: 1.003 secs
        >> [INFO] sleep 1 :: 1.003 secs

    """
    def __init__(self, message=None, print_message=False):
        self.message = message
        self.print_message = print_message
        try:
            path = inspect.stack()[1][1]
            folders = get_last_n_levels_of_path(path, CALLER_DEPTH)
            path = '.'.join(folders)
            method = inspect.stack()[1][3]
            line = inspect.stack()[1][2]
            self.caller = "{path}.{method}:{line} :: ".format(path=path,
                                                              line=line,
                                                              method=method)
        except Exception:
            self.caller = ''

    def __call__(self, f):
        @functools.wraps(f)
        def decorated(*args, **kwds):
            with self:
                return f(*args, **kwds)
        return decorated

    def __enter__(self):
        self.start = time.time()
        self.max = self.start
        self.laps = []
        self.lap_deltas = []
        self.delta = None
        self.average = None
        self.end = None
        return self

    def __str__(self):
        if self.message:
            return self.caller + self.message + ' :: ' + self.deltaPretty()
        else:
            return self.caller + self.deltaPretty()

    def deltaPretty(self):
        return self.prettySeconds(self.delta)

    def averagePretty(self):
        average = self.prettySeconds(self.average)
        message = average + ' of ' if average else ''
        return message + '%d laps' % len(self.laps)

    def prettySeconds(self, seconds):
        return '%.03f secs' % seconds if seconds is not None else ''

    def logMessage(self):
        if self.message:
            log.info(self.__str__())

    def printMessage(self):
        if self.print_message:
            print self.__str__()

    def lap(self):
        """
        Lap the timer.

        Updates max timer lap and adds time of lap
        to list of laps.
        """
        last_lap = self.laps[-1] if self.laps else self.start
        now = time.time()
        self.laps.append(now)
        self.lap_deltas.append(now - last_lap)
        self.max = max(self.laps[-1], self.max)

    def __exit__(self, *args):
        self.end = time.time()
        self.delta = self.end - self.start
        if self.laps:
            self.average = sum(self.lap_deltas) / len(self.laps)
        self.logMessage()
        self.printMessage()
