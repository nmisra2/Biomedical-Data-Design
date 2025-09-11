import pytest
import numpy as np
from DoctorAssigner import assign_doctors, _preprocess, _extract_assignments

# Test for ranks to be a 2D list of lists, not a flat list
def test_invalid_iput1():
    ranks = [3, 2, 1]  # Invalid rank (not 2d list)
    capacities = [1, 1, 1]
    with pytest.raises(ValueError, match="Expected list of lists of positive integers for ranks"):
        assign_doctors(ranks, capacities)

# Test for ranks cannot be 3D
def test_invalid_iput2():
    ranks = [[[1,2], [2, 1]],[[1,2], [2, 1]]]  # Invalid rank (not 2d list)
    capacities = [1, 1]
    with pytest.raises(ValueError, match="Expected list of lists of positive integers for ranks"):
        assign_doctors(ranks, capacities) 

# Test for ranks must contain integers, not strings
def test_invalid_iput3():
    ranks = [['a', 'b', 'c'], ['b', 'c', 'a']]  # Invalid rank (not integers)
    capacities = [1, 1, 1]
    with pytest.raises(ValueError, match="Expected list of lists of positive integers for ranks"):
        assign_doctors(ranks, capacities)  

# Test for ranks must contain integers, not floats or strings
def test_invalid_iput4():
    ranks = [[0.5, 1.1, 4.6], ['b', 'c', 'a']]  # Invalid rank (not integers)
    capacities = [1, 1, 1]
    with pytest.raises(ValueError, match="Expected list of lists of positive integers for ranks"):
        assign_doctors(ranks, capacities)   
# Test for all doctors must rank the same number of hospitals
def test_invalid_iput5():
    ranks = [[1, 2, 3], [2, 1]]  # Invalid rank (list lengths differ)
    capacities = [1, 1, 1]
    with pytest.raises(ValueError, match="Expected each doctor to rank the same number of hospitals"):
        assign_doctors(ranks, capacities)

# Test for ranks must all be positive, no negative values allowed
def test_invalid_iput6():
    ranks = [[1, 2, 3], [2, 1, -1]]  # Invalid rank (negative rank)
    capacities = [1, 1, 1]
    with pytest.raises(ValueError, match="Expected ranks to be positive"):
        assign_doctors(ranks, capacities)

# Test for hospital capacities must be non-negative integers
def test_invalid_iput7():
    ranks = [[1, 2, 3], [2, 1, 3]]  
    capacities = [1, 1, -1]     # Invalid capacity (negative capacity)
    with pytest.raises(ValueError, match="Expected capacities to be non-negative integers"):
        assign_doctors(ranks, capacities)

# Test for length of capacities list must equal number of hospitals
def test_invalid_iput8():
    ranks = [[1, 2, 3], [2, 1, 3]]  
    capacities = [1, 1]     # Invalid capacity (length mismatch)
    with pytest.raises(ValueError, match="Expected one capacity provided for each hospital"):
        assign_doctors(ranks, capacities)

# Test the preprocess, pads extra doctors (rows) when total slots > doctors
def test_preprocess1(): # test padding of doctors
    ranks = np.array([[1, 2, 3], [3, 2, 1]])
    capacities = [1, 1, 1]
    n_doctors = 2
    cost_matrix, slot_to_hospital = _preprocess(ranks, capacities, n_doctors)
    expected_cost_matrix = [[1, 2, 3], [3, 2, 1], [0, 0, 0]]
    expected_slot_to_hospital = [0, 1, 2]
    assert (cost_matrix == expected_cost_matrix)
    assert slot_to_hospital == expected_slot_to_hospital

# Test the preprocess, pads extra hospital slots (columns) when doctors > total slots
def test_preprocess2(): # test padding of hospital slots
    ranks = np.array([[1, 2], [2, 1], [1, 2]])
    capacities = [1, 1]
    n_doctors = 3
    cost_matrix, slot_to_hospital = _preprocess(ranks, capacities, n_doctors)
    expected_cost_matrix = [[1, 2, 0], [2, 1, 0], [1, 2, 0]]
    expected_slot_to_hospital = [0, 1]
    assert (cost_matrix == expected_cost_matrix)
    assert slot_to_hospital == expected_slot_to_hospital

# Test the preprocess, expands hospitals into multiple slots based on capacity
def test_preprocess3(): # test slot mapping
    ranks = np.array([[1, 2, 3], [3, 2, 1], [3, 1, 2], [1, 2, 3], [3, 2, 1], [3, 1, 2]])
    capacities = [0, 2, 4]
    n_doctors = 6
    cost_matrix, slot_to_hospital = _preprocess(ranks, capacities, n_doctors)
    expected_cost_matrix = [[2, 2, 3, 3, 3, 3], [2, 2, 1, 1, 1, 1], [1, 1, 2, 2, 2, 2], [2, 2, 3, 3, 3, 3], [2, 2, 1, 1, 1, 1], [1, 1, 2, 2, 2, 2]]
    expected_slot_to_hospital = [1, 1, 2, 2, 2, 2]
    assert (cost_matrix == expected_cost_matrix)
    assert slot_to_hospital == expected_slot_to_hospital

# Test the extract_assignments, maps solver indexes back to doctor→hospital assignments
def test_extract_assignments1():
    indexes = [(0, 1), (1, 0), (2, 2)]
    slot_to_hospital = [0, 1, 2]
    n_doctors = 3
    assignments = _extract_assignments(indexes, slot_to_hospital, n_doctors)
    expected_assignments = [1, 0, 2]
    assert assignments == expected_assignments

# Test for assign_doctors produces the minimum total cost assignment
def test_min_cost1():
    ranks = [[1, 2, 3], [3, 2, 1], [1, 3, 2]]
    capacities = [1, 1, 1]
    expected_cost = 4
    assignments = assign_doctors(ranks, capacities)
    actual_cost = sum(ranks[i][assignments[i]] for i in range(len(assignments)) if assignments[i] != -1)
    assert actual_cost == expected_cost