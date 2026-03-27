from utils.yolo11n_extract import YOLOLayerAnalyzer
from src.handle_data import Data
from src.dijkstra import Dijkstra
from src.neurosurgeon import Neurosurgeon

import time
import matplotlib.pyplot as plt


# =========================
# Load model
# =========================
analyzer = YOLOLayerAnalyzer("yolo11n.pt")
flops_layers, output_size_layers = analyzer.analyze()


# =========================
# Config
# =========================
f_edge = 5 * 2e9
f_server = 5 * 30e9
bandwidth = 10


# =========================
# Measure
# =========================
def measure(num_layers):

    flops = flops_layers[:num_layers]
    outputs = output_size_layers[:num_layers]

    data = Data(flops, f_edge, f_server, outputs, bandwidth)
    cost = data.run()

    # =========================
    # 🔵 Dijkstra
    # =========================
    start = time.perf_counter_ns()
    dijkstra_solver = Dijkstra(cost)
    dijkstra_cost = dijkstra_solver.run()
    dijkstra_time = time.perf_counter_ns() - start

    # =========================
    # 🟠 Neurosurgeon
    # =========================
    start = time.perf_counter_ns()
    neuro_solver = Neurosurgeon(data)
    _, neuro_cost = neuro_solver.run()
    neuro_time = time.perf_counter_ns() - start

    return dijkstra_time, neuro_time, dijkstra_cost, neuro_cost


# =========================
# Warm-up
# =========================
for _ in range(10):
    measure(10)


# =========================
# Benchmark
# =========================
cases = []
avg_dijkstra_time = []
avg_neuro_time = []

avg_dijkstra_cost = []
avg_neuro_cost = []

for num in range(2, len(flops_layers), max(1, len(flops_layers)//10)):

    n = 10

    dijkstra_times = []
    neuro_times = []

    dijkstra_costs = []
    neuro_costs = []

    for _ in range(n):
        dt, nt, dc, nc = measure(num)

        dijkstra_times.append(dt)
        neuro_times.append(nt)

        dijkstra_costs.append(dc)
        neuro_costs.append(nc)

    cases.append(num)

    avg_dijkstra_time.append(sum(dijkstra_times)/n)
    avg_neuro_time.append(sum(neuro_times)/n)

    avg_dijkstra_cost.append(sum(dijkstra_costs)/n)
    avg_neuro_cost.append(sum(neuro_costs)/n)

    print(f"\n=== Case: {num} layers ===")
    print(f"Dijkstra time: {avg_dijkstra_time[-1]:.2f} ns")
    print(f"Neuro time: {avg_neuro_time[-1]:.2f} ns")

    print(f"Dijkstra cost: {avg_dijkstra_cost[-1]:.4f}")
    print(f"Neuro cost: {avg_neuro_cost[-1]:.4f}")



# =========================
# PLOT 1: Runtime
# =========================
plt.figure(figsize=(10,6))
plt.plot(cases, avg_dijkstra_time, marker='o', label='Dijkstra')
plt.plot(cases, avg_neuro_time, marker='s', label='Neurosurgeon')

plt.xlabel('Number of Layers')
plt.ylabel('Execution Time (ns)')
plt.title('Runtime Comparison')

plt.yscale('log')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("runtime.png")


# =========================
# PLOT 2: Latency (Cost)
# =========================
plt.figure(figsize=(10,6))
plt.plot(cases, avg_dijkstra_cost, marker='o', label='Dijkstra')
plt.plot(cases, avg_neuro_cost, marker='s', label='Neurosurgeon')

plt.xlabel('Number of Layers')
plt.ylabel('Latency (Cost)')
plt.title('Optimal Latency Comparison')

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("latency.png")

plt.show()