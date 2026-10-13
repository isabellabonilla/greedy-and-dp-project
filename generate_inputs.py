from pathlib import Path
import random


SEED = 4533
K = 10
SIZES = range(5_000, 100_000, 5_000)
SAMPLES_PER_SIZE = 5

# save inputs beside this script, inside the inputs folder
PROJECT_DIR = Path(__file__).resolve().parent
INPUT_DIR = PROJECT_DIR / "inputs"


def generate_decreasing_costs(n, rng):
    costs = []

    for i in range(n):
        costs.append(rng.randint(1, 99_999))

    # largest to smallest, so costs never increase
    costs.sort(reverse=True)

    return costs


def generate_single_peak_costs(n, rng):
    # keep the peak away from the first and last panels
    peak_index = rng.randint(1, n - 2)

    left = []
    right = []

    for i in range(peak_index):
        left.append(rng.randint(1, 99_998))

    for i in range(n - peak_index - 1):
        right.append(rng.randint(1, 99_998))

    # costs rise toward the peak and fall after it
    left.sort()
    right.sort(reverse=True)

    # all other costs are below 99,999, making this peak unique
    costs = left + [99_999] + right

    return costs


def validate_costs(costs, n, single_peak=False):
    # check the input size, jump limit, and cost bounds
    if len(costs) != n:
        raise ValueError("The number of costs must equal n.")

    if not (1 <= K <= n < 100_000):
        raise ValueError("The input must satisfy 1 <= k <= n < 100,000.")

    for cost in costs:
        if cost < 1 or cost >= 100_000:
            raise ValueError("Each cost must be between 1 and 99,999.")

    if single_peak:
        peak_cost = max(costs)
        peak_index = costs.index(peak_cost)

        if peak_index == 0 or peak_index == n - 1:
            raise ValueError("The peak cannot be the first or last panel.")

        if costs.count(peak_cost) != 1:
            raise ValueError("There must be exactly one highest-cost panel.")

        # before peak, costs cannot decrease
        for i in range(peak_index):
            if costs[i] > costs[i + 1]:
                raise ValueError("Costs must not decrease before the peak.")

        # after peak, costs cannot increase
        for i in range(peak_index, n - 1):
            if costs[i] < costs[i + 1]:
                raise ValueError("Costs must not increase after the peak.")

    else:
        # prog 1 costs cannot increase anywhere
        for i in range(n - 1):
            if costs[i] < costs[i + 1]:
                raise ValueError("Program 1 costs must never increase.")


def write_input(path, n, costs):
    with path.open("w", encoding="utf-8") as file:
        file.write(f"{n} {K}\n")

        # convert the costs to text so we can join them with spaces
        cost_strings = []

        for cost in costs:
            cost_strings.append(str(cost))

        file.write(" ".join(cost_strings) + "\n")


def main():
    # fixed seed makes the random inputs reproducible
    rng = random.Random(SEED)

    program1_dir = INPUT_DIR / "program1"
    program2_dir = INPUT_DIR / "program2"

    program1_dir.mkdir(parents=True, exist_ok=True)
    program2_dir.mkdir(parents=True, exist_ok=True)

    file_count = 0

    for n in SIZES:
        for sample in range(1, SAMPLES_PER_SIZE + 1):
            filename = f"n{n}_sample{sample}.txt"

            # generate, check, and save the prog 1 input
            costs1 = generate_decreasing_costs(n, rng)
            validate_costs(costs1, n)
            write_input(program1_dir / filename, n, costs1)

            # generate, check, and save the prog 2 input
            costs2 = generate_single_peak_costs(n, rng)
            validate_costs(costs2, n, single_peak=True)
            write_input(program2_dir / filename, n, costs2)

            file_count += 2

        print(f"Generated inputs for n = {n}")

    print(f"Finished. Created or replaced {file_count} input files.")


if __name__ == "__main__":
    main()