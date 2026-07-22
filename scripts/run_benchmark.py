import subprocess
import sys
import os

DATASET = "email_eu_core.pkl"
MODEL_PATH = "/app/ckpt/universal/model_universal_hybrid_minilm_rgcn.pt"
VOCAB_DIR = "/app/artifacts/vocab_ci_semantic"
STRS = ["greedy", "mcts", "beam"]
CONFIGS = {
    "small": "n_trials=100 n_neighborhoods=200 min_neighborhood_size=3 max_neighborhood_size=6 radius=3",
    "medium": "n_trials=300 n_neighborhoods=800 min_neighborhood_size=4 max_neighborhood_size=12 radius=4",
    "large": "n_trials=800 n_neighborhoods=1500 min_neighborhood_size=5 max_neighborhood_size=20 radius=5",
}


def run(cmd, check=False):
    print(f"\n>>> {cmd}")
    res = subprocess.run(cmd, shell=True, text=True)
    if check and res.returncode != 0:
        sys.exit(res.returncode)
    return res


def main():
    run("python scripts/convert_email_dataset.py --input email-Eu-core.txt.gz --output email_eu_core.pkl", check=True)
    run("test -f /app/email_eu_core.pkl")

    for strat in STRS:
        for cfg, defs in CONFIGS.items():
            params = dict(kv.split("=") for kv in defs.split())
            out_path = f"/app/results/patterns_{strat}_{cfg}.pkl"
            log_path = f"/app/results/decoder_{strat}_{cfg}.log"
            cmd = (
                f"python -m subgraph_mining.decoder"
                f" --dataset={DATASET}"
                f" --graph_type=directed"
                f" --model_path={MODEL_PATH}"
                f" --vocab_dir={VOCAB_DIR}"
                f" --n_trials={params['n_trials']}"
                f" --n_neighborhoods={params['n_neighborhoods']}"
                f" --min_pattern_size=3"
                f" --max_pattern_size=4"
                f" --min_neighborhood_size={params['min_neighborhood_size']}"
                f" --max_neighborhood_size={params['max_neighborhood_size']}"
                f" --search_strategy={strat}"
                f" --memory_efficient"
                f" --out_batch_size=2"
                f" --streaming_workers=0"
                f" --radius={params['radius']}"
                f" --out_path={out_path}"
            )
            run(f"bash -c \"{cmd} > {log_path} 2>&1 || true\"")
            run(
                f"python scripts/collect_metrics.py"
                f" {log_path} {out_path} {strat} {cfg}"
                f" {params['n_trials']} {params['n_neighborhoods']}"
                f" {params['min_neighborhood_size']} {params['max_neighborhood_size']}"
                f" {params['radius']} /app/results/benchmark_results.csv"
            )

    run("python scripts/generate_plots.py || true")
    run("ls -la /app/results")
    run("ls -la /app/plots/cluster")


if __name__ == "__main__":
    main()
