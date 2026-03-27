class CostModel:
    def __init__(self, mode="sum"):
        self.mode = mode

    def compute_latency(self, edge_time, server_time, comm_time):
        if self.mode == "sum":
            return edge_time + server_time + comm_time
        elif self.mode == "max":
            return max(edge_time, server_time) + comm_time