import sys
import os

BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(BASE_DIR, "src"))
sys.path.append(os.path.join(BASE_DIR, "utils"))

from yolo11n_extract import YOLOLayerAnalyzer
from handle_data import Data
from dijkstra import Dijkstra
from dp import DP
from plot import plot_results
import time


# -------- LOAD MODEL --------
analyzer = YOLOLayerAnalyzer("yolo11n.pt")
flops_layers, output_size_layers = analyzer.analyze()

# config
f_edge = 2e9
f_server = 30e9
bandwidth = 10


# -------- MEASURE FUNCTION --------
def measure(flops, outputs, K):
    cost = Data(flops, f_edge, f_server, outputs, bandwidth).run()

    # Dijkstra
    start = time.perf_counter_ns()
    dij_cost = Dijkstra(cost).run(K,
    flops=flops,
    edge_speed=f_edge,
    server_speed=f_server,
    output=outputs,
    bandwidth=bandwidth)
    dij_time = time.perf_counter_ns() - start

    # DP
    start = time.perf_counter_ns()
    dp_cost = DP(flops, f_edge, f_server, outputs, bandwidth).run(K)
    dp_time = time.perf_counter_ns() - start

    return dij_cost, dp_cost, dij_time, dp_time


# -------- WARMUP --------
for _ in range(3):
    measure(flops_layers[:100], output_size_layers[:100], K=1)


# -------- RUN EXPERIMENT --------
results = []

#  chạy theo K thay vì layer
Ks = [1, 2, 3, 4]

# giữ số layer cố định để fair
num_layers = 100

f = flops_layers[:num_layers]
o = output_size_layers[:num_layers]

for K in Ks:

    dij, dp, t1, t2 = measure(f, o, K)

    print(f"K={K} | Dijkstra: {dij:.4f} ({t1}) | DP: {dp:.4f} ({t2})")

    results.append({
        "layers": K,
        "dijkstra_latency": dij,
        "dp_latency": dp,
        "dijkstra_time": t1,
        "dp_time": t2
    })


# -------- PLOT --------
plot_results(results)