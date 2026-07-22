import os
import csv
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns


CSV_PATH = 'results/benchmark_results.csv'
OUT_DIR = 'plots/cluster'
BEST_CONFIG_PATH = 'results/best_config.json'


def ensure_dirs():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(BEST_CONFIG_PATH), exist_ok=True)


def load_results():
    rows = []
    if not os.path.exists(CSV_PATH):
        return rows
    with open(CSV_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key in ['n_trials', 'n_neighborhoods', 'min_neighborhood_size', 'max_neighborhood_size', 'radius', 'runtime_sec', 'num_patterns']:
                if row.get(key) == '':
                    row[key] = None
                else:
                    try:
                        row[key] = float(row[key]) if '.' in str(row[key]) else int(row[key])
                    except ValueError:
                        row[key] = None
            rows.append(row)
    return rows


def plot_runtime_vs_strategy(rows):
    if not rows:
        return
    plt.figure(figsize=(10, 6))
    sns.barplot(data=rows, x='strategy', y='runtime_sec', hue='config_name')
    plt.title('Runtime vs Search Strategy')
    plt.ylabel('Runtime (seconds)')
    plt.xlabel('Search Strategy')
    plt.legend(title='Config')
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'runtime_vs_strategy.png')
    plt.savefig(path)
    plt.close()
    print(f'Saved {path}')


def plot_patterns_vs_config(rows):
    if not rows:
        return
    plt.figure(figsize=(10, 6))
    sns.barplot(data=rows, x='config_name', y='num_patterns', hue='strategy')
    plt.title('Number of Patterns vs Configuration')
    plt.ylabel('Number of Patterns Found')
    plt.xlabel('Configuration')
    plt.legend(title='Strategy')
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'patterns_vs_config.png')
    plt.savefig(path)
    plt.close()
    print(f'Saved {path}')


def summarize_and_save_best(rows):
    if not rows:
        print('No results to summarize.')
        return

    print('\n=== Benchmark Summary ===')
    for row in rows:
        print(f"[{row['strategy']}] config={row['config_name']} trials={row['n_trials']} neighs={row['n_neighborhoods']} radius={row['radius']} -> runtime={row['runtime_sec']}s, patterns={row['num_patterns']}")

    valid = [r for r in rows if r['num_patterns'] is not None and r['runtime_sec'] is not None]
    best = {}
    if valid:
        best_by_patterns = max(valid, key=lambda r: r['num_patterns'])
        best['best_by_patterns'] = {
            'strategy': best_by_patterns['strategy'],
            'config_name': best_by_patterns['config_name'],
            'num_patterns': best_by_patterns['num_patterns'],
            'runtime_sec': best_by_patterns['runtime_sec'],
            'n_trials': int(best_by_patterns['n_trials']),
            'n_neighborhoods': int(best_by_patterns['n_neighborhoods']),
            'min_neighborhood_size': int(best_by_patterns['min_neighborhood_size']),
            'max_neighborhood_size': int(best_by_patterns['max_neighborhood_size']),
            'radius': int(best_by_patterns['radius']),
        }
        print(f"\nBest by patterns: {best_by_patterns['strategy']} / {best_by_patterns['config_name']} ({best_by_patterns['num_patterns']} patterns)")

        fastest = min(valid, key=lambda r: r['runtime_sec'])
        best['fastest'] = {
            'strategy': fastest['strategy'],
            'config_name': fastest['config_name'],
            'num_patterns': fastest['num_patterns'],
            'runtime_sec': fastest['runtime_sec'],
            'n_trials': int(fastest['n_trials']),
            'n_neighborhoods': int(fastest['n_neighborhoods']),
            'min_neighborhood_size': int(fastest['min_neighborhood_size']),
            'max_neighborhood_size': int(fastest['max_neighborhood_size']),
            'radius': int(fastest['radius']),
        }
        print(f"Fastest: {fastest['strategy']} / {fastest['config_name']} ({fastest['runtime_sec']}s)")

        non_empty = [r for r in valid if r['num_patterns'] and r['num_patterns'] > 0 and r['runtime_sec'] and r['runtime_sec'] > 0]
        if non_empty:
            best_efficiency = max(non_empty, key=lambda r: r['num_patterns'] / r['runtime_sec'])
            best['best_efficiency'] = {
                'strategy': best_efficiency['strategy'],
                'config_name': best_efficiency['config_name'],
                'num_patterns': best_efficiency['num_patterns'],
                'runtime_sec': best_efficiency['runtime_sec'],
                'patterns_per_second': round(best_efficiency['num_patterns'] / best_efficiency['runtime_sec'], 4),
                'n_trials': int(best_efficiency['n_trials']),
                'n_neighborhoods': int(best_efficiency['n_neighborhoods']),
                'min_neighborhood_size': int(best_efficiency['min_neighborhood_size']),
                'max_neighborhood_size': int(best_efficiency['max_neighborhood_size']),
                'radius': int(best_efficiency['radius']),
            }
            print(f"Best efficiency: {best_efficiency['strategy']} / {best_efficiency['config_name']} ({best_efficiency['num_patterns']} patterns / {best_efficiency['runtime_sec']}s = {best_efficiency['num_patterns']/best_efficiency['runtime_sec']:.2f} patterns/s)")

    with open(BEST_CONFIG_PATH, 'w') as f:
        json.dump(best, f, indent=2)
    print(f"\nSaved best config summary: {BEST_CONFIG_PATH}")


def main():
    ensure_dirs()
    rows = load_results()
    plot_runtime_vs_strategy(rows)
    plot_patterns_vs_config(rows)
    summarize_and_save_best(rows)


if __name__ == '__main__':
    main()
