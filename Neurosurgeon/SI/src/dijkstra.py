import heapq

class Dijkstra:
    def __init__(self, cost):
        self.cost = cost
        self.num_points = len(cost)//2 - 1
        self.start = 1

    def dijkstra(self):
        n = len(self.cost)

        # distance array
        dist = [float("inf")] * n
        dist[self.start] = 0

        # min heap: (cost, node)
        heap = [(0, self.start)]

        while heap:
            current_cost, u = heapq.heappop(heap)


            # skip nếu đã có đường tốt hơn
            if current_cost > dist[u]:
                continue

            #  early stop (rất quan trọng)
            if u == self.num_points * 2:
                return current_cost

            # relax edges
            for v, edge_cost in enumerate(self.cost[u]):
                if edge_cost != float("inf"):
                    new_cost = current_cost + edge_cost


                    if new_cost < dist[v]:
                        dist[v] = new_cost
                        heapq.heappush(heap, (new_cost, v))


        return dist[self.num_points * 2]

    def run(self):
        return self.dijkstra()