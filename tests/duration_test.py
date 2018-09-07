from datetime import timedelta

from pytest import raises

from timew import Duration, DurationError


def test_invalid_duration():
    with raises(DurationError):
        duration = Duration('invalid duration')
    with raises(DurationError):
        duration = Duration(timedelta(minutes=-30))


def test_duration():
    assert str(Duration(timedelta(days=1))) == 'PT86400S'
    assert str(Duration(timedelta(seconds=30))) == 'PT30S'
    assert str(Duration(timedelta(minutes=30))) == 'PT1800S'
