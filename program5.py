from typing import List, Tuple
from collections import deque


def program5(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 5
    
    Parameters:
    n (int): number of panels
    k (int): maximum number of positions in a forward jump
    costs (List[int]): the landing costs of the panels

    Returns:
    int:  minimum total energy cost
    List[int]: the indices of the visited panels in increasing order(1-indexed, including n and excluding 0)
    """
    ############################

    # O(n) to initialize dp and parent arrays
    dp = [float('inf')] * (n + 1) # stores min cost to reach panel i
    parent = [-1] * (n + 1) # stores prev panel on cheapest path

    dp[0] = 0
    candidates = deque([0]) # stores possible prev panels to jump from

    # O(n) to process each panel + O(k) to maintain candidates deque = total O(n)
    for i in range(1, n + 1):
        # remove panels from candidates that are too far back to jump from
        while candidates and candidates[0] < i - k:
            candidates.popleft()

        # best prev panel to jump from is at the front
        best_prev = candidates[0]
        dp[i] = dp[best_prev] + costs[i - 1]
        parent[i] = best_prev

        # remove candidates that are no longer better options
        while candidates and dp[candidates[-1]] >= dp[i]:
            candidates.pop()

        candidates.append(i) # add curr panel to candidates for future jumps

    # O(n) to reconstruct path
    # path reconstruction going backward
    path = []
    current = n
    
    while current != 0:
        path.append(current)
        current = parent[current]
        
    path.reverse()

    ############################

    return dp[n], path


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program5(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)