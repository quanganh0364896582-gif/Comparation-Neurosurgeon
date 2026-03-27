import sys
import os

# thêm dòng này
sys.path.append(os.path.dirname(__file__))

import time
import matplotlib.pyplot as plt

from dp import DP
from cost_model import CostModel
from handle_data import Data
from dijkstra import Dijkstra


def run_experiment(flops, output_sizes, edge_speed, server_speed, bandwidth):

    results = []

    for num_layers in range(50, 251, 50):

        print(f"\n===== {num_layers} layers =====")

        # cắt model theo số layer
        f = flops[:num_layers]
        o = output_sizes[:num_layers]

        cost_model = CostModel(mode="sum")

        # -------- Dijkstra --------
        start = time.time()

        data = Data(f, edge_speed, server_speed, o, bandwidth)
        cost = data.run()

        dij_cost = Dijkstra(cost).run()

        dij_time = time.time() - start

        # -------- DP --------
        start = time.time()

        dp = DP(f, edge_speed, server_speed, o, bandwidth)
        dp_cost = dp.run()

        dp_time = time.time() - start

        print(f"Dijkstra: {dij_cost:.4f} | time: {dij_time:.4f}")
        print(f"DP:       {dp_cost:.4f} | time: {dp_time:.4f}")

        results.append({
            "layers": num_layers,
            "dijkstra_latency": dij_cost,
            "dp_latency": dp_cost,
            "dijkstra_time": dij_time,
            "dp_time": dp_time
        })

    return results