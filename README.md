
# First In-class Project: Coding a Rank-order Assignment Algorithm
## TEAM INFORMATION:
* Naina Misra
* Rex Wang
* Phoebe Wu


## CONTRIBUTIONS:
* Naina - Conducted research, helped develop code for Hungarian algorithm, developed the code to output which doctors are matched to each hospital, edited code, wrote introduction
* Rex - Conducted research, helped develop code handling input and printing output, modularized functions, and wrote unit tests.
* Phoebe - Conducted research and found resources, helped brainstorm assignment system, commented code, wrote Algorithm Implemented


## ASSUMPTIONS:
* Hospitals do not participate in ranking doctors
* Doctors will always rank every hospital
* Input matrix will be i = doctors, j = hospital
* Capacity for each hospital will be mentioned in capacities, and be non-negative


## ALGORITHM IMPLEMENTED:

We need to assign doctors to hospitals based on their ranked preference.

The doctors rank their preference of hospitals with (1) being the number one preference and larger numbers representing lower preference.

There is a capacity for the number of doctors for each hospital and a doctor can only be assigned to one hospital.

To solve this problem, we choose to work with the Hungarian Algorithm, which is also known as the Munkres Algorithm.

This algorithm provides a way to match a doctor to a hospital while minimizing the cost. In our system, the cost is defined based on the doctor's preference.
Therefore, the higher the rank of the hospital (1 being the highest), the lower the cost.

The preferences data was represented by a matrix with the rows being the doctor's preferences of each hospital and the hospital as columns.
When a hospital had multiple slots open, the matrix was expanded to have multiple columns representing the hospital to reflect the capacity.
The Munkres Algorithm requires a square matrix.

However, sometimes, the number of doctors and hospitals may be unequal.
Therefore, the matrix was padded with dummy doctors or hospital slots to ensure the algorithm runs smoothly while the doctors that were
unmatched remained unassigned.

The Munkres library in Python was used to compute the assignments.
The algorithm produces a list of doctors matched with hospitals as well as doctors that did not have a match (unmatched).

Munkres Explained

It is an algorithm based on the Hungarian algorithm that finds the minimum-cost assignment on a bipartite graph, represented as a cost matrix where rows are one partition (e.g., doctors), columns the other (e.g., hospitals), and each cell is the assignment cost. When multiple equal-cost matchings (ties) exist, the algorithm still returns one optimal assignment. The assignment that is given depends on the internal implementation details (e.g., the order in which rows/columns are processed, how augmenting paths are picked, or the order of scanning for zeros in the cost matrix). In our case, based on the source code, the algorithm scans rows top to bottom and columnns left to right. Once it finds the first feasible zero it stars it and breaks the loop. If multiple zeros are available, the lowest-indexed row gets served first, and within that row the lowest-indexed column is chosen. This is the primary tie-breaker. When multiple equally optimal matchings exist, such as in the case of the doctors ranking all the hospitals the same, it consistently favors assignments involving lower-indexed rows and columns.



## RESOURCES USED:
### Hungarian algorithm original paper
Harold W. Kuhn (1955). The Hungarian Method for the Assignment Problem. Naval Research Logistics Quarterly, 2(1–2), 83–97.

### Munkres explained
https://brilliant.org/wiki/hungarian-matching/

### Munkres package documentation
https://software.clapper.org/munkres/

### Munkres package source code
https://github.com/bmc/munkres/blob/master/munkres.py