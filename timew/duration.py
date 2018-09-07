from datetime import timedelta

from .exceptions import DurationError


class Duration:
    """
    Wrapper class for a Timewarrior Duration.
    """

    def __init__(self, delta):
        if not type(delta) is timedelta:
            raise DurationError('Duration must be of type datetime.timedelta')
        if delta < timedelta(0):
            raise DurationError('Duration cannot be negative')
        self.__delta = delta

    def __repr__(self):
        return 'PT%dS' % self.__delta.total_seconds()

    def __str__(self):
        return 'PT%dS' % self.__delta.total_seconds()
