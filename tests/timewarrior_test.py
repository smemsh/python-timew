from datetime import datetime, timedelta

from pytest import fixture

from timew import Duration, TimeWarrior


@fixture(scope="module")
def timew():
    yield TimeWarrior(simulate=True)


def test_cancel(timew):
    assert timew.cancel() == '/usr/bin/timew cancel'


def test_cont(timew):
    assert timew.cont(2) == '/usr/bin/timew continue @2'


def test_delete(timew):
    assert timew.delete(3) == '/usr/bin/timew delete @3'


def test_join(timew):
    assert timew.join(1, 2) == '/usr/bin/timew join @1 @2'


def test_lengthen(timew):
    assert timew.lengthen(1, Duration(timedelta(minutes=30))) \
        == '/usr/bin/timew lengthen @1 PT1800S'


def test_move(timew):
    assert timew.move(5, datetime(2018, 8, 15, 9, 0, 0)) \
        == '/usr/bin/timew move @5 20180815T090000'


def test_shorten(timew):
    assert timew.shorten(2, Duration(timedelta(minutes=10))) \
        == '/usr/bin/timew shorten @2 PT600S'


def test_split(timew):
    assert timew.split(7) == '/usr/bin/timew split @7'


def test_start(timew):
    assert timew.start(time=datetime(2018, 8, 15, 9, 0, 0), tags=['my tag']) \
        == '/usr/bin/timew start 20180815T090000 "my tag"'


def test_stop(timew):
    assert timew.stop() == '/usr/bin/timew stop'
    assert timew.stop(tags=['my tag1', 'my tag2']) \
        == '/usr/bin/timew stop "my tag1" "my tag2"'
    assert timew.stop(tags=3) \
        == '/usr/bin/timew stop @3'


def test_tag(timew):
    assert timew.tag(5, ['new tag', 'another tag']) \
        == '/usr/bin/timew tag @5 "new tag" "another tag"'


def test_untag(timew):
    assert timew.tag(1, ['new tag', 'another tag']) \
        == '/usr/bin/timew tag @1 "new tag" "another tag"'


def test_track(timew):
    assert timew.track(start_time=datetime(2018, 8, 15, 9, 0, 0),
                       end_time=datetime(2018, 8, 15, 10, 0, 0)) \
        == '/usr/bin/timew track from 20180815T090000 - 20180815T100000'
    assert timew.track(start_time=datetime(2018, 8, 15, 9, 0, 0),
                       end_time=datetime(2018, 8, 15, 9, 30, 0),
                       tags=['tag 1', 'tag 2']) \
        == '/usr/bin/timew track from 20180815T090000 - 20180815T093000 "tag 1" "tag 2"'
