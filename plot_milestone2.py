"""Generate Milestone 2 Plots 3–9 from the project root."""

import csv
from pathlib import Path
from statistics import mean
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

from milestone2_pilot import check_result, generate_input, read_input, validate_example
from program1 import program1
from program5 import program5


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "plots" / "milestone2"
BATCHES = ("m2-small", "m2-dp")
PROGRAMS = {
    "program3": ("Program 3", "tab:blue", "o"),
    "program4A": ("Program 4A", "tab:orange", "s"),
    "program4B": ("Program 4B", "tab:green", "^"),
    "program5": ("Program 5", "tab:red", "D"),
}


def load_runtime_data():
    timings = {program: {} for program in PROGRAMS}
    summaries = [ROOT / batch / "summary.csv" for batch in BATCHES]
    extension = ROOT / "m2-extension" / "summary.csv"
    if extension.is_file():
        summaries.append(extension)

    for summary in summaries:
        with summary.open(newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                n = int(row["n"])
                k = int(row["k"])
                seconds = float(row["mean_seconds"])
                series = timings[row["program"]]
                if k != (n + 9) // 10 or seconds <= 0 or n in series:
                    raise ValueError(f"Unexpected or duplicate timing row in {summary}: {row}")
                series[n] = seconds

    small_sizes = timings["program3"].keys()
    if not small_sizes or any(not small_sizes <= series.keys() for series in timings.values()):
        raise ValueError("All four programs need results for the shared small input sizes.")
    if timings["program4A"].keys() != timings["program4B"].keys():
        raise ValueError("Programs 4A and 4B need results at the same input sizes.")
    return timings


def draw_series(ax, program, timings):
    label, color, marker = PROGRAMS[program]
    series = timings[program]
    sizes = sorted(series)
    ax.plot(sizes, [series[n] for n in sizes], label=label, color=color, marker=marker, clip_on=False)


def format_axis(ax, title, ylabel="Mean runtime (seconds)"):
    ax.set(title=title, xlabel="Number of panels (n)", ylabel=ylabel)
    ax.grid(True, alpha=0.25)


def save_figure(fig, number):
    for extension in ("png", "pdf"):
        fig.savefig(OUTPUT / f"plot{number}.{extension}", dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_runtimes(timings):
    comparison_limit = max(timings["program4A"])
    for number, program in enumerate(PROGRAMS, start=3):
        fig, ax = plt.subplots(figsize=(7, 4))
        draw_series(ax, program, timings)
        format_axis(ax, f"{PROGRAMS[program][0]} runtime")
        ax.set(xlim=(0, comparison_limit), ylim=(0, None))
        if program == "program3":
            last = max(timings[program])
            seconds = timings[program][last]
            ax.annotate(
                f"Last measured point: n = {last} ({seconds:.2f} s)",
                xy=(last, seconds),
                xytext=(20, -12),
                textcoords="offset points",
                va="top",
                arrowprops={"arrowstyle": "-"},
            )
        save_figure(fig, number)

    fig, ax = plt.subplots(figsize=(8.5, 4.8), layout="constrained")
    shared_sizes = sorted(timings["program3"])
    for program in PROGRAMS:
        draw_series(ax, program, timings)
    first, last = shared_sizes[0], shared_sizes[-1]
    ax.axvspan(first, last, color="0.9", zorder=0, label=f"All four ran at n = {first}–{last}")
    format_axis(ax, "Runtime comparison across all four programs")
    ax.set(xlim=(0, comparison_limit), yscale="log")
    ax.legend(loc="upper right")
    save_figure(fig, 7)

    fig, ax = plt.subplots(figsize=(7, 4))
    for program in ("program4A", "program4B"):
        draw_series(ax, program, timings)
    format_axis(ax, "Top-down vs. bottom-up dynamic programming")
    ax.set_ylim(bottom=0)
    ax.legend()
    save_figure(fig, 8)


def plot_cost_gap():
    validate_example("program5", program5)
    sizes = range(1_000, 10_001, 1_000)
    mean_gaps = []
    with TemporaryDirectory() as directory, (
        OUTPUT / "plot9_costs.csv"
    ).open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["n", "k", "sample", "greedy_cost", "optimal_cost", "relative_excess"])
        path = Path(directory) / "input.txt"
        for n in sizes:
            k = (n + 9) // 10
            gaps = []
            for sample in range(1, 51):
                generate_input(path, n, k, sample)
                case = read_input(path)
                greedy = program1(*case)
                optimal = program5(*case)
                check_result(greedy, *case)
                check_result(optimal, *case)
                if not 0 < optimal[0] <= greedy[0]:
                    raise ValueError(f"Invalid cost comparison for n={n}, sample={sample}")
                gap = (greedy[0] - optimal[0]) / optimal[0]
                gaps.append(gap)
                writer.writerow([n, k, sample, greedy[0], optimal[0], gap])
            mean_gaps.append(mean(gaps))

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(sizes, mean_gaps, marker="o")
    format_axis(ax, "Greedy cost compared with optimal", "Mean relative excess cost")
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.set_ylim(bottom=0)
    save_figure(fig, 9)


def main():
    timings = load_runtime_data()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    plot_runtimes(timings)
    plot_cost_gap()
    print(f"Saved Plots 3–9 and Plot 9 cost data to {OUTPUT}")


if __name__ == "__main__":
    main()
