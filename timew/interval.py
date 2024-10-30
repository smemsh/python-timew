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
        at least start_time, and optionally one of end_time or duration must be supplied
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

        if duration and not re.match("\\d+[dDhHmMsS]", duration):
            raise IntervalError('Duration value "%s" is invalid.' % (duration))

        self.__args = []

        if start_time and end_time:
            self.__args = [
                "from",
                f"{start_time.strftime('%Y%m%dT%H%M%S')}",
                "-",
                f"{end_time.strftime('%Y%m%dT%H%M%S')}",
            ]
        elif start_time and duration:
            self.__args = [
                f"{duration}",
                "after",
                f"{start_time.strftime('%Y%m%dT%H%M%S')}",
            ]
        elif end_time and duration:
            self.__args = [
                f"{duration}",
                "before",
                f"{end_time.strftime('%Y%m%dT%H%M%S')}",
            ]
        elif start_time and not end_time and not duration:
            self.__args = [
                "from",
                f"{start_time.strftime('%Y%m%dT%H%M%S')}",
            ]
        else:
            raise IntervalError(
                "start time must be supplied; optional 2nd arg is end time or duration"
            )

    @property
    def args(self):
        return self.__args

    def __repr__(self):
        return " ".join(self.__args)

    def __str__(self):
        return " ".join(self.__args)
