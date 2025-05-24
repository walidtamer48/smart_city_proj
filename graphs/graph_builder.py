import networkx as nx

class GraphBuilder:
    def __init__(self):
        self.G = nx.Graph()

    def build_from_roads(self, existing_df, potential_df=None, coords_df=None, traffic_df=None):
        if coords_df is not None:
            for _, row in coords_df.iterrows():
                self.G.add_node(row["id"], x=row["x"], y=row["y"])

        # Load traffic flow data (road_id = "from-to")
        traffic_lookup = {}
        if traffic_df is not None:
            for _, row in traffic_df.iterrows():
                parts = str(row["road_id"]).split("-")
                if len(parts) == 2:
                    key = (parts[0], parts[1])
                    traffic_lookup[key] = row
                    traffic_lookup[(parts[1], parts[0])] = row  # both directions

        def get_weights(from_id, to_id, distance):
            row = traffic_lookup.get((str(from_id), str(to_id)))
            if row is not None:
                base = 1000  # normalize vehicle count to scale weights
                return {
                    "morning_weight": distance * (row["morning_peak_veh_h"] / base),
                    "evening_weight": distance * (row["evening_peak_veh_h"] / base),
                    "offpeak_weight": distance * ((row["afternoon_veh_h"] + row["night_veh_h"]) / (2 * base))
                }
            else:
                return {
                    "morning_weight": distance,
                    "evening_weight": distance,
                    "offpeak_weight": distance
                }

        for _, row in existing_df.iterrows():
            weights = get_weights(row["from_id"], row["to_id"], row["distance_km"])
            self.G.add_edge(
                row["from_id"], row["to_id"],
                weight=row["distance_km"],
                morning_weight=weights["morning_weight"],
                evening_weight=weights["evening_weight"],
                offpeak_weight=weights["offpeak_weight"],
                capacity=row.get('capacity_veh_h'),
                type="existing"
            )

        if potential_df is not None:
            for _, row in potential_df.iterrows():
                weights = get_weights(row["from_id"], row["to_id"], row["distance_km"])
                self.G.add_edge(
                    row["from_id"], row["to_id"],
                    weight=row["distance_km"],
                    morning_weight=weights["morning_weight"],
                    evening_weight=weights["evening_weight"],
                    offpeak_weight=weights["offpeak_weight"],
                    capacity=row.get('capacity_veh_h'),
                    type="potential"
                )

        return self.G
