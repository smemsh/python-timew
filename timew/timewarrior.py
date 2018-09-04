import json
from datetime import datetime, timedelta
from subprocess import PIPE, Popen

from .exceptions import TimeWarriorError


class TimeWarrior:
    """

    """

    def __init__(self,  bin='/usr/bin/timew', simulate=False):
        self.bin = bin
        self.simulate = simulate

    def cancel(self):
        """If there is an open interval, it is abandoned."""
        self.__execute('cancel')

    def cont(self, id, date):
        """Resumes tracking of closed intervals.

        Args:

        """
        self.__execute('continue', str(id), date)

    def delete(self, id):
        self.__execute('delete', '@%d' % id)

    def join(self, id1, id2):
        self.__execute('join', id1, id2)

    def lengthen(self, id, duration):
        self.__execute('lengthen', '@%d' % id, duration)

    def move(self, id, datetime):
        self.__execute('move', '@%d' % id, datetime)

    def shorten(self, id, duration):
        self.__execute('shorten', '@%d' % id, duration)

    def split(self, id):
        self.__execute('split', '@%d' % id)

    def start(self, date=None, tags=None):
        args = ['start']
        if(date):
            args.append(date)
        if(tags):
            args += tags
        self.__execute(*args)

    def stop(self, tags=None):
        args = ['stop']
        if(tags):
            args.append(tags)
        self.__execute(*args)

    def tag(self, id, tags):
        self.__execute(self, 'tag', '@%d' % id, tags)

    def track(self, start_date, end_date, tags=None):
        """The track command is used to add tracked time in the past.
           Perhaps you forgot to record time, or are just filling in old entries.

        Args:
            start_date (datetime): The task start time.
            end_date (datetime or timedelta, optional): The task end time, or task duration.
            tags (list of string): The tags

        Raises:
            TimewarriorError: Timew command errors
        """
        args = ['track']
        args.append(self.__strfdatetime(start_date))

        if type(end_date) is timedelta:
            args.append('for')
            args.append(self.__strftimedelta(end_date))
        else:
            args.append('to')
            args.append(self.__strfdatetime(end_date))

        if(tags):
            args += tags

        self.__execute(*args)

    def untag(self, id, tag):
        self.__execute(args)

    def __strftimedelta(self, duration):
        return 'PT%dS' % duration.total_seconds()

    def __strfdatetime(self, dt):
        return dt.strftime('%Y%m%dT%H%M%S')

    def __export(self):
        stdout, stderr = self.__execute('export')
        data = json.loads(stdout)
        data.reverse()
        return data

    def __execute(self, *args):
        """ Execute a given timewarrior command with arguments
        Returns a 2-tuple of stdout and stderr (respectively).
        """
        command = [self.bin] + list(args)
        if(self.simulate):
            return command

        try:
            proc = Popen(
                command,
                stdout=PIPE,
                stderr=PIPE,
            )
            stdout, stderr = proc.communicate()
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise OSError("Unable to find the '%s' command-line tool." % (self.bin))
            raise

        if proc.returncode != 0:
            raise TimeWarriorError(command, stderr.strip().decode(), proc.returncode)

        return stdout.strip().decode(), stderr.strip().decode()
