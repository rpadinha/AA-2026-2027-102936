# Advanced Algorithms (2026/2027) — Student Project Repository Starter

Welcome to your **Advanced Algorithms** project repository! This repository serves as the starter template and workspace for both **Project 1** (Exhaustive Search & Greedy Baselines) and **Project 2** (Refined Heuristics & Randomized Approximations).

---

## 1. Student & Project Identification

* **Student Name:** Rui Alexandre Oliveira Padinha
* **Student ID / Seed:** 102936
* **Course:** M.Sc. in Computational Engineering
* **Assigned Problem ID & Name:** P25 - Min Weight Dominating Set
* **Problem Type:** Optimization
* **Graph Type:** Undirected Graph

---

## 2. Domain Application & Hand-Crafted Instances

### Real-World Application
* **Domain Context:** Describe 1–2 real-world applications of your assigned problem (if possible) relevant to your degree course or engineering domain.
* **Motivation:** Explain why solving this problem matters in practice.

### Hand-Crafted Toy Instances
* Small hand-crafted test instances ($N \le 8$) must be placed in `data/graphs/handmade/`.
* These instances include manual ground-truth solutions used by `tests/test_against_handmade.py` to verify algorithm correctness before executing large experimental sweeps.

---

## 3. Directory Structure

This repository follows a strict modular separation of concerns:

```text
AA-2026-2027-StudentNumber/
├── src/                        # Core algorithmic & problem logic (Python modules)
│   ├── __init__.py
│   ├── problem.py              # Problem formulation, state representation, & validators
│   ├── exhaustive.py           # Exhaustive search, bitmasking, & backtracking solvers
│   ├── greedy.py               # Greedy baseline heuristic implementations
│   ├── graph_io.py             # NetworkX I/O functions (.graphml, .json)
│   └── utils.py                # 2D coordinate graph generators (student seed)
├── experiments/                # Execution & benchmarking runners
│   ├── run_p1_benchmarks.py    # Project 1 benchmark sweep runner
│   └── run_p2_benchmarks.py    # Project 2 benchmark sweep runner
├── data/                       # Experimental instances & structured log results
│   ├── graphs/                 
│   │   ├── handmade/           # Hand-crafted small graphs for unit testing
│   │   └── synthetic/          # Generated 2D coordinate graphs
│   └── results.csv             # Structured benchmark logs
├── notebooks/                  # Visualization & exploratory analysis ONLY
│   └── main_analysis.ipynb     # Performance plots (Time vs N, Log scales, Optimality gap)
├── docs/                       # Course deliverables
│   ├── p1/
│   │   ├── report_p1.pdf       # Project 1 PDF report (8-page limit)
│   │   ├── slides_p1.pdf       # Project 1 defense presentation
│   │   └── demo_notes_p1.pdf   # Project 1 live demo execution instructions
│   └── p2/
│       ├── report_p2.pdf       # Project 2 PDF report (8-page limit)
│   │   ├── slides_p2.pdf       # Project 2 defense presentation
│   │   └── demo_notes_p2.pdf   # Project 2 live demo execution instructions
├── tests/                      # Automated unit test suite
│   └── test_against_handmade.py# Pytest suite verifying solver correctness
├── .gitignore                  # Git exclusion rules
├── requirements.txt            # Python dependencies
└── README.md                   # This instruction file
```

---

## 4. Setup & Installation

### Prerequisites
* Python 3.10+ installed on your local system.

