import heapq
class PathFinder: # A dictionary to cache previously computed paths so repeated calculations are avoided.
    def __init__(self, G):
        self.G = G
        self.memo = {}
       

    def dijkstra(self, source, target):
        key = ("dijkstra", source, target)
        if key in self.memo:
            return self.memo[key]
        dist = {node: float('inf') for node in self.G.nodes}
        # Initializes the distance to every node as infinity, meaning they are unreachable at first.
        prev = {node: None for node in self.G.nodes}
        #prev keeps track of the previous node in the shortest path to each node.
        dist[source] = 0
        pq = [(0, source)]
        while pq:
            curr_dist, u = heapq.heappop(pq)
            if u == target:
                break
            for v in self.G.neighbors(u):
                weight = self.G[u][v].get("weight", 1)
                alt = dist[u] + weight #Calculate the tentative distance
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(pq, (alt, v))
        path = []
        node = target
        while node is not None:
            path.append(node)
            node = prev[node]
        result = path[::-1]
        self.memo[key] = result
        # Store the computed result in memo for future reuse and return the path.
        return result

    def dijkstra_time_variant(self, source, target, time_period="morning"):
        key = ("dijkstra_time", source, target, time_period)
        if key in self.memo:
            return self.memo[key]

        dist = {node: float('inf') for node in self.G.nodes}
        prev = {node: None for node in self.G.nodes}
        dist[source] = 0
        pq = [(0, source)]

        while pq:
            curr_dist, u = heapq.heappop(pq)
            if u == target:
                break
            for v in self.G.neighbors(u):
                weight = self.G[u][v].get(f"{time_period}_weight", 1)
                alt = dist[u] + weight
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(pq, (alt, v))

        path = []
        node = target
        while node is not None:
            path.append(node)
            node = prev[node]
        result = path[::-1]
        self.memo[key] = result
        return result

    def a_star(self, source, target, pos):
        key = ("astar", source, target)
        if key in self.memo:
            return self.memo[key]

        def heuristic(u, v):
            return ((pos[u][0] - pos[v][0]) ** 2 + (pos[u][1] - pos[v][1]) ** 2) ** 0.5

        open_set = [(0, source)]
        g_score = {node: float('inf') for node in self.G.nodes}
        f_score = {node: float('inf') for node in self.G.nodes}
        came_from = {}
        g_score[source] = 0
        f_score[source] = heuristic(source, target)

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == target:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(source)
                result = path[::-1]
                self.memo[key] = result
                return result
            for neighbor in self.G.neighbors(current):
                tentative_g = g_score[current] + self.G[current][neighbor].get("weight", 1)
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, target)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    def a_star_time_variant(self, source, target, pos, time_period="morning"):
        key = ("astar_time", source, target, time_period)
        if key in self.memo:
            return self.memo[key]

        def heuristic(u, v):
            return ((pos[u][0] - pos[v][0]) ** 2 + (pos[u][1] - pos[v][1]) ** 2) ** 0.5

        open_set = [(0, source)]
        g_score = {node: float('inf') for node in self.G.nodes}
        f_score = {node: float('inf') for node in self.G.nodes}
        came_from = {}
        g_score[source] = 0
        f_score[source] = heuristic(source, target)

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == target:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(source)
                result = path[::-1]
                self.memo[key] = result
                return result
            for neighbor in self.G.neighbors(current):
                weight = self.G[current][neighbor].get(f"{time_period}_weight", 1)
                tentative_g = g_score[current] + weight
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, target)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []
