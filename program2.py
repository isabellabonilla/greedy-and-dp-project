from typing import List, Tuple


def program2(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 2
    
    Parameters:
    n (int): number of panels
    k (int): maximum number of positions in a forward jump
    costs (List[int]): the landing costs of the panels

    Returns:
    int:  minimum total energy cost
    List[int]: the indices of the visited panels in increasing order(1-indexed, including n and excluding 0)
    """
    ############################

    # unique peak index - before peak: backward w biggest allowed jumps, after peak: forward w biggest allowed jumps
    # example 3: n = 10, k = 4, c =[1,2,4,9,12,10,6,4,3,1]

    # find best first panel to land on
    best_cost = float("inf")
    best_start = 1

    for start in range(1, k + 1): # every possible first landing
        candidate_cost = costs[n - 1] # all possible starts will have the cost at the goal panel n

        for panel in range(start, n, k): # in between landings before getting to n panel
            candidate_cost += costs[panel - 1]

        if candidate_cost < best_cost: # 11 = [4, 6, 1]
            best_cost = candidate_cost
            best_start = start # panel 3

    visited = [] # [3, 7, 10]
    position = best_start

    while position < n:
        visited.append(position)
        position += k

    visited.append(n) # include the last goal panel n

    ############################

    return best_cost, visited


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program2(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)