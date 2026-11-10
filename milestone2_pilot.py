"""Run this file from the project root alongside benchmark.py."""

import argparse
import csv
from importlib import import_module
from pathlib import Path
import platform
import random
import sys
from time import perf_counter

from benchmark import check_result, read_input
from generate_inputs import SEED


PROGRAMS = ("3", "4A", "4B", "5")
SMALL_SIZES = (12, 14, 16, 18, 20, 22, 24)
EXAMPLE = (7, 3, [7, 2, 9, 4, 1, 8, 3])


def generate_input(path, n, k, sample):
    # Make each input reproducible even when we run a different subset of sizes.
    rng = random.Random(f"{SEED}:{n}:{k}:{sample}")
    costs = [rng.randint(1, 99_999) for _ in range(n)]
    path.write_text(f"{n} {k}\n" + " ".join(map(str, costs)) + "\n", encoding="utf-8")


def validate_example(name, solve):
    result = solve(*EXAMPLE)
    try:
        check_result(result, *EXAMPLE)
        if result[0] != 6:
            raise ValueError(f"expected cost 6, got {result[0]}")
    except ValueError as error:
        raise SystemExit(f"{name} failed the assignment example: {error}") from error


def benchmark(args, solvers):
    output = args.output
    output.mkdir(parents=True)
    inputs = output / "inputs"
    inputs.mkdir()

    (output / "environment.txt").write_text(
        f"Python: {sys.version}\nPlatform: {platform.platform()}\n"
        f"Seed: {SEED}\nSizes: {args.sizes}\nk: ceil(n/10)\n"
        f"Datasets per size: {args.samples}\nTimed calls per dataset: {args.runs}\n"
        "Warm-up calls per dataset: 1\nTimer: perf_counter\n"
        "Timed scope: solver call, including route construction\n",
        encoding="utf-8",
    )

    with (output / "raw_times.csv").open("w", newline="", encoding="utf-8") as raw, (
        output / "summary.csv"
    ).open("w", newline="", encoding="utf-8") as summary:
        raw_writer = csv.writer(raw)
        summary_writer = csv.writer(summary)
        raw_writer.writerow(["program", "n", "k", "sample", "run", "seconds"])
        summary_writer.writerow(["program", "n", "k", "measurements", "mean_seconds"])

        for n in args.sizes:
            k = (n + 9) // 10
            times = {name: [] for name in solvers}
            for sample in range(1, args.samples + 1):
                path = inputs / f"n{n}_k{k}_sample{sample}.txt"
                generate_input(path, n, k, sample)
                case = read_input(path)
                costs = {}
                for name, solve in solvers.items():
                    # Use the untimed warm-up to check the route and reported cost.
                    try:
                        result = solve(*case)
                        check_result(result, *case)
                    except (ValueError, RecursionError) as error:
                        raise SystemExit(f"{name} failed on {path.name}: {error}") from error
                    costs[name] = result[0]
                    del result

                if len(set(costs.values())) != 1:
                    raise SystemExit(f"Optimal costs disagree on {path.name}: {costs}")

                for run in range(1, args.runs + 1):
                    for name, solve in solvers.items():
                        start = perf_counter()
                        result = solve(*case)
                        elapsed = perf_counter() - start
                        del result
                        times[name].append(elapsed)
                        raw_writer.writerow([name, n, k, sample, run, elapsed])

            for name, measurements in times.items():
                mean = sum(measurements) / len(measurements)
                summary_writer.writerow([name, n, k, len(measurements), mean])
                print(f"{name}  n={n:>5}  k={k:>4}  {mean:.8f} s", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--programs", nargs="+", choices=PROGRAMS, default=PROGRAMS)
    parser.add_argument("--sizes", nargs="+", type=int, default=SMALL_SIZES)
    parser.add_argument("--samples", type=int, default=1)
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True, help="New output directory")
    args = parser.parse_args()

    args.sizes = sorted(set(args.sizes))
    if any(not 1 <= n < 100_000 for n in args.sizes):
        parser.error("sizes must be between 1 and 99,999")
    if "3" in args.programs and max(args.sizes) > 30:
        parser.error("this pilot caps Program 3 at n=30 to limit exponential runs")
    if min(args.samples, args.runs) < 1:
        parser.error("samples and runs must both be positive")
    if args.output.exists():
        parser.error("choose a new output directory to preserve previous results")

    solvers = {}
    for program in args.programs:
        name = f"program{program}"
        solve = getattr(import_module(name), name)
        validate_example(name, solve)
        solvers[name] = solve

    benchmark(args, solvers)


if __name__ == "__main__":
    main()
