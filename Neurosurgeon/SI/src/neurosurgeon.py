class Neurosurgeon:
    def __init__(self, data):
        """
        data: object từ class Data của bạn
        """
        self.mobile = data.layer_times_2   # T_m
        self.cloud = data.layer_times_3    # T_c
        self.comm = data.comm_times        # T_u
        self.N = len(self.mobile) - 1      # số layer

    def run(self):
        best_cost = float("inf")
        best_split = -1
        cloud_only = self.comm[1] + sum(self.cloud[1:self.N+1])
        if cloud_only < best_cost:
            best_cost = cloud_only
            best_split = 0

        # Neurosurgeon (Algorithm 1)
        for j in range(1, self.N):

            # --- Mobile execution ---
            mobile_cost = sum(self.mobile[1:j+1])

            # --- Cloud execution ---
            cloud_cost = sum(self.cloud[j+1:self.N+1])

            # --- Data transfer ---
            transfer_cost = self.comm[j]

            total_cost = mobile_cost + cloud_cost + transfer_cost


            if total_cost < best_cost:
                best_cost = total_cost
                best_split = j

        return best_split, best_cost