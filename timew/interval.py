import re
from datetime import datetime, timedelta

from dateutil.parser import parse

from .exceptions import IntervalError


class Interval:
    """
    Wrapper class for a Timewarrior Interval.
    """

    def __init__(self, start_time=None, end_time=None, duration=None):
        """
        2 of the 3 keyword arguments need to be supplied.
        If all 3 are supplied, start_time and end_time takes precedence over duration

        Arguments:
            start_time (datetime.date/str): Start time for interval
            end_time (datetime.date/str): End time for interval
            duration (timew.Duration): Duration of the interval
        """
        # Test for valid input
        if type(start_time) is str:
            start_time = parse(start_time)

        if type(end_time) is str:
            end_time = parse(end_time)

        if(duration and not re.match("\\d+[dDhHmMsS]", duration)):
            raise IntervalError('Duration value "%s" is invalid.' % (duration))

        self.__interval = ''

        if(start_time and end_time):
            self.__interval = 'from %s - %s' % (start_time.strftime('%Y%m%dT%H%M%S'),
                                                end_time.strftime('%Y%m%dT%H%M%S'))
        elif(start_time and duration):
            self.__interval = '%s after %s' % (duration,
                                               start_time.strftime('%Y%m%dT%H%M%S'))
        elif(end_time and duration):
            self.__interval = '%s before %s' % (duration,
                                                end_time.strftime('%Y%m%dT%H%M%S'))
        else:
            raise IntervalError(
                'At least 2 arguments need to be supplied: start time, end time, duration')

    def __repr__(self):
        return self.__interval

    def __str__(self):
        return self.__interval
