from core.data_loader import DataLoader
from graphs.graph_builder import GraphBuilder
from algorithms.mst_planner import MSTPlanner

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

def main():
    print("🔄 Loading data...")
    loader = DataLoader()
    data = loader.load_all()

    print("🧠 Building transportation graph...")
    G = GraphBuilder().build_from_roads(data['existing_roads'], data['potential_roads'])

    print(f"✅ Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    print("🛠️ Running Kruskal's MST algorithm...")
    mst = MSTPlanner(G).kruskal_mst()
    print(f"✅ MST created with {mst.number_of_edges()} edges")

    # Build position dictionary
    coords = pd.concat([data["neighborhoods"], data["facilities"]])
    id_to_pos = {row["id"]: (row["x"], row["y"]) for _, row in coords.iterrows()}
    missing = [n for n in G.nodes if n not in id_to_pos]

    # Warn if any node missing position
    if missing:
        print(f"⚠️ Warning: {len(missing)} node(s) missing coordinates. Defaulting to (0,0)")
        for n in missing:
            id_to_pos[n] = (0, 0)

    # Calculate MST total length
    total_length = sum(G[u][v]['weight'] for u, v in mst.edges)
    print(f"📏 Total MST length: {total_length:.2f} units")

    # Plot full graph and MST
    print("🖼️ Rendering MST map...")
    plt.figure(figsize=(10, 8))
    nx.draw(G, id_to_pos, node_color="lightgray", edge_color="gray", with_labels=True, alpha=0.5)
    nx.draw(mst, id_to_pos, node_color="skyblue", edge_color="green", width=2, with_labels=True)
    plt.title("Optimized Cairo Road Network - MST")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
