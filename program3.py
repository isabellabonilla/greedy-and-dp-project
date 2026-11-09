from typing import List, Tuple


def program3(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 3
    
    Parameters:
    n (int): number of panels
    k (int): maximum number of positions in a forward jump
    costs (List[int]): the landing costs of the panels

    Returns:
    int:  minimum total energy cost
    List[int]: the indices of the visited panels in increasing order(1-indexed, including n and excluding 0)
    """
    ############################

    def min_cost(panel):

        # starting pos has no landing cost
        if panel == 0:
            return 0, []

        best_cost = float("inf")
        best_route = []

        # check every panel we could have jumped from
        for prev in range(max(0, panel - k), panel):
            prev_cost, prev_route = min_cost(prev) # recursively find the best cost and route to the prev panel

            # add cost of landing on curr panel
            total_cost = prev_cost + costs[panel - 1]

            if total_cost < best_cost:
                best_cost = total_cost
                best_route = prev_route + [panel]

        return best_cost, best_route
    
    ############################

    return min_cost(n) # call helper function with the last panel as the target


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program3(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)