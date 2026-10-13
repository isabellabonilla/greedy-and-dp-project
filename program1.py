from typing import List, Tuple


def program1(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 1
    
    Parameters:
    n (int): number of panels
    k (int): maximum number of positions in a forward jump
    costs (List[int]): the landing costs of the panels

    Returns:
    int:  minimum total energy cost
    List[int]: the indices of the visited panels in increasing order(1-indexed, including n and excluding 0)
    """
    ############################
    
    # landing costs are monotonically non-increasing
    # example 2: n = 8, k = 3, c =[20,18,16,14,12,10,8,6]
    position = 0
    total_cost = 0 # ends at 32 = [16, 10, 6]
    visited = [] # ends as [3, 6, 8]

    while position < n:
        position = min(position + k, n) # move to farthest allowed panel
        total_cost += costs[position - 1] # add panel's cost to total 
        visited.append(position) # add panel num to visited

    ############################

    return total_cost, visited


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program1(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)