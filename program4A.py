from typing import List, Tuple


def program4A(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 4A
    
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

    memo = {} # memo table, tracks panel index to its result as a tuple

    def solve(current_panel: int) -> Tuple[int, List[int]]:
    # base case where if we've reached panel n, cost is 0 and no more panels need to be covered
        if current_panel == n: 
            return 0, []
    # check if best path has already been calculated for this curr panel, can just read it from memo table
        if current_panel in memo:
            return memo[current_panel]

        min_cost = float('inf')
        best_path = []

        # now loop going 1 up to k steps forward, but not past last one
        for jump in range(1, k+1):
            next_panel = current_panel + jump

            if next_panel > n:
                break

            # now recursively find cost and path for the rest of the way from next_panel
            future_cost, future_path = solve(next_panel)

            # store cost of next_panel, and check if it was cheaper overall, update records if so
            total_cost = costs[next_panel - 1] + future_cost
            if total_cost < min_cost:
                min_cost = total_cost
                best_path = [next_panel] + future_path

        # outside of loop, save the best outcome to table before returning value
        memo[current_panel] = (min_cost, best_path)
        return memo[current_panel]




    return solve(0)


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program4A(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)