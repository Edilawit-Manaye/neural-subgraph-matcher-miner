import sys
import os
import pickle
import csv
import re


def extract_runtime(log_path):
    if not os.path.exists(log_path):
        return None
    with open(log_path, 'r') as f:
        content = f.read()
    m = re.search(r'Total time:\s*([\d.]+)s', content)
    if m:
        return float(m.group(1))
    return None


def count_patterns(pkl_path):
    if not os.path.exists(pkl_path):
        return 0
    with open(pkl_path, 'rb') as f:
        data = pickle.load(f)
    return len(data)


def main():
    if len(sys.argv) < 11:
        print("Usage: collect_metrics.py <log_path> <pkl_path> <strategy> <config_name> <n_trials> <n_neighborhoods> <min_neighborhood_size> <max_neighborhood_size> <radius> <csv_path>")
        sys.exit(1)

    log_path = sys.argv[1]
    pkl_path = sys.argv[2]
    strategy = sys.argv[3]
    config_name = sys.argv[4]
    n_trials = sys.argv[5]
    n_neighborhoods = sys.argv[6]
    min_neighborhood_size = sys.argv[7]
    max_neighborhood_size = sys.argv[8]
    radius = sys.argv[9]
    csv_path = sys.argv[10]

    runtime = extract_runtime(log_path)
    num_patterns = count_patterns(pkl_path)

    write_header = not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0
    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow([
                'strategy', 'config_name', 'n_trials', 'n_neighborhoods',
                'min_neighborhood_size', 'max_neighborhood_size', 'radius',
                'runtime_sec', 'num_patterns'
            ])
        writer.writerow([
            strategy, config_name, n_trials, n_neighborhoods,
            min_neighborhood_size, max_neighborhood_size, radius,
            runtime if runtime is not None else '',
            num_patterns
        ])


if __name__ == '__main__':
    main()
