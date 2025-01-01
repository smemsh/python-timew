from datetime import datetime, timedelta

from pytest import fixture, raises

from timew import Duration, TimeWarrior

TWBIN = "timew"


@fixture(scope="module")
def timew():
    yield TimeWarrior(simulate=True)


def test_cancel(timew):
    assert timew.cancel() == [TWBIN, "cancel"]


def test_cont(timew):
    assert timew.cont(2) == [TWBIN, "continue", "@2"]


def test_delete(timew):
    assert timew.delete(3) == [TWBIN, "delete", "@3"]


def test_join(timew):
    assert timew.join(1, 2) == [TWBIN, "join", "@1", "@2"]


def test_lengthen(timew):
    assert timew.lengthen(1, Duration(timedelta(minutes=30))) == [
        TWBIN,
        "lengthen",
        "@1",
        "PT1800S",
    ]


def test_list(timew):
    assert not isinstance(timew.list(), type(None))
    assert len(timew.list()) == 6
    assert "from" in timew.list()


def test_modify(timew):
    assert timew.modify("start", 5, datetime(2018, 8, 15, 9, 0, 0)) == [
        TWBIN,
        "modify",
        "start",
        "@5",
        "20180815T090000",
    ]
    assert timew.modify("end", 5, datetime(2018, 8, 15, 9, 0, 0)) == [
        TWBIN,
        "modify",
        "end",
        "@5",
        "20180815T090000",
    ]
    with raises(ValueError):
        timew.modify("strat", 5, datetime(2018, 8, 15, 9, 0, 0))


def test_move(timew):
    assert timew.move(5, datetime(2018, 8, 15, 9, 0, 0)) == [
        TWBIN,
        "move",
        "@5",
        "20180815T090000",
    ]


def test_shorten(timew):
    assert timew.shorten(2, Duration(timedelta(minutes=10))) == [
        TWBIN,
        "shorten",
        "@2",
        "PT600S",
    ]


def test_split(timew):
    assert timew.split(7) == [TWBIN, "split", "@7"]


def test_start(timew):
    assert timew.start(time=datetime(2018, 8, 15, 9, 0, 0), tags=["my tag"]) == [
        TWBIN,
        "start",
        "20180815T090000",
        "my tag",
    ]


def test_stop(timew):
    assert timew.stop() == [TWBIN, "stop"]
    assert timew.stop(tags=["my tag1", "my tag2"]) == [
        TWBIN,
        "stop",
        "my tag1",
        "my tag2",
    ]


def test_tag(timew):
    assert timew.tag(5, ["new tag", "another tag"]) == [
        TWBIN,
        "tag",
        "@5",
        "new tag",
        "another tag",
    ]


def test_untag(timew):
    assert timew.tag(1, ["new tag", "another tag"]) == [
        TWBIN,
        "tag",
        "@1",
        "new tag",
        "another tag",
    ]


def test_track(timew):
    assert timew.track(
        start_time=datetime(2018, 8, 15, 9, 0, 0),
        end_time=datetime(2018, 8, 15, 10, 0, 0),
    ) == [
        TWBIN,
        "track",
        "from",
        "20180815T090000",
        "-",
        "20180815T100000",
    ]
    assert timew.track(
        start_time=datetime(2018, 8, 15, 9, 0, 0),
        end_time=datetime(2018, 8, 15, 9, 30, 0),
        tags=["tag 1", "tag 2"],
    ) == [
        TWBIN,
        "track",
        "from",
        "20180815T090000",
        "-",
        "20180815T093000",
        "tag 1",
        "tag 2",
    ]


def test_export(timew):
    assert timew.export() == [TWBIN, 'export']
    assert timew.export(ids=[7, 14, 18],) == [
        TWBIN, 'export', '@7', '@14', '@18'
    ]
    with raises(ValueError):
        assert timew.export(
            ids=[1, 2, 3],
            start_time=datetime(2018, 8, 15, 9, 0, 0),
        )
    with raises(ValueError):
        assert timew.export(ids=[1, 2, 3], tags=['foo'])


def test_annotate(timew):
    note = 'test annotation including spaces'
    assert timew.annotate(1, note) == [TWBIN, 'annotate', '@1', note]
