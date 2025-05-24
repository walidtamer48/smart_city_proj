import networkx as nx
class MSTPlanner:
    def __init__(self, G):
        self.G = G
    def kruskal_mst(self, critical_nodes=None):
        mst = nx.Graph()
        parent = {node: node for node in self.G.nodes}
        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u
        def union(u, v):
            pu, pv = find(u), find(v)
            parent[pu] = pv
        edges = sorted(self.G.edges(data=True), key=lambda x: x[2]['weight'])
        for u, v, data in edges:
            if find(u) != find(v):
                mst.add_edge(u, v, **data)
                union(u, v)
        if critical_nodes:
            connected = set(mst.nodes)
            for node in critical_nodes:
                if node not in connected:
                    nearest = None
                    min_weight = float('inf')
                    for neighbor in self.G.neighbors(node):
                        if neighbor in mst:
                            weight = self.G[node][neighbor].get('weight', 1)
                            if weight < min_weight:
                                nearest = neighbor
                                min_weight = weight
                    if nearest:
                        mst.add_edge(node, nearest, **self.G[node][nearest])
                        print(f"✅ Critical node {node} connected to MST via {nearest} (weight={min_weight})")

        return mst
