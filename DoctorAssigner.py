from munkres import Munkres
import numpy as np

#function to assign doctors to hospital based on preference
def assign_doctors(ranks, capacities):
    """
    Assign doctors to hospitals using the Hungarian algorithm.

    Parameters
    ----------
    ranks : 2D list or ndarray
        ranks[i][j] = doctor i's rank of hospital j (1 = best, higher = less preferred).
    capacities : list[int]
        capacity[j] = number of slots available at hospital j; should be non-negative

    Returns
    -------
    assignments : list[int]
        assignments[i] = hospital index assigned to doctor i.
    """
    ##Error statments: Check if inputs are valid

    # Check if the rank input is a list of lists of integers
    is_2d = (isinstance(ranks, list)                              # the input is a list ...
      and all(isinstance(row, list) for row in ranks)             # ... of lists ...
      and all(all(isinstance(rank, int) for rank in row) for row in ranks) # ... of integers
    )
    if not is_2d:
      raise ValueError(f"Expected list of lists of positive integers for ranks")

    # Check if the lists of preferences have the same length
    same_len = len({len(row) for row in ranks}) == 1
    if not same_len:
      raise ValueError(f"Expected each doctor to rank the same number of hospitals")

    # Check if all rankings are positive integers
    all_positive = all(all(rank > 0 for rank in row) for row in ranks)
    if not all_positive:
      raise ValueError(f"Expected ranks to be positive")

    # Check if all capacities are non-negative integers
    valid_cap = all(isinstance(c, int) for c in capacities) and all(c >= 0 for c in capacities)
    if not valid_cap:
      raise ValueError(f"Expected capacities to be non-negative integers")

    # Check if there is a capacity for each hospital
    num_cap = len(capacities) == len(ranks[0])
    if not num_cap:
      raise ValueError(f"Expected one capacity provided for each hospital")


    # Convert ranks to a NumPy array
    ranks = np.array(ranks)
    n_doctors, n_hospitals = ranks.shape                  #gets the number of doctors and hospitals

    # Preprocess ranks and capacities to create cost matrix
    cost_matrix, slot_to_hospital = _preprocess(ranks, capacities, n_doctors)

    # Runs algorithm on matrix
    m = Munkres()
    indexes = m.compute(cost_matrix)

    # Extract assignments from the result
    assignments = _extract_assignments(indexes, slot_to_hospital, n_doctors)

    # Print final assignment for doctors to hospitals
    for doctor, hospital in enumerate(assignments):       #Loops through doctors and assigned hospital
      if hospital >= 0:                                   #prints match if there is a match
        print(f"Doctor {doctor} is matched to hospital {hospital}")
      else:                                               #Unmatched doctors have an index of -1, because when doctors go unassigned their index stays the same as originally assigned
        print(f"Doctor {doctor} wasn't assigned to a hospital :(")
    return assignments                                    # returns final list

def _preprocess(ranks, capacities, n_doctors):
    """
    Preprocess the ranks and capacities to create a cost matrix suitable for the Hungarian algorithm.

    Parameters
    ----------
    ranks : 2D np array
        ranks[i][j] = doctor i's rank of hospital j (1 = best, higher = less preferred).
    capacities : list[int]
        capacity[j] = number of slots available at hospital j; should be non-negative

    Returns
    -------
    cost_matrix : 2D list
        The cost matrix for the Hungarian algorithm.
    slot_to_hospital : list[int]
        slot_to_hospital[k] = hospital index for slot k in the cost matrix.
    """
    # Expand hospitals into slots
    expanded_cols = []                                    #stores the duplicated columns of the hospital
    slot_to_hospital = []                                 #keeps track of which slot is for which hospital
    for j, cap in enumerate(capacities):                  # j = hospital index, cap = capacity of hospital j
        for _ in range(cap):                              # repeats the "cap = capacity" times
            expanded_cols.append(ranks[:, j][:, None])    # adds hospital j's column to the expanded columns
            slot_to_hospital.append(j)                    #records which hospital this slot is for

    cost_matrix = np.hstack(expanded_cols)                #combines expanded columns into matrix

    # If there are more slots than doctors, pad rows with zeros
    if cost_matrix.shape[1] > n_doctors:
        pad_rows = cost_matrix.shape[1] - n_doctors       #gives you the number of rows needed
        pad = np.zeros((pad_rows, cost_matrix.shape[1]))  #pads the unfilled rows with 0
        cost_matrix = np.vstack([cost_matrix, pad])       #adds the pads to the matrix

    # Similarly, if there are more slots than doctors, pad columns with zeros
    if n_doctors > cost_matrix.shape[1]:
        pad_cols = n_doctors - cost_matrix.shape[1]       #gives you the number of columns needed
        pad = np.zeros((cost_matrix.shape[0], pad_cols))  #pads the unfilled columns with 0
        cost_matrix = np.hstack([cost_matrix, pad])       #adds the pads to the matrix

    # Convert to NumPy array to list of lists for Munkres
    cost_matrix = cost_matrix.tolist()

    return cost_matrix, slot_to_hospital

def _extract_assignments(indexes, slot_to_hospital, n_doctors):
    """
    Extract the assignments from the result of the Hungarian algorithm.

    Parameters
    ----------
    indexes : list[tuple[int, int]]
        The list of (row, column) indexes from the Hungarian algorithm.
    slot_to_hospital : list[int]
        slot_to_hospital[k] = hospital index for slot k in the cost matrix.
    n_doctors : int
        The number of doctors.

    Returns
    -------
    assignments : list[int]
        assignments[i] = hospital index assigned to doctor i, or -1 if unassigned.
    """

    #Build doctor to hospital assignments
    assignments = [-1] * n_doctors                         #initialize all doctors as unassigned

    for row, col in indexes:                              #loops through each doctor and their assigned slot
        if row < n_doctors and col < len(slot_to_hospital): #only consider valid doctors and slots
            assignments[row] = slot_to_hospital[col]      #assigns the hospital corresponding to the slot

    return assignments