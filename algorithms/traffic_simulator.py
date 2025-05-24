import pandas as pd

class TrafficSimulator:
    def __init__(self, traffic_df):
        self.traffic_df = traffic_df.copy()

    def simulate_congestion(self):
        results = []
        for _, row in self.traffic_df.iterrows():
            road_id = row.get("road_id")
            flows = {
                "morning": row.get("morning_peak_veh_h", 0) or 0,
                "afternoon": row.get("afternoon_veh_h", 0) or 0,
                "evening": row.get("evening_peak_veh_h", 0) or 0,
                "night": row.get("night_veh_h", 0) or 0
            }
            total_flow = sum(flows.values())
            green_time = {
                period: round((v / total_flow) * 60, 1) if total_flow > 0 else 0
                for period, v in flows.items()
            }
            dominant = max(flows, key=flows.get)
            congestion = (
                "High" if total_flow >= 3000 else
                "Moderate" if total_flow >= 1500 else
                "Low"
            )
            results.append({
                "road_id": road_id,
                "total_flow": total_flow,
                "dominant_period": dominant,
                "green_time_alloc": green_time,
                "congestion_level": congestion
            })
        return results

    def prioritize_emergency(self, emergency_roads):
        """
        emergency_roads: dict mapping road_id to prioritized time period (e.g. 'morning', 'evening')
        """
        overrides = []
        for _, row in self.traffic_df.iterrows():
            road_id = row.get("road_id")
            time_periods = ["morning", "afternoon", "evening", "night"]
            green_default = {t: 15 for t in time_periods}
            if road_id in emergency_roads:
                priority = emergency_roads[road_id]
                green_default = {t: 10 for t in time_periods}
                green_default[priority] = 30
                reason = f"Emergency priority → {priority}"
            else:
                reason = "Normal cycle"
            overrides.append({
                "road_id": road_id,
                "emergency_plan": green_default,
                "reason": reason
            })
        return overrides

    def analyze_greedy_vs_fixed(self):
        """
        Compare greedy timing vs fixed-timing (15s each period) at each road segment.
        """
        analysis = []
        for _, row in self.traffic_df.iterrows():
            road_id = row.get("road_id")
            flows = {
                "morning": row.get("morning_peak_veh_h", 0) or 0,
                "afternoon": row.get("afternoon_veh_h", 0) or 0,
                "evening": row.get("evening_peak_veh_h", 0) or 0,
                "night": row.get("night_veh_h", 0) or 0
            }
            total_flow = sum(flows.values())
            if total_flow == 0:
                continue  # skip invalid data

            dominant = max(flows, key=flows.get)
            greedy_time = (flows[dominant] / total_flow) * 60
            fixed_time = 15
            is_optimal = greedy_time >= fixed_time

            analysis.append({
                "road_id": road_id,
                "dominant_period": dominant,
                "greedy_alloc_time": round(greedy_time, 1),
                "fixed_alloc_time": fixed_time,
                "is_optimal": is_optimal,
                "congestion_level": (
                    "High" if total_flow >= 3000 else
                    "Moderate" if total_flow >= 1500 else
                    "Low"
                )
            })
        return analysis
