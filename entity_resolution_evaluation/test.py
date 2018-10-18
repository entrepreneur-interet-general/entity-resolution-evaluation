from entity_resolution_evaluation.evaluation import gmd, evaluate, check_r_s_same_size
import pytest


def f1(x, y):
    return 1


@pytest.fixture()
def init_data():
    S = [[0, 1], [2, 3, 4], [5]]
    S3 = [[0, 1], [2, 3], [4], [5]]
    R3 = [[0, 1], [2], [3], [4], [5]]
    S2 = [[0, 1, 2, 3, 4], [5]]
    R = [[0, 1, 2], [3, 4], [5]]
    S_splitted = [[0], [1], [2], [3], [4], [5]]
    S_merged = [[0, 1, 2, 3, 4, 5]]
    R4 = [[0, 1, 2, 3, 4, 6, 7]]

    return S, S3, R3, S2, R, S_splitted, S_merged, R4


def test_gmd(init_data):
    """
    make sure the Generalized Merged Distance is computed correctly
    """
    S, S3, R3, S2, R, S_splitted, S_merged, R4 = init_data
    assert gmd(S, S, f1, f1) == 0
    assert gmd(S3, S, f1, f1) == 1
    assert gmd(S_splitted, S, f1, f1) == 3


def test_evaluate_bmd(init_data):
    S, S3, R3, S2, R, S_splitted, S_merged, R4 = init_data

    assert evaluate(S, S3, 'bmd') == 1
    assert evaluate(S, S, 'bmd') == 0


def test_evaluate_variation_of_information(init_data):
    S, S3, R3, S2, R, S_splitted, S_merged, R4 = init_data
    assert evaluate(R, S, 'variation_of_information') == 0.6365141682948129
    assert evaluate(S_merged, S, 'variation_of_information') == 1.0114042647073518
    assert evaluate(S_splitted, S, 'variation_of_information') == 0.7803552045207032
    assert evaluate(S, S, 'variation_of_information') == 0


def test_evaluate_precision(init_data):
    S, S3, R3, S2, R, S_splitted, S_merged, R4 = init_data
    assert evaluate(S_merged, S, 'precision') == 0.2666666666666667
    assert evaluate(S_splitted, S, 'precision') == 0


def test_evaluate_recall(init_data):
    S, S3, R3, S2, R, S_splitted, S_merged, R4 = init_data
    assert evaluate(S_merged, S, 'recall') == 1.0
    assert evaluate(S_splitted, S, 'recall') == 0
    assert evaluate(R, S, 'recall') == 0.5

def test_evaluate_f1(init_data):
    S, S3, R3, S2, R, S_splitted, S_merged, R4 = init_data
    assert evaluate(R, S, 'f1') == 0.5
    assert evaluate(S_merged, S, 'f1') == 0.42105263157894746


def test_check_r_s_same_size_raises_value_error(init_data):
    S, S3, R3, S2, R, S_splitted, S_merged, R4 = init_data
    with pytest.raises(ValueError):
        check_r_s_same_size(R4, S)

