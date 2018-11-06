import pytest

from entity_resolution_evaluation.reconcile import reconcile


@pytest.fixture()
def init_data():
    S = [[0, 1], [2, 3, 4], [5]]
    R5 = [[0,1,2,3,4,8],[5,1,10,11],[13,14]]
    return S, R5


def test_reconcile_r_s(init_data):
    S, R5 = init_data
    R1,S1 =  reconcile(R5,S, 'R1S1')
    assert S1 == [[0, 1], [2, 3, 4], [5], [8], [10, 11]]