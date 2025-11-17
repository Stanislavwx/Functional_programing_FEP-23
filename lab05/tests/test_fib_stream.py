from itertools import islice
from streams import fib_stream

def test_first_10_fib():
    assert list(islice(fib_stream(), 10)) == [0,1,1,2,3,5,8,13,21,34]
