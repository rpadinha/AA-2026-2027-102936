import csv
import time
import argparse
from pathlib import Path

from src.graph_io import load_graph
from src.exhaustive import exhaustive_search
from src.greedy import greedy_basic_search, greedy_ratio_search

BASE_DIR = Path(__file__).parent.parent

GRAPH_DIR = BASE_DIR / "data" / "graphs" / "synthetic"
RESULTS_FILE = BASE_DIR / "data" / "results.csv"

TIME_LIMIT = 30                     # 30 sec timeout starter

PROBLEM_ID = "P25"                  # problem id -> P25: MWDS
PROJECT_PHASE = "P1"                # project phase -> p1

CSV_HEADERS = [
    "student_id", "problem_id", "project_phase", "N", "density", "seed", 
    "solver_type", "basic_ops", "execution_time_sec", "tested_configs", 
    "solution_quality", "optimality_gap_pct", "status"
]

def save_results(results):
    """ Append benchmark results to CSV. """

    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    file_exists = RESULTS_FILE.exists()

    with open(RESULTS_FILE, "a", newline='') as file:

        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)

        # write the header if it doesnt exist
        if not file_exists or RESULTS_FILE.stat().st_size == 0:
            writer.writeheader()

        writer.writerows(results)

def benchmark_graph(G, filename, student_id):
    """ 
    Benchmark exhaustive, greedy basic, and greedy ratio search on one graph. 
    Returns all three results in a list.
    """

    # Extract graph information from filename
    parts = filename.replace(".graphml", "").split("_")
    n = int(parts[1])
    density = int(parts[2]) / 1000.0
    print(f"\nBenchmarking graph: {n} vertices with {density} edges")
    seed = student_id

    results = []

    # exhaustive search for G
    start_time = time.perf_counter()
    exhaustive_result = exhaustive_search(
                        G, 
                        time_limit_sec=TIME_LIMIT) # added this for exhaustive because 2^n possibilities, it scales up pretty fast
    exhaustive_time = time.perf_counter() - start_time
    # check if exhaustive timed out
    exhaustive_status = (
        "TIMEOUT"
        if exhaustive_result["timed_out"]
        else "SUCCESS"
    )

    # greedy basic search for G (unweighted span heuristic)
    start_time = time.perf_counter()
    greedy_basic_result = greedy_basic_search(G)
    greedy_basic_time = time.perf_counter() - start_time

    # greedy ratio search for G (cost/coverage heuristic)
    start_time = time.perf_counter()
    greedy_ratio_result = greedy_ratio_search(G)
    greedy_ratio_time = time.perf_counter() - start_time

    # optimal gap calculations for both greedy heuristics
    basic_gap = None
    ratio_gap = None

    if exhaustive_status == "SUCCESS":
        optimal_cost = exhaustive_result["solution_quality"]
        basic_cost = greedy_basic_result["solution_quality"]
        ratio_cost = greedy_ratio_result["solution_quality"]

        if optimal_cost > 0:
            basic_gap = (abs(basic_cost - optimal_cost) / optimal_cost) * 100
            ratio_gap = (abs(ratio_cost - optimal_cost) / optimal_cost) * 100
        else:
            basic_gap = 0.0
            ratio_gap = 0.0

    # append the exhaustive search result
    results.append({
        "student_id": student_id,
        "problem_id": PROBLEM_ID,
        "project_phase": PROJECT_PHASE,
        "N": n,
        "density": density,
        "seed": seed,
        "solver_type": "Exhaustive_Bitmask",
        "basic_ops": exhaustive_result["basic_ops"],
        "execution_time_sec": round(exhaustive_time, 6),
        "tested_configs": exhaustive_result["tested_configs"],
        "solution_quality": (
            exhaustive_result["solution_quality"]
            if exhaustive_result["solution_quality"] != float('inf')
            else ""
        ),
        "optimality_gap_pct": (
            0.0 if exhaustive_status == "SUCCESS" else ""
        ),
        "status": exhaustive_status
    })

    # append the greedy basic search result
    results.append({
        "student_id": student_id,
        "problem_id": PROBLEM_ID,
        "project_phase": PROJECT_PHASE,
        "N": n,
        "density": density,
        "seed": seed,
        "solver_type": "Greedy_Basic",
        "basic_ops": greedy_basic_result["basic_ops"],
        "execution_time_sec": round(greedy_basic_time, 6),
        "tested_configs": greedy_basic_result["tested_configs"],
        "solution_quality": greedy_basic_result["solution_quality"],
        "optimality_gap_pct": (
            round(basic_gap, 4)
            if basic_gap is not None else ""
        ),
        "status": "SUCCESS"
    })

    # append the greedy ratio search result
    results.append({
        "student_id": student_id,
        "problem_id": PROBLEM_ID,
        "project_phase": PROJECT_PHASE,
        "N": n,
        "density": density,
        "seed": seed,
        "solver_type": "Greedy_Ratio",
        "basic_ops": greedy_ratio_result["basic_ops"],
        "execution_time_sec": round(greedy_ratio_time, 6),
        "tested_configs": greedy_ratio_result["tested_configs"],
        "solution_quality": greedy_ratio_result["solution_quality"],
        "optimality_gap_pct": (
            round(ratio_gap, 4)
            if ratio_gap is not None else ""
        ),
        "status": "SUCCESS"
    })

    return results

def run_benchmarks(student_id):
    """ Main function to call benchmark graph for all graphs in synthetic folder. """

    graph_files = sorted(
    GRAPH_DIR.glob("graph_*.graphml"),
    key=lambda p: (
        int(p.stem.split("_")[1]), 
        int(p.stem.split("_")[2])
        )
    )

    if not graph_files:
        raise FileNotFoundError(f"No synthetic graphs found in {GRAPH_DIR}. \n Generate them first using:\n python -m src.utils --seed 12345\n")

    print(f"Graphs being benchmarked: {len(graph_files)}")
    print(f" {"~" * 15} P1 Benchmarks for {student_id} with time limit of {TIME_LIMIT} {"~" * 15}")


    for index, filepath in enumerate(graph_files, start=1):
        print(f"\nGraph {index}/{len(graph_files)}")

        G = load_graph(str(filepath))

        graph_results = benchmark_graph(
                                    G,
                                    filepath.name,
                                    student_id
        )

        save_results(graph_results)

    print(f" {"~" * 40} Benchmarks completed {"~" * 40}")
    print(f"Results saved: {RESULTS_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run P1 algorithm benchmarks."
    )

    parser.add_argument(
        "--student-id",
        type=int,
        required=True,
        help="Student ID used to generate synthetic graphs."
    )

    args = parser.parse_args()

    run_benchmarks(args.student_id)