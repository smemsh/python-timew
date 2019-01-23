import json
from datetime import datetime, timedelta
from subprocess import PIPE, Popen

from .exceptions import TimeWarriorError
from .interval import Interval


class TimeWarrior:
    """

    """

    def __init__(self,  bin='timew', simulate=False):
        self.bin = bin
        self.simulate = simulate

    def cancel(self):
        """If there is an open interval, it is abandoned."""
        return self.__execute('cancel')

    def cont(self, id):
        """Resumes tracking of closed intervals.

        Args:
            id (int): The Timewarrior id to be continued

        """
        return self.__execute('continue @%d' % id)

    def delete(self, id):
        """Deletes an interval.

        Args:
            id (int): The Timewarrior id to be deleted
        """
        return self.__execute('delete', '@%d' % id)

    def join(self, id1, id2):
        """Joins two intervals, by using the earlier of the two start times,
        and the later of the two end times, and the combined set of tags.

        Args:
            id1 (int): The first Timewarrior id to be joined
            id2 (int): The second Timewarrior id to be joined

        """
        return self.__execute('join', '@%d' % id1, '@%d' % id2)

    def lengthen(self, id, duration):
        """Defer the end date of a closed interval.

        Args:
            id (int): The Timewarrior id
            duration (timew.Duration): The duration to lengthen the interval by
        """
        return self.__execute('lengthen', '@%d' % id, '%s' % str(duration))

    def move(self, id, time):
        """Reposition an interval at a new start time.

        Args:
            id (int): The Timewarrior id
            time (datetime): The new start time for the interval

        """
        return self.__execute('move', '@%d' % id, self.__strfdatetime(time))

    def shorten(self, id, duration):
        """Advance the end date of a closed interval.

        Args:
            id (int): The Timewarrior id
            duration (timew.Duration): The duration to shorten the interval by

        """
        return self.__execute('shorten', '@%d' % id, '%s' % str(duration))

    def list(self, start_time=None, end_time=datetime.now()):
        """export the timewarrior entries for interval

        Args:
            start_time (datetime, optional): start of interval to list entries for.
            end_time (datetime, optional): start of interval to list entries for.

        Returns a list of database entries formatted like the following
        [
        {"id" : 1,"start":"20190123T092300Z","tags":["watering new plants","gardening"]},
        {"id" : 2,"start":"20190123T085000Z","end":"20190123T092256Z","tags":["helped plant roses","gardening"]}
        ]
        the above contains a started (but not ended) entry with id=1; and an ended entry with id=2
        """

        if not start_time:
            now = datetime.now()
            start_time = datetime(now.year, now.month, now.day)
            end_time = datetime(now.year, now.month, now.day, 23, 59, 59)

        interval = Interval(start_time=start_time, end_time=end_time)
        cmd = f'export {interval}'
        out = self.__execute(*(cmd.split()))

        if self.simulate:
            return out
        data = json.loads(out[0])

        data.reverse()
        counter = 1
        for d in data:
            d["id"] = counter
            counter += 1
        return data

    def summary(self, start_time=None, end_time=None):
        """export the timewarrior entries for interval

        Args:
            start_time (datetime, optional): start of interval to list entries for.
            end_time (datetime, optional): start of interval to list entries for.

        Returns a list of database entries formatted like the following
        [
        {"id" : 1,"start":"20190123T092300Z","tags":["watering new plants","gardening"]},
        {"id" : 2,"start":"20190123T085000Z","end":"20190123T092256Z","tags":["helped plant roses","gardening"]}
        ]
        the above contains a started (but not ended) entry with id=1; and an ended entry with id=2
        """
        return self.list(start_time, end_time)

    def split(self, id):
        """Splits an interval into two equally sized adjacent intervals,
        having the same tags.

        Args:
            id (int): The Timewarrior id to split

        """
        return self.__execute('split', '@%d' % id)

    def start(self, time=datetime.now(), tags=None):
        """Begins tracking using the current time with any specified set of tags.

        Args:
            time (datetime): The time to start the interval
            tags (list<str>): The list of tags to apply to the interval

        """
        args = ['start', self.__strfdatetime(time)]
        if(tags):
            for tag in tags:
                args.append('"%s"' % tag)

        return self.__execute(*args)

    def stop(self, tags=None):
        """Stops tracking time. If tags are specified, then they are no longer tracked.
        If no tags are specified, all tracking stops.

        Args:
            tags (int): The Timewarrior id
            tags (list): The list of tags to stop tracking

        """
        args = ['stop']
        if tags:
            if isinstance(tags, type(list())):
                for tag in tags:
                    args.append('"%s"' % tag)
            else:
                args.append(f"@{tags}")

        return self.__execute(*args)

    def tag(self, id, tags):
        """Adds a tag to an interval.

        Args:
            id (int): The Timewarrior id
            tags (list): The list of tags to add to the interval
        """
        args = ['tag', '@%d' % id]
        for tag in tags:
            args.append('"%s"' % tag)

        return self.__execute(*args)

    def track(self, start_time, end_time=None, tags=None):
        """The track command is used to add tracked time in the past.
           Perhaps you forgot to record time, or are just filling in old entries.

        Args:
            start_time (datetime): The task start time.
            end_time (datetime, optional): The task end time. (required if duration not given)
            duration (timew.Timedelta, optional): The task duration. (required if task not given)
            tags (list of string): The tags

        Raises:
            TimewarriorError: Timew command errors
        """
        args = ['track']

        interval = Interval(start_time=start_time, end_time=end_time)
        args.append(str(interval))

        if tags:
            for tag in tags:
                args.append('"%s"' % tag)

        return self.__execute(*args)

    def untag(self, id, tag):
        """Remove a tag from an interval

        Args:
            id (int): The Timewarrior id
            tag (str): The tag to remove
        """
        return self.__execute(args)

    def __strftimedelta(self, duration):
        if type(duration) is timedelta:
            return 'PT%dS' % duration.total_seconds()
        else:
            return duration

    def __strfdatetime(self, dt):
        if type(dt) is datetime:
            return dt.strftime('%Y%m%dT%H%M%S')
        else:
            return dt

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
            return ' '.join(command)

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
