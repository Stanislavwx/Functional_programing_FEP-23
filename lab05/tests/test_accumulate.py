from itertools import accumulate
import operator
from streams import accumulate_sum, accumulate_prod, accumulate_custom

def test_accumulate_builtin_examples():
    assert list(accumulate([1,2,3,4])) == [1,3,6,10]
    assert list(accumulate([1,2,3,4], operator.mul)) == [1,2,6,24]

def test_accumulate_wrappers():
    assert list(accumulate_sum([1,2,3,4])) == [1,3,6,10]
    assert list(accumulate_prod([1,2,3,4])) == [1,2,6,24]
    assert list(accumulate_custom([3,1,4,1,5], max)) == [3,3,4,4,5]
