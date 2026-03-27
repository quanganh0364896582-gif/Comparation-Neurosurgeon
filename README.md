# 🧠 Comperation-DP

This project studies how to optimally split a deep neural network (YOLO) between an edge device and a cloud server to minimize inference latency.

We compare two optimization strategies:
- **Dijkstra (Shortest Path)**
- **Dynamic Programming (DP)**

---

## 🚀 Problem Overview

Modern AI applications often require real-time inference on resource-constrained devices (edge). To improve performance, part of the model can be offloaded to a server.

👉 The key question:
> Where should we split the model to minimize total latency?

---

## ⚙️ Cost Model

We model the total latency as a combination of:
- Edge computation time
- Server computation time
- Communication time

---

### 📌 Notation

- \( F_i \): FLOPs of layer \( i \)  
- \( S_i \): Output size of layer \( i \)  
- \( f_{edge} \): Edge compute speed  
- \( f_{server} \): Server compute speed  
- \( B \): Network bandwidth  

---

### 🧮 Latency Formula

#### ✅ Sequential Model
