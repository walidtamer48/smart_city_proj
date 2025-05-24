import numpy as np
import pandas as pd
class TransitOptimizer:
    def __init__(self, demand_df):
        self.demand_df = demand_df
    def dp_optimize(self, vehicle_budget=15):
        """
        Select routes that maximize coverage of demand under limited vehicles.
        Each route has:
        - demand (benefit)
        - required_vehicles (cost)
        """
        df = self.demand_df.copy()
        # Compute total demand
        if 'demand' not in df.columns:
            df['demand'] = (
                df.get('morning_peak_demand', 0) +
                df.get('afternoon_demand', 0) +
                df.get('evening_peak_demand', 0) +
                df.get('night_demand', 0)
            )
        # Estimate required vehicles
        if 'required_vehicles' not in df.columns:
            df['required_vehicles'] = np.ceil(df['demand'] / 100).astype(int)

        n = len(df)
        cost = df['required_vehicles'].tolist()
        benefit = df['demand'].tolist()
        # DP table
        dp = [[0] * (vehicle_budget + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for v in range(vehicle_budget + 1):
                if cost[i - 1] <= v:
                    dp[i][v] = max(dp[i - 1][v], dp[i - 1][v - cost[i - 1]] + benefit[i - 1])
                else:
                    dp[i][v] = dp[i - 1][v]

        # Backtrack to find selected routes
        selected = []
        v = vehicle_budget
        for i in range(n, 0, -1):
            if dp[i][v] != dp[i - 1][v]:
                selected.append(i - 1)
                v -= cost[i - 1]

        if 'route_id' in df.columns:
            return df.iloc[selected]['route_id'].tolist()
        else:
            return df.iloc[selected].index.tolist()
