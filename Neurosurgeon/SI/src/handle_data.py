chubby_size = 10000000

# comm_times = [chubby_size, 484.752, 94.563, 41.322, 51.551, 28.33, 24.968, 16.532,
#  20.588, 17.426, 52.015, 67.003, 24.234, 100.574, chubby_size,
#  47.96, 12.344, 32.771, 20.26, 6.187, 21.604, 13.5, 2.423]
#
# layer_times_2 = [13150.81, 15468.55, 35690.06, 17578.67, 22310.97, 14488.44, 22642.61,
#  6065.51, 18103.24, 19662.81, 16138.71, 5363.45, 676.75, 16020.68,
#  1698.42, 1770.54, 33257.24, 7237.94, 1548.84, 29074.08, 3864.21,
#  246.86, 44671.88, 106679.49]
#
# layer_times_3 = [16026.25, 14163.68, 44144.43, 18671.9, 41584.95, 21272.84, 61831.02,
#  10811.47, 42549.29, 21310.4, 22975.56, 2589.66, 683.63, 19536.7,
#  2296.24, 3873.87, 26174.95, 4480.21, 482.07, 15115.18, 4723.94,
#  152.32, 59023.33, 116022.15]

class Data:
 def __init__(self, flop_layers, flop_edge, flop_server, output, bandwidth):
  self.layer_times_2 = []
  self.layer_times_3 = []

  for flop in flop_layers:
   self.layer_times_2.append(flop / flop_edge)
   self.layer_times_3.append(flop / flop_server)

  self.comm_times = []
  for size in output:
   self.comm_times.append(size / bandwidth)

  # thêm index 0 (để index từ 1)
  self.layer_times_2.insert(0, 0)
  self.layer_times_3.insert(0, 0)
  self.comm_times.insert(0, 0)

  self.capacity = len(self.layer_times_2)
  self.num_points = self.capacity - 1

  # dùng INF cho no-edge
  self.cost = [[float("inf") for _ in range(self.capacity * 2)] for _ in range(self.capacity * 2)]

 def get_test_bed_cost(self):
  N = self.num_points

  for i in range(1, N):
   # =========================
   # 1. Mobile execution
   # =========================
   self.cost[i][i + 1] = self.layer_times_2[i]

   # =========================
   # 2. Cloud execution
   # =========================
   self.cost[i + N][i + N + 1] = self.layer_times_3[i]

   # =========================
   # 3. Transfer (SPLIT POINT)
   # =========================
   self.cost[i][i + N] = self.comm_times[i]

  # =========================
  # START → mobile first layer
  # =========================
  self.cost[1][2] = self.layer_times_2[1]

  # =========================
  # END: last cloud node
  # =========================
  # đảm bảo có đường tới node cuối
  self.cost[N + N - 1][N + N] = self.layer_times_3[N]

 def run(self):
  self.get_test_bed_cost()
  return self.cost