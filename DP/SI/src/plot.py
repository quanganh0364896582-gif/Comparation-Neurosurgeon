import matplotlib.pyplot as plt
import os


def plot_results(results):

    layers = [r["layers"] for r in results]

    dij_latency = [r["dijkstra_latency"] for r in results]
    dp_latency = [r["dp_latency"] for r in results]

    dij_time = [r["dijkstra_time"] for r in results]
    dp_time = [r["dp_time"] for r in results]

    #  tạo thư mục lưu ảnh
    save_dir = "plots"
    os.makedirs(save_dir, exist_ok=True)

    # -------- Latency --------
    plt.figure(figsize=(6, 4))
    plt.plot(layers, dij_latency, marker='o', linewidth=2, label="Dijkstra")
    plt.plot(layers, dp_latency, marker='s', linewidth=2, label="DP")

    plt.xlabel("Number of Allowed Switches (K)")
    plt.ylabel("Latency")
    plt.title("Latency Comparison")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    #  lưu ảnh
    plt.savefig(os.path.join(save_dir, "latency.png"), dpi=300)

    # -------- Runtime --------
    plt.figure(figsize=(6, 4))
    plt.plot(layers, dij_time, marker='o', linewidth=2, label="Dijkstra")
    plt.plot(layers, dp_time, marker='s', linewidth=2, label="DP")

    plt.xlabel("Number of Allowed Switches (K)")
    plt.ylabel("Runtime (ns)")
    plt.title("Runtime Comparison")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    #  lưu ảnh
    plt.savefig(os.path.join(save_dir, "runtime.png"), dpi=300)

    plt.show()