### Environment Setup
1. Clone your private repository:
   ```bash
   git clone <your-repository-url>
   cd AA-2026-2027-12345
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # On Linux/macOS
   # venv\Scripts\activate          # On Windows
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 5. Running Tests & Benchmarks

### Step 1: Run Unit Tests
Verify solver correctness against your hand-crafted instances:
```bash
pytest tests/
```

### Step 2: Generate 2D Benchmark Graphs
Generate synthetic 2D spatial graphs seeded by your student number:
```bash
python -m src.utils --seed 12345
```

### Step 3: Run Benchmark Sweeps
Execute benchmark sweeps across vertex counts $N$ and density levels (12.5%, 25%, 50%, 75%):
```bash
python -m experiments.run_p1_benchmarks
```
All benchmark logs will be saved automatically to `data/results.csv`.

---

## 6. Experimental Benchmarking Schema (`data/results.csv`)

Every experimental run appends a log entry to `data/results.csv` with the following schema:

| Column | Description |
| :--- | :--- |
| `student_id` | Your student number |
| `problem_id` | Assigned problem ID (e.g., `P02`) |
| `project_phase` | `P1` or `P2` |
| `N` | Number of vertices |
| `density` | Graph edge density (`0.125`, `0.25`, `0.50`, `0.75`) |
| `seed` | Random seed used for generation |
| `solver_type` | `Exhaustive_Bitmask`, `Backtracking_Pruned`, `Greedy_Basic`, etc. |
| `basic_ops` | Counter of fundamental operations (e.g., state checks, bitwise ops) |
| `execution_time_sec` | Execution time recorded via `time.perf_counter()` |
| `tested_configs` | Total number of candidate solutions/states evaluated |
| `solution_quality` | Optimal value $S^*$ or heuristic value found |
| `optimality_gap_pct` | Gap percentage: $\frac{\|S_{greedy} - S^*\|}{S^*} \times 100\%$ |
| `status` | `SUCCESS` or `TIMEOUT` (if execution exceeded time limit) |

---

## 7. Submission Checklist

Before submitting your final project commit:
- [ ] Ensure all code in `src/` is well-documented, clean, and importable.
- [ ] Verify that `tests/test_against_handmade.py` passes without errors.
- [ ] Confirm `data/results.csv` contains complete experimental runs.
- [ ] Place your final 8-page PDF report in `docs/p1/report_p1.pdf` (or `docs/p2/report_p2.pdf`).
- [ ] Verify that the lecturer has Viewer access to your private GitHub repository.
- [ ] Include your repository URL and final submission Git commit hash on the report cover page.

---

## 8. Generative AI Usage Policy

Generative AI tools (ChatGPT, GitHub Copilot, Gemini, Claude, etc.) are recognized as software engineering and technical writing assistants under the following strict boundaries:

### The "Traffic Light" Policy Matrix
* 🟢 **GREEN LIGHT (Allowed & Encouraged — No Citation Required):** Conceptual learning, syntax lookups, execution error debugging, and language/grammar polishing of your original text.
* 🟡 **YELLOW LIGHT (Permitted WITH Mandatory Disclosure):** Boilerplate code generation (CLI parsers, CSV logging, plot layout) and code refactoring suggestions. **Requirements:** You must fully understand every line, verify it against hand-crafted test cases, and disclose its usage in your report and code comments.
* 🔴 **RED LIGHT (Strictly Prohibited — Academic Misconduct):** Direct generation of core solver logic (exhaustive backtracking, or greedy heuristics) without personal implementation, data fabrication/falsification in `data/results.csv`, submitting unverified AI text/equations, or passing off AI work as original unassisted effort.

### Mandatory Disclosure Protocol
1. **Report Declaration:** Include a "Generative AI Declaration" section or appendix in `docs/p1/report_p1.pdf` (and `docs/p2/report_p2.pdf`) listing tools used, scope of assistance, and a statement confirming that all AI-generated code/text was manually verified.
2. **In-Code Annotations:** Add an inline comment above any AI-assisted function:
   ```python
   # AI-Assisted: Generated boilerplate for matplotlib multi-panel figure layout.
   # Tool: ChatGPT-4o | Prompt: "Create a 2x2 grid plot in matplotlib"
   # Verified and modified by: Student #12345
   def plot_benchmark_results(df: pd.DataFrame) -> None:
       ...
   ```

### The Accountability Principle
**You are 100% accountable for all report contents, every line of code, equation, figure, and claim submitted under your name.**

During the live oral defense and repository evaluation, you may be asked to explain the exact mechanics of any function in `src/`, modify a solver live, or trace an execution loop. Inability to explain submitted code—regardless of source—will result in a **zero grade for the algorithmic implementation component** and may trigger further integrity review.
