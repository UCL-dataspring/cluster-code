from ...harness.utils import *

def test_in_groups_of():
    assert list(groups_of(3,range(7)))==[[0,1,2],[1,2,3],[2,3,4],[3,4,5],[4,5,6]]
