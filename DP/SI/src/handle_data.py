from cost_model import CostModel


class Data:
    def __init__(self, flop_layers, flop_edge, flop_server, output, bandwidth, mode="sum"):

        self.cost_model = CostModel(mode)

        self.layer_times_2 = [f / flop_edge for f in flop_layers]
        self.layer_times_3 = [f / flop_server for f in flop_layers]
        self.comm_times = [s / bandwidth for s in output]

        self.layer_times_2.insert(0, -1)
        self.layer_times_3.insert(0, -1)
        self.comm_times.insert(0, -1)

        self.capacity = len(self.layer_times_2)
        self.num_points = self.capacity - 1

        self.cost = [[-1 for _ in range(self.capacity * 2)] for _ in range(self.capacity * 2)]

    def run(self):

        cost_1 = 0
        cost_2 = sum(self.layer_times_3[1:])

        for i in range(1, self.capacity - 1):

            cost_1 += self.layer_times_2[i]
            cost_2 -= self.layer_times_3[i]

            self.cost[i][i + 1] = 0
            self.cost[i + self.num_points][i + self.num_points + 1] = 0

            edge_time = cost_1
            server_time = cost_2
            comm_time = self.comm_times[i]

            self.cost[i][i + self.num_points + 1] = self.cost_model.compute_latency(
                edge_time, server_time, comm_time
            )

        return self.cost