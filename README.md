# timew - Python API for Timewarrior #

## Installation ##

For this API to work, you need [Timewarrior](https://taskwarrior.org/docs/timewarrior/download.html) installed

Installation is easy from the [Python Package Index](https://pypi.org/project/timew/)

```bash
pip install timew
```

## API Documentation ##
[Read the docs](http://tjaart.gitlab.io/python-timew)


## Examples ##

```bash
>>> from timew import TimeWarrior

>>> timew = TimeWarrior()

>>> timew.start(time=datetime(2018, 8, 15, 9, 0, 0), tags=['my tag'])
Tracking "my tag"
Started 2018-09-06T09:00:00
Current         07T13:20:45
Total              28:20:45

>>> timew.cancel()
Canceled active time tracking.

>>> timew.delete(1)
Deleted @1

>>> timew.join(1, 2)
Joined @1 and @2

>>> from timew import Duration
>>> from datetime import timedelta
>>> timew.lengthen(1, Duration(timedelta(minutes=30)))
Lengthened @1 by 0:30:00

>>> timew.move(1, datetime(2018, 8, 15, 9, 0, 0))
Moved @1 to 2018-09-05T09:00:00

>>> timew.shorten(1, Duration(timedelta(minutes=10)))
Shortened @1 by 0:10:00

>>> timew.split(1)
Split @1

>>> timew.start(tags=['my tag'])
Tracking "my tag"
Started 2018-09-07T13:37:00
Current               40:22
Total               0:03:22

>>> timew.stop()
Recorded "my tag"
Started 2018-09-07T13:37:00
Ended                 40:53
Total               0:03:53

>>> timew.track(start_time=datetime(2018, 9, 7, 11, 0, 0), end_time=datetime(2018, 9, 7, 12, 0, 0))
Tracking "from 20180907T110000 - 20180907T120000"
Started 2018-09-07T13:42:27
Current                  27
Total               0:00:00
```

## Contributing to timew ##

### Code formatting ###

To avoid [bikeshedding](https://en.wiktionary.org/wiki/bikeshedding) about code formatting, we use the following tools to format our code in a deterministic way:

- [isort](https://github.com/timothycrosley/isort) for organizing imports
- [Black](https://github.com/ambv/black) for code formatting

Our CI pipeline will fail on code that does not conform. To check your code, run `tox` in your local environment.

We recommend that you configure your favorite editor to run these commands on a shortcut. [Here](https://github.com/tjaartvdwalt/emacs-config/blob/master/load.d/init-python.el#L16-L20) is an example of my Emacs configuration
