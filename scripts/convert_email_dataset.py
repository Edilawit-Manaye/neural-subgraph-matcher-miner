import gzip
import pickle
import argparse
import networkx as nx
from tqdm import tqdm


def convert_email_eu_core(input_path, output_path):
    G = nx.DiGraph()
    with gzip.open(input_path, 'rt') as f:
        for line in tqdm(f, desc='Reading edges'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            src, dst = int(parts[0]), int(parts[1])
            G.add_edge(src, dst)
    data_to_save = {
        'nodes': [(n, {'label': str(n), 'id': str(n)}) for n in G.nodes()],
        'edges': [(u, v, {'type': 'email'}) for u, v in G.edges()]
    }
    with open(output_path, 'wb') as f:
        pickle.dump(data_to_save, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"Saved {output_path} ({G.number_of_nodes()} nodes, {G.number_of_edges()} edges)")


def main():
    parser = argparse.ArgumentParser(description='Convert SNAP email-Eu-core to pkl')
    parser.add_argument('--input', default='email-Eu-core.txt.gz')
    parser.add_argument('--output', default='email_eu_core.pkl')
    args = parser.parse_args()
    convert_email_eu_core(args.input, args.output)


if __name__ == '__main__':
    main()
