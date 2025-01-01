import json
from datetime import datetime, timedelta
from subprocess import PIPE, Popen

from .exceptions import TimeWarriorError
from .interval import Interval


class TimeWarrior:
    """

    """

    def __init__(self, bin="timew", simulate=False):
        self.bin = bin
        self.simulate = simulate

    def annotate(self, id, annotation):
        """Add annotation to an existing interval

        Args:
            id (int): The Timewarrior id
            annotation (str): Annotation text to be set
        """
        return self.__execute("annotate", f"@{id}", f"{annotation}")

    def cancel(self):
        """If there is an open interval, it is abandoned."""
        return self.__execute("cancel")

    def cont(self, id):
        """Resumes tracking of closed intervals.

        Args:
            id (int): The Timewarrior id to be continued

        """
        return self.__execute("continue", f"@{id}")

    def delete(self, id):
        """Deletes an interval.

        Args:
            id (int): The Timewarrior id to be deleted
        """
        return self.__execute("delete", f"@{id}")

    def join(self, id1, id2):
        """Joins two intervals, by using the earlier of the two start times,
        and the later of the two end times, and the combined set of tags.

        Args:
            id1 (int): The first Timewarrior id to be joined
            id2 (int): The second Timewarrior id to be joined

        """
        return self.__execute("join", f"@{id1}", f"@{id2}")

    def lengthen(self, id, duration):
        """Defer the end date of a closed interval.

        Args:
            id (int): The Timewarrior id
            duration (timew.Duration): The duration to lengthen the interval by
        """
        return self.__execute("lengthen", f"@{id}", f"{str(duration)}")

    def modify(self, start_or_end, id, time):
        """Changes the start or end of an interval.

        Args:
            start_or_end (str): "start" or "end"
            id (int): The Timewarrior id
            time (datetime): The new start or end time for the interval
        """
        if start_or_end not in ["start", "end"]:
            raise ValueError("start_or_end must be either start or end")
        return self.__execute(
            "modify", start_or_end, f"@{id}", self.__strfdatetime(time)
        )

    def move(self, id, time):
        """Reposition an interval at a new start time.

        Args:
            id (int): The Timewarrior id
            time (datetime): The new start time for the interval

        """
        return self.__execute("move", f"@{id}", self.__strfdatetime(time))

    def shorten(self, id, duration):
        """Advance the end date of a closed interval.

        Args:
            id (int): The Timewarrior id
            duration (timew.Duration): The duration to shorten the interval by

        """
        return self.__execute("shorten", f"@{id}", f"{str(duration)}")

    def export(self, ids=None, start_time=None, end_time=None, tags=None):
        """export timewarrior entries by list of integer IDs, """ \
        """or with optional tags and for optional interval, """ \
        """default all entries in the database

        Args:
            intervals (list[int], optional): list of IDs to export, exclusive of other options
            start_time (datetime, optional): start of interval to list entries for.
            end_time (datetime, optional): end of interval to list entries for.
            tags (list, optional): dump only events with matching tag(s)

        Returns a list of database entries formatted like the following::

          [{"id": 1, "start": "20190123T092300Z",
            "tags": ["watering new plants","gardening"]},
           {"id" : 2, "start": "20190123T085000Z", "end": "20190123T092256Z",
            "tags": ["helped plant roses","gardening"]}]

        the above contains a started (but not ended) entry with id=1; and an ended entry with id=2

        """
        cmd = ['export']

        if ids is not None:
            if start_time or end_time or tags:
                raise ValueError("ids can only be specified exclusively")
            if type(ids) is not list:
                raise ValueError("ids must be provided as a list")
            if not all([type(i) is int for i in ids]):
                raise ValueError("provided ids must all be integers")
            cmd += [f"@{id}" for id in ids]

        interval = None
        if start_time:
            interval = Interval(start_time=start_time, end_time=end_time)

        if interval: cmd += interval.args
        if tags: cmd += tags

        out = self.__execute(*cmd)
        if self.simulate:
            return out

        return json.loads(out[0])

    def list(self, start_time=None, end_time=None):
        """export the timewarrior entries for interval

        Args:
            start_time (datetime, optional): start of interval to list entries for.
            end_time (datetime, optional): start of interval to list entries for.

        Returns a list of database entries formatted like the following::

          [{"id": 1, "start": "20190123T092300Z",
            "tags": ["watering new plants","gardening"]},
           {"id" : 2, "start": "20190123T085000Z", "end": "20190123T092256Z",
            "tags": ["helped plant roses","gardening"]}]

        the above contains a started (but not ended) entry with id=1; and an ended entry with id=2
        """

        if not start_time:
            now = datetime.now()
            start_time = datetime(now.year, now.month, now.day)
            end_time = datetime(now.year, now.month, now.day, 23, 59, 59)

        interval = Interval(start_time=start_time, end_time=end_time)
        cmd = f"export {interval}"
        out = self.__execute(*(cmd.split()))

        if self.simulate:
            return out
        data = json.loads(out[0])

        data.reverse()
        return data

    def summary(self, start_time=None, end_time=None):
        """export the timewarrior entries for interval

        Args:
            start_time (datetime, optional): start of interval to list entries for.
            end_time (datetime, optional): start of interval to list entries for.

        Returns a list of database entries formatted like the following::

          [{"id": 1, "start": "20190123T092300Z",
            "tags": ["watering new plants","gardening"]},
           {"id" : 2, "start": "20190123T085000Z", "end": "20190123T092256Z",
            "tags": ["helped plant roses","gardening"]}]

        the above contains a started (but not ended) entry with id=1; and an ended entry with id=2
        """
        return self.list(start_time, end_time)

    def split(self, id):
        """Splits an interval into two equally sized adjacent intervals,
        having the same tags.

        Args:
            id (int): The Timewarrior id to split

        """
        return self.__execute("split", f"@{id}")

    def start(self, time=None, tags=None):
        """Begins tracking using the current time with any specified set of tags.

        Args:
            time (datetime): The time to start the interval
            tags (list[str]): The list of tags to apply to the interval

        """
        if time is None:
            time = datetime.now()
        args = ["start", self.__strfdatetime(time)]
        if tags:
            for tag in tags:
                args.append(f"{tag}")

        return self.__execute(*args)

    def stop(self, tags=None):
        """Stops tracking time. If tags are specified, then they are no longer tracked.
        If no tags are specified, all tracking stops.

        Args:
            tags (int): The Timewarrior id
            tags (list): The list of tags to stop tracking

        """
        args = ["stop"]
        if tags:
            if isinstance(tags, type(list())):
                for tag in tags:
                    args.append(f"{tag}")
            else:
                args.append(f"@{tags}")

        return self.__execute(*args)

    def tag(self, id, tags):
        """Adds a tag to an interval.

        Args:
            id (int): The Timewarrior id
            tags (list): The list of tags to add to the interval
        """
        args = ["tag", f"@{id}"]
        for tag in tags:
            args.append(f"{tag}")

        return self.__execute(*args)

    def track(self, start_time, end_time=None, tags=None):
        """The track command is used to add tracked time in the past.
           Perhaps you forgot to record time, or are just filling in old entries.

        Args:
            start_time (datetime): The task start time.
            end_time (datetime, optional): The task end time. (required if duration not given)
            duration (timew.Timedelta, optional): The task duration. (required if task not given)
            tags (list[str]): The tags

        Raises:
            TimewarriorError: Timew command errors
        """
        args = ["track"]

        interval = Interval(start_time=start_time, end_time=end_time)
        args += interval.args

        if tags:
            for tag in tags:
                args.append(f"{tag}")

        return self.__execute(*args)

    def untag(self, id, tags):
        """Remove a tag from an interval

        Args:
            id (int): The Timewarrior id
            tag (str): The tag to remove
        """
        args = ["untag", f"@{id}"]
        for tag in tags:
            args.append(f'{tag}')

        return self.__execute(*args)

    def __strftimedelta(self, duration):
        if type(duration) is timedelta:
            return "PT%dS" % duration.total_seconds()
        else:
            return duration

    def __strfdatetime(self, dt):
        if type(dt) is datetime:
            return dt.strftime("%Y%m%dT%H%M%S")
        else:
            return dt

    def __export(self):
        stdout, stderr = self.__execute("export")
        data = json.loads(stdout)
        data.reverse()
        return data

    def __execute(self, *args):
        """ Execute a given timewarrior command with arguments
        Returns a 2-tuple of stdout and stderr (respectively).
        """
        command = [self.bin] + list(args)
        if self.simulate:
            return command

        try:
            proc = Popen(command, stdout=PIPE, stderr=PIPE)
            stdout, stderr = proc.communicate()
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise OSError(f"Unable to find the '{self.bin}' command-line tool.")
            raise

        if proc.returncode != 0:
            raise TimeWarriorError(command, stderr.strip().decode(), proc.returncode)

        return stdout.strip().decode(), stderr.strip().decode()
