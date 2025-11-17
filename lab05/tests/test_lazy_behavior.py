from itertools import islice
from streams import take

def noisy_iter(n):
    # yields 0..n-1 and counts how many times we pulled
    for i in range(n):
        yield i

def test_take_is_lazy():
    it = noisy_iter(1000)
    out = take(5, it)
    assert out == [0,1,2,3,4]
    # Iterator should now be at position 5; taking next 3 yields 5,6,7
    assert take(3, it) == [5,6,7]
