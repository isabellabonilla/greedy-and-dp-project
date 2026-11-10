from typing import List, Tuple


def program4B(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 4B
    
    Parameters:
    n (int): number of panels
    k (int): maximum number of positions in a forward jump
    costs (List[int]): the landing costs of the panels

    Returns:
    int:  minimum total energy cost
    List[int]: the indices of the visited panels in increasing order(1-indexed, including n and excluding 0)
    """
    ############################
    # Add your code here
    ############################

    # dp[i] stores min cost to reach panel i from panel 0, parent[i] stores panel we jumped FROM to reach panel i
    dp = [float('inf')] * (n + 1)
    parent = [-1] * (n + 1)
    
    # base case here starting at position 0 costs nothing, then outer loop will build up the rest of the table
    dp[0] = 0
    for i in range(1, n + 1):
        
        # inner loop looks backward at the previous k panels to see which had the cheapest jump
        for j in range(max(0, i - k), i):
            
            # cost to reach panel i if we jumped from panel j, update if jumping from j is cheaper than our recorded best way to reach i
            current_cost = dp[j] + costs[i - 1]
            if current_cost < dp[i]:
                dp[i] = current_cost
                parent[i] = j
                
    # path reconstruction with breadcrumbs backward from n to 0
    path = []
    current = n
    
    while current != 0:
        path.append(current)
        current = parent[current]
        
    path.reverse()
    
    return dp[n], path


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program4B(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)