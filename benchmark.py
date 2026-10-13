from pathlib import Path
from time import perf_counter
import csv
import platform
import sys

from program1 import program1
from program2 import program2
from generate_inputs import SIZES, K, SAMPLES_PER_SIZE, SEED


TIMED_RUNS = 10

PROJECT_DIR = Path(__file__).resolve().parent
INPUT_DIR = PROJECT_DIR / "inputs"
RESULTS_DIR = PROJECT_DIR / "results"


def read_input(path):
    with path.open("r", encoding="utf-8") as file:
        n, k = map(int, file.readline().split())
        costs = list(map(int, file.readline().split()))

    return n, k, costs


def check_result(result, n, k, costs):
    # check route validity and the reported cost
    # this does not prove that the route is optimal
    total_cost, visited = result

    if len(visited) == 0 or visited[-1] != n:
        raise ValueError("The route must end on panel n.")

    previous = 0
    calculated_cost = 0

    for panel in visited:
        if panel < 1 or panel > n:
            raise ValueError("The route contains an invalid panel.")

        jump = panel - previous

        if jump < 1 or jump > k:
            raise ValueError("The route contains an invalid jump.")

        calculated_cost += costs[panel - 1]
        previous = panel

    if calculated_cost != total_cost:
        raise ValueError("The reported cost does not match the route.")


def measure_input(function, n, k, costs):
    # warm up the function and check its output outside the timer.
    result = function(n, k, costs)
    check_result(result, n, k, costs)
    del result

    times = []

    for run in range(TIMED_RUNS):
        start_time = perf_counter()

        result = function(n, k, costs)

        end_time = perf_counter()

        elapsed = end_time - start_time
        times.append(elapsed)

        # release the returned route outside the timed portion
        del result

    return times


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    raw_path = RESULTS_DIR / "raw_times.csv"
    summary_path = RESULTS_DIR / "summary.csv"

    programs = [
        ("program1", program1),
        ("program2", program2),
    ]

    with raw_path.open("w", newline="", encoding="utf-8") as raw_file:
        with summary_path.open(
            "w", newline="", encoding="utf-8"
        ) as summary_file:
            raw_writer = csv.writer(raw_file)
            summary_writer = csv.writer(summary_file)

            raw_writer.writerow([
                "program", "n", "k", "sample", "run", "seconds"
            ])

            summary_writer.writerow([
                "program", "n", "k", "measurements", "mean_seconds"
            ])

            for n in SIZES:
                for program_name, function in programs:
                    all_times = []

                    for sample in range(1, SAMPLES_PER_SIZE + 1):
                        filename = f"n{n}_sample{sample}.txt"
                        path = INPUT_DIR / program_name / filename

                        # file reading happens before timing
                        input_n, input_k, costs = read_input(path)

                        if input_n != n or input_k != K:
                            raise ValueError(
                                f"Unexpected n or k in {path}"
                            )

                        if len(costs) != n:
                            raise ValueError(
                                f"Incorrect number of costs in {path}"
                            )

                        times = measure_input(
                            function, input_n, input_k, costs
                        )

                        for run in range(len(times)):
                            raw_writer.writerow([
                                program_name,
                                n,
                                K,
                                sample,
                                run + 1,
                                times[run],
                            ])

                        all_times.extend(times)

                    mean_time = sum(all_times) / len(all_times)

                    summary_writer.writerow([
                        program_name,
                        n,
                        K,
                        len(all_times),
                        mean_time,
                    ])

                    print(
                        f"{program_name}, n = {n}, "
                        f"average = {mean_time:.8f} seconds"
                    )

    # save details
    metadata_path = RESULTS_DIR / "environment.txt"

    with metadata_path.open("w", encoding="utf-8") as file:
        file.write(f"Python version: {sys.version}\n")
        file.write(f"Platform: {platform.platform()}\n")
        file.write(f"Machine architecture: {platform.machine()}\n")
        file.write(f"Random seed: {SEED}\n")
        file.write(f"Input sizes: {list(SIZES)}\n")
        file.write(f"k: {K}\n")
        file.write(f"Datasets per size: {SAMPLES_PER_SIZE}\n")
        file.write(f"Timed runs per dataset: {TIMED_RUNS}\n")
        file.write("Warm-up runs per dataset: 1\n")
        file.write("Timer: perf_counter\n")
        file.write("Measured scope: algorithm function call\n")

    print("Finished. Measurements saved in the results folder.")


if __name__ == "__main__":
    main()