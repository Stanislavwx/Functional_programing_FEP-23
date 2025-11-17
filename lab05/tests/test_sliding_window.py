from itertools import islice, starmap
from streams import sliding_window, naturals, moving_average

def test_sliding_window_basic():
    assert list(sliding_window([1,2,3,4], 3)) == [(1,2,3),(2,3,4)]

def test_sliding_window_edge():
    assert list(sliding_window([1,2], 3)) == []
    assert list(sliding_window([7], 1)) == [(7,)]

def test_sliding_window_infinite_is_bounded():
    sw = sliding_window(naturals(1), 2)
    first5_sums = list(islice((sum(w) for w in sw), 5))
    assert first5_sums == [3,5,7,9,11]

def test_moving_average():
    assert list(moving_average([1,2,3,4,5], 3)) == [2.0,3.0,4.0]
