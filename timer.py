import settings
import time
import logging
log = logging.getLogger(__name__)


class Timer(object):
    """
    Used for timing blocks of code.

    Usage:
        try:
            with Timer() as t:
                conn = httplib.HTTPConnection('example.com')
                conn.request('GET', '/')
        finally:
            print 'Request took %.03f sec.' % t.delta

    :param: message If set will log.info the message plus delta
    :param: print_message If true will print the __str__ to std out

    """
    def __init__(self, message=None, print_message=False):
        self.message = message
        self.print_message = print_message
        try:
            self.caller = inspect.stack()[1][1].split(settings.PROJ_PATH)[1] + ':' + inspect.stack()[1][3] + ' :: '
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
            return self.deltaPretty()

    def deltaPretty(self):
        return self.prettySeconds(self.delta)

    def averagePretty(self):
        average = self.prettySeconds(self.average)
        message = average + ' of ' if average else ''
        return message + '%d laps' % len(self.laps)

    def prettySeconds(self, seconds):
        return '%.2f secs' % seconds if seconds is not None else ''

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

