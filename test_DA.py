import pytest
import numpy as np
from DoctorAssigner import assign_doctors, _preprocess, _extract_assignments

def test_invalid_iput1():
    ranks = [3, 2, 1]  # Invalid rank (not 2d list)
    capacities = [1, 1, 1]
    with pytest.raises(ValueError, match="Expected list of lists of positive integers for ranks"):
        assign_doctors(ranks, capacities)

def test_invalid_iput2():
    ranks = [[[1,2], [2, 1]],[[1,2], [2, 1]]]  # Invalid rank (not 2d list)
    capacities = [1, 1]
    with pytest.raises(ValueError, match="Expected list of lists of positive integers for ranks"):
        assign_doctors(ranks, capacities) 

def test_invalid_iput3():
    ranks = [['a', 'b', 'c'], ['b', 'c', 'a']]  # Invalid rank (not integers)
    capacities = [1, 1, 1]
    with pytest.raises(ValueError, match="Expected list of lists of positive integers for ranks"):
        assign_doctors(ranks, capacities)  

def test_invalid_iput4():
    ranks = [[0.5, 1.1, 4.6], ['b', 'c', 'a']]  # Invalid rank (not integers)
    capacities = [1, 1, 1]
    with pytest.raises(ValueError, match="Expected list of lists of positive integers for ranks"):
        assign_doctors(ranks, capacities)   

def test_invalid_iput5():
    ranks = [[1, 2, 3], [2, 1]]  # Invalid rank (list lengths differ)
    capacities = [1, 1, 1]
    with pytest.raises(ValueError, match="Expected each doctor to rank the same number of hospitals"):
        assign_doctors(ranks, capacities)

def test_invalid_iput6():
    ranks = [[1, 2, 3], [2, 1, -1]]  # Invalid rank (negative rank)
    capacities = [1, 1, 1]
    with pytest.raises(ValueError, match="Expected ranks to be positive"):
        assign_doctors(ranks, capacities)

def test_invalid_iput7():
    ranks = [[1, 2, 3], [2, 1, 3]]  
    capacities = [1, 1, -1]     # Invalid capacity (negative capacity)
    with pytest.raises(ValueError, match="Expected capacities to be non-negative integers"):
        assign_doctors(ranks, capacities)

def test_invalid_iput8():
    ranks = [[1, 2, 3], [2, 1, 3]]  
    capacities = [1, 1]     # Invalid capacity (length mismatch)
    with pytest.raises(ValueError, match="Expected one capacity provided for each hospital"):
        assign_doctors(ranks, capacities)

def test_preprocess1(): # test padding of doctors
    ranks = np.array([[1, 2, 3], [3, 2, 1]])
    capacities = [1, 1, 1]
    n_doctors = 2
    cost_matrix, slot_to_hospital = _preprocess(ranks, capacities, n_doctors)
    expected_cost_matrix = [[1, 2, 3], [3, 2, 1], [0, 0, 0]]
    expected_slot_to_hospital = [0, 1, 2]
    assert (cost_matrix == expected_cost_matrix)
    assert slot_to_hospital == expected_slot_to_hospital

def test_preprocess2(): # test padding of hospital slots
    ranks = np.array([[1, 2], [2, 1], [1, 2]])
    capacities = [1, 1]
    n_doctors = 3
    cost_matrix, slot_to_hospital = _preprocess(ranks, capacities, n_doctors)
    expected_cost_matrix = [[1, 2, 0], [2, 1, 0], [1, 2, 0]]
    expected_slot_to_hospital = [0, 1]
    assert (cost_matrix == expected_cost_matrix)
    assert slot_to_hospital == expected_slot_to_hospital

def test_preprocess3(): # test slot mapping
    ranks = np.array([[1, 2, 3], [3, 2, 1], [3, 1, 2], [1, 2, 3], [3, 2, 1], [3, 1, 2]])
    capacities = [0, 2, 4]
    n_doctors = 6
    cost_matrix, slot_to_hospital = _preprocess(ranks, capacities, n_doctors)
    expected_cost_matrix = [[2, 2, 3, 3, 3, 3], [2, 2, 1, 1, 1, 1], [1, 1, 2, 2, 2, 2], [2, 2, 3, 3, 3, 3], [2, 2, 1, 1, 1, 1], [1, 1, 2, 2, 2, 2]]
    expected_slot_to_hospital = [1, 1, 2, 2, 2, 2]
    assert (cost_matrix == expected_cost_matrix)
    assert slot_to_hospital == expected_slot_to_hospital

def test_extract_assignments1():
    indexes = [(0, 1), (1, 0), (2, 2)]
    slot_to_hospital = [0, 1, 2]
    n_doctors = 3
    assignments = _extract_assignments(indexes, slot_to_hospital, n_doctors)
    expected_assignments = [1, 0, 2]
    assert assignments == expected_assignments