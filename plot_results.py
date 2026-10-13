from pathlib import Path
import csv
import matplotlib.pyplot as plt


PROJECT_DIR = Path(__file__).resolve().parent
RESULTS_FILE = PROJECT_DIR / "results" / "summary.csv"
PLOTS_DIR = PROJECT_DIR / "plots"


def read_results():
    results = {
        "program1": [],
        "program2": [],
    }

    with RESULTS_FILE.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            program = row["program"]
            n = int(row["n"])
            k = int(row["k"])
            mean_seconds = float(row["mean_seconds"])

            results[program].append((n, k, mean_seconds))

    # sort by input size
    results["program1"].sort()
    results["program2"].sort()

    return results


def create_plot(rows, program_name, title, color):
    if len(rows) == 0:
        raise ValueError(f"No measurements found for {program_name}.")

    sizes = []
    times = []
    k = rows[0][1]

    for n, row_k, mean_seconds in rows:
        if row_k != k:
            raise ValueError("This plot expects k to stay fixed.")

        sizes.append(n)
        times.append(mean_seconds)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        sizes,
        times,
        marker="o",
        markersize=4,
        linewidth=2,
        color=color,
        label=f"k = {k}",
    )

    ax.set_title(title)
    ax.set_xlabel("Number of panels (n)")
    ax.set_ylabel("Average running time (seconds)")

    # start the axes at zero to make growth easier to compare
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    # keep input sizes readable instead of using scientific notation
    ax.ticklabel_format(style="plain", axis="x")
    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()

    fig.savefig(
        PLOTS_DIR / f"{program_name}_runtime.png",
        dpi=300,
    )
    fig.savefig(
        PLOTS_DIR / f"{program_name}_runtime.pdf",
    )

    plt.close(fig)

    print(f"Saved plots for {program_name}.")


def main():
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    results = read_results()

    create_plot(
        results["program1"],
        "program1",
        "Program 1 Runtime vs. Input Size",
        "tab:blue",
    )

    create_plot(
        results["program2"],
        "program2",
        "Program 2 Runtime vs. Input Size",
        "tab:orange",
    )


if __name__ == "__main__":
    main()