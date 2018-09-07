from datetime import datetime

from pytest import raises

from timew import Interval, IntervalError


def test_start_stop_datetime():
    interval = Interval(start_time=datetime(2018, 8, 15, 9, 0, 0),
                        end_time=datetime(2018, 8, 15, 10, 0, 0))
    assert str(interval) == 'from 20180815T090000 - 20180815T100000'


def test_start_stop_string():
    interval = Interval(start_time='2018-08-15T07:00', end_time='2018-08-15T08:30')
    assert str(interval) == 'from 20180815T070000 - 20180815T083000'


def test_invalid_duration():
    with raises(IntervalError):
        Interval(start_time='2018-08-15T07:00', duration='Invalid format')


def test_start_duration():
    interval = Interval(start_time='2018-08-15T07:00', duration='30m')
    assert str(interval) == '30m after 20180815T070000'


def test_stop_duration():
    interval = Interval(end_time='2018-08-15T07:00', duration='30m')
    assert str(interval) == '30m before 20180815T070000'
