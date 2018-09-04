import sys


class TimeWarriorError(Exception):
    def __init__(self, command, stderr, code):
        self.command = command
        self.stderr = stderr
        self.code = code
