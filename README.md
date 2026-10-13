# COP4533: Algorithm Design & Analysis - Project 1

## Milestone 1 - Orbital Solar Array Inspection Robot

### Team

- Isabella Bonilla
- Jacqueline

We each implemented both programs independently, then compared our
approaches in person and agreed on the final implementations.

### Project Overview

The robot starts at position 0 and must reach panel n. It can jump
forward between 1 and k positions and pays a cost each time it lands
on a panel. The goal is to find a valid route with the lowest total
energy cost.

This milestone focuses on two restricted versions of the problem.

- Program 1 handles costs that never increase as we move right.
- Program 2 handles costs that rise toward one unique peak and then fall.

### Files

| File | Purpose |
|---|---|
| `program1.py` | Greedy solution for monotonically non-increasing costs |
| `program2.py` | Solution for single-peak costs |

### Requirements

The solution programs use Python 3.10 and the Python standard library.
No additional packages are needed to run them.

### Running the Programs

Run either command from the project folder.

```bash
python3 program1.py
```

```bash
python3 program2.py
```

Then enter two lines of input.

- The first line contains n and k.
- The second line contains the n landing costs.

For example, Program 1 accepts

```text
8 3
20 18 16 14 12 10 8 6
```

Its output is

```text
32
3
3
6
8
```

The first output line is the total energy cost. The second is the number
of visited panels. Each remaining line contains one visited panel index.
Panel n is included, and position 0 is excluded.

### Algorithm Runtimes

| Function | Runtime |
|---|---|
| `program1` | Θ(n/k) |
| `program2` | Θ(n) |

These bounds describe the functions themselves. Reading all panel costs
takes Θ(n) time for either program.

### Experimental Study

We will add runtime measurements and Matplotlib plots to examine how
each algorithm's running time changes as the input size increases.
