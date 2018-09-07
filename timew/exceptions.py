import sys


class DurationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class IntervalError(Exception):
    def __init__(self, message):
        super().__init__(message)


class TimeWarriorError(Exception):
    def __init__(self, command, stderr, code):
        self.command = command
        self.stderr = stderr
        self.code = code
