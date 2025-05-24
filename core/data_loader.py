import pandas as pd

class DataLoader:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

    def load_csv(self, filename):
        return pd.read_csv(f"{self.data_dir}/{filename}")

    def normalize_columns(self, df, rename_map):
        df.columns = df.columns.str.strip().str.lower()  # Clean and lowercase
        df = df.rename(columns=rename_map)
        return df

    def cast_ids(self, df):
        # Convert relevant ID columns to string
        for col in ['id', 'from_id', 'to_id', 'route_id', 'line_id']:
            if col in df.columns:
                df[col] = df[col].astype(str)
        return df

    def load_all(self):
        return {
            "neighborhoods": self.cast_ids(self.load_csv("neighborhoods.csv")),
            "facilities": self.cast_ids(self.load_csv("facilities.csv")),
            "existing_roads": self.cast_ids(self.load_csv("existing_roads.csv")),
            "potential_roads": self.cast_ids(self.load_csv("potential_roads.csv")),
            "bus_routes": self.cast_ids(
                self.normalize_columns(
                    self.load_csv("bus_routes.csv"),
                    {
                        "routeid": "route_id",
                        "stops": "stops",
                        "stations": "stations",
                        "buses": "buses",
                        "daily": "daily_passengers"
                    }
                )
            ),
            "metro_lines": self.cast_ids(
                self.normalize_columns(
                    self.load_csv("metro_lines.csv"),
                    {
                        "line_id": "line_id",
                        "stations": "stations",
                        "name": "name",
                        "daily_passengers": "daily_passengers"
                    }
                )
            ),
            "traffic_flow": self.cast_ids(
                self.normalize_columns(
                    self.load_csv("traffic_flow.csv"),
                    {
                        "intersection": "intersection",
                        "northbound": "northbound_flow",
                        "eastbound": "eastbound_flow",
                        "southbound": "southbound_flow",
                        "westbound": "westbound_flow"
                    }
                )
            ),
            "public_transport_demand": self.cast_ids(
                self.normalize_columns(
                    self.load_csv("public_transport_demand.csv"),
                    {
                        "from": "from_id",
                        "to": "to_id",
                        "dailypassengers": "daily_passengers"
                    }
                )
            )
        }
