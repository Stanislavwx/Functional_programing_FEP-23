from itertools import count, islice
from streams import take, drop, naturals

def test_take_and_stream_progress():
    xs = naturals(1)
    assert take(5, xs) == [1,2,3,4,5]
    # xs has advanced
    assert take(3, xs) == [6,7,8]

def test_drop_then_take():
    xs = drop(10, count(0))
    assert list(islice(xs, 3)) == [10,11,12]

def test_negative_take_drop():
    xs = naturals(0)
    assert take(-5, xs) == []
    ys = drop(-3, [1,2,3])
    assert list(ys) == [1,2,3]
