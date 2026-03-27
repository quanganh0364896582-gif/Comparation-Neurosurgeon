import heapq


class Dijkstra:
    def __init__(self, cost):

        self.cost = cost

    def run(self, K=1, flops=None, edge_speed=None, server_speed=None, output=None, bandwidth=None):

        N = len(flops)

        # state: (layer, loc, k)
        start = (0, 0, 0)  # layer 0, edge, 0 switch

        dist = {start: 0}
        pq = [(0, start)]

        while pq:
            current_cost, (i, loc, k) = heapq.heappop(pq)

            if i == N:
                return current_cost

            # -------- 1. Continue compute --------
            if i < N:
                if loc == 0:
                    compute_cost = flops[i] / edge_speed
                else:
                    compute_cost = flops[i] / server_speed

                nxt = (i + 1, loc, k)
                new_cost = current_cost + compute_cost

                if nxt not in dist or new_cost < dist[nxt]:
                    dist[nxt] = new_cost
                    heapq.heappush(pq, (new_cost, nxt))

            # -------- 2. Switch --------
            if k < K:
                comm_cost = output[i] / bandwidth
                new_loc = 1 - loc

                nxt = (i, new_loc, k + 1)
                new_cost = current_cost + comm_cost

                if nxt not in dist or new_cost < dist[nxt]:
                    dist[nxt] = new_cost
                    heapq.heappush(pq, (new_cost, nxt))

        return float("inf")