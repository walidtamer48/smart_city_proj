import streamlit as st
import ast
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from folium.plugins import BeautifyIcon
from core.data_loader import DataLoader
from graphs.graph_builder import GraphBuilder
from algorithms.mst_planner import MSTPlanner
from algorithms.path_finder import PathFinder
from algorithms.transit_optimizer import TransitOptimizer
from algorithms.traffic_simulator import TrafficSimulator

st.set_page_config(layout="wide")
st.title("🚦 Smart Cairo Transportation Optimizer")

# Load data with normalized columns
loader = DataLoader()
data = loader.load_all()

# Combine coordinates
coords_df = pd.concat([data['neighborhoods'], data['facilities']])

# Build graph with roads and traffic (if handled in GraphBuilder)
builder = GraphBuilder()
G = builder.build_from_roads(
    data['existing_roads'],
    data['potential_roads'],
    coords_df=coords_df,
    traffic_df=data['traffic_flow']  # Assumes GraphBuilder supports this
)

# UI - Navigation
st.sidebar.header("Select View")
tab = st.sidebar.radio("Navigation", [
    "City Map", "Route Finder", "MST Network",
    "Emergency Routing", "Transit Optimization", "Traffic Simulation"
])

if tab == "City Map":
    st.header("🗺 Cairo Real Map - Neighborhoods, Facilities, Roads")

    neighborhoods = data['neighborhoods']
    facilities = data['facilities']
    existing_roads = data['existing_roads']
    potential_roads = data['potential_roads']
    metro_lines = data['metro_lines']
    bus_routes = data['bus_routes']

    # Sidebar filters
    with st.sidebar:
        st.markdown("### 🔍 Filter Options")
        neigh_name_filter = st.text_input("Neighborhood name contains:")
        neigh_type_filter = st.multiselect(
            "Neighborhood type:",
            sorted(neighborhoods['type'].dropna().unique().tolist()),
            default=neighborhoods['type'].dropna().unique().tolist()
        )
        facility_type_filter = st.multiselect(
            "Facility type:",
            sorted(facilities['type'].dropna().unique().tolist()),
            default=facilities['type'].dropna().unique().tolist()
        )

    filtered_neigh = neighborhoods[
        neighborhoods['type'].isin(neigh_type_filter) &
        neighborhoods['name'].str.contains(neigh_name_filter, case=False, na=False)
    ]

    filtered_facilities = facilities[facilities['type'].isin(facility_type_filter)]
    coords_df = pd.concat([filtered_neigh, filtered_facilities])

    center = [filtered_neigh['y'].mean(), filtered_neigh['x'].mean()]
    fmap = folium.Map(location=center, zoom_start=11, control_scale=True)

    layer_neigh = folium.FeatureGroup(name="Neighborhoods").add_to(fmap)
    layer_facilities = folium.FeatureGroup(name="Facilities").add_to(fmap)
    layer_existing = folium.FeatureGroup(name="Existing Roads").add_to(fmap)
    layer_potential = folium.FeatureGroup(name="Potential Roads").add_to(fmap)
    layer_metro = folium.FeatureGroup(name="Metro Lines").add_to(fmap)
    layer_bus = folium.FeatureGroup(name="Bus Routes").add_to(fmap)

    type_colors = {
        "Residential": "green", "Mixed": "blue", "Business": "orange", "Industrial": "gray",
        "Government": "purple", "Airport": "black", "Education": "lightblue", "Transit Hub": "darkgreen",
        "Tourism": "pink", "Sports": "red", "Commercial": "brown", "Medical": "crimson"
    }

    for _, row in filtered_neigh.iterrows():
        type_color = type_colors.get(row['type'], 'lightgray')
        pop = row['population']
        radius = 4 if pop < 100000 else 6 if pop < 300000 else 8
        folium.CircleMarker(
            location=(row['y'], row['x']),
            radius=radius,
            color=type_color,
            fill=True,
            fill_opacity=0.8,
            popup=f"{row['name']}<br>Pop: {pop}<br>Type: {row['type']}"
        ).add_to(layer_neigh)

    icon_map = {
        "Airport": "plane", "Transit Hub": "bus", "Education": "book",
        "Medical": "plus-sign", "Tourism": "camera", "Business": "briefcase",
        "Commercial": "shopping-cart", "Sports": "futbol", "Government": "university"
    }
    for _, row in filtered_facilities.iterrows():
        icon = icon_map.get(row['type'], 'info-sign')
        folium.Marker(
            location=(row['y'], row['x']),
            popup=f"{row['name']} ({row['type']})",
            icon=folium.Icon(icon=icon, prefix="fa", color="blue")
        ).add_to(layer_facilities)

    for _, row in existing_roads.iterrows():
        if row['from_id'] in coords_df['id'].values and row['to_id'] in coords_df['id'].values:
            a = coords_df[coords_df['id'] == row['from_id']].iloc[0]
            b = coords_df[coords_df['id'] == row['to_id']].iloc[0]
            folium.PolyLine([(a['y'], a['x']), (b['y'], b['x'])], color="gray", weight=2).add_to(layer_existing)

    for _, row in potential_roads.iterrows():
        if row['from_id'] in coords_df['id'].values and row['to_id'] in coords_df['id'].values:
            a = coords_df[coords_df['id'] == row['from_id']].iloc[0]
            b = coords_df[coords_df['id'] == row['to_id']].iloc[0]
            folium.PolyLine(
                [(a['y'], a['x']), (b['y'], b['x'])],
                color="blue", weight=2, dash_array="5,10"
            ).add_to(layer_potential)

    for _, row in metro_lines.iterrows():
        stops = row['stations'].split("->")
        coords = []
        for stop in stops:
            if stop in coords_df['id'].astype(str).values:
                pt = coords_df[coords_df['id'].astype(str) == stop].iloc[0]
                coords.append((pt['y'], pt['x']))
        if len(coords) >= 2:
            folium.PolyLine(coords, color="green", weight=3, tooltip=row['name']).add_to(layer_metro)


    for _, row in bus_routes.iterrows():
        try:
            stop_ids = ast.literal_eval(row['stops'])
            coords = []
            for stop in stop_ids:
                stop = str(stop)
                if stop in coords_df['id'].astype(str).values:
                    pt = coords_df[coords_df['id'].astype(str) == stop].iloc[0]
                    coords.append((pt['y'], pt['x']))
            if len(coords) >= 2:
                folium.PolyLine(coords, color="orange", weight=2, tooltip=row.get('routeid', 'Bus Route')).add_to(layer_bus)
        except Exception as e:
            st.warning(f"Error parsing bus route: {e}")


    folium.LayerControl().add_to(fmap)

    with st.expander("ℹ Map Legend & Guide (Click to expand)"):
        st.markdown("""
        ### 🗺 Cairo Map - Legend

        *Neighborhood Types:*
        - 🟩 *Residential*: Housing areas
        - 🟦 *Mixed*: Blend of residential & business
        - 🟧 *Business*: Commercial districts
        - ⬛ *Industrial*: Factories, warehouses
        - 🟪 *Government*: Government offices

        *Facilities:*
        - ⬛ *Airport*: Cairo Intl Airport and similar
        - 🟦 *Education*: Universities and schools
        - 🟩 *Transit Hub*: Metro and rail stations
        - 🟥 *Tourism*: Museums and attractions
        - 🟥 *Sports*: Stadiums and facilities
        - 🟫 *Commercial*: Shopping centers
        - 🟥 *Medical*: Hospitals and clinics

        *Road Types:*
        - ➖ *Gray Line*: Existing Roads
        - ➖ *Blue Dashed*: Potential Roads (planned construction)

        *Transit Lines:*
        - ✅ Green Line: Metro lines
        - 🟠 Orange Line: Bus routes

        *Population Circle Radius:*
        - 🔵 4: Low population (<100k)
        - 🔵 6: Medium population (100k-300k)
        - 🔵 8: High population (>300k)
        """)

    st_folium(fmap, width=1000, height=650)


elif tab == "Route Finder":
    st.header("🚗 Route Finder (Folium)")

    name_df = pd.concat([data['neighborhoods'], data['facilities']])
    id_to_name = {row['id']: row['name'] for _, row in name_df.iterrows()}
    id_to_coords = {row['id']: (row['y'], row['x']) for _, row in name_df.iterrows()}

    nodes = list(G.nodes)
    display_names = [f"{nid} - {id_to_name.get(nid, 'Unknown')}" for nid in nodes]
    node_selector = dict(zip(display_names, nodes))

    start_display = st.selectbox("Start Node", display_names)
    end_display = st.selectbox("End Node", display_names)
    start = node_selector[start_display]
    end = node_selector[end_display]

    algo = st.radio("Select Algorithm", ["Dijkstra", "Dijkstra (Time-Variant)"])
    time_period = "morning"
    if algo == "Dijkstra (Time-Variant)":
        time_period = st.selectbox("Select Time Period", ["morning", "evening", "offpeak"])
        route = PathFinder(G).dijkstra_time_variant(start, end, time_period=time_period)
    else:
        route = PathFinder(G).dijkstra(start, end)

    # Create base map with no tiles initially
    m = folium.Map(location=[30.05, 31.25], zoom_start=11, tiles=None)

    # Tile selection logic
    def add_tile_layer(map_obj, algo_name, period):
        if algo_name == "Dijkstra":
            # Always use classic map for standard Dijkstra
            folium.TileLayer("OpenStreetMap", name="Classic Mode").add_to(map_obj)
        elif period == "morning":
            folium.TileLayer("CartoDB positron", name="Light Mode").add_to(map_obj)
        elif period == "evening":
            folium.TileLayer("OpenStreetMap", name="Evening (Default)").add_to(map_obj)
        elif period == "offpeak":
            folium.TileLayer(
                tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
                attr="© OpenStreetMap contributors, © CartoDB",
                name="Dark Visible Roads"
            ).add_to(map_obj)
        else:
            folium.TileLayer("OpenStreetMap").add_to(map_obj)

    add_tile_layer(m, algo, time_period)

    # Mark all nodes
    for node in G.nodes:
        if node in id_to_coords:
            folium.Marker(
                location=id_to_coords[node],
                popup=id_to_name.get(node, str(node)),
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(m)

    # Draw the route path
    path_coords = [id_to_coords[n] for n in route if n in id_to_coords]
    folium.PolyLine(path_coords, color="#00BFFF", weight=6, opacity=0.9).add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=1000, height=600)


elif tab == "MST Network":
    st.header("🛣 Optimized Road Network (Minimum Spanning Tree)")

    neighborhoods = data['neighborhoods']
    facilities = data['facilities']
    coords_df = pd.concat([neighborhoods, facilities])
    id_to_pos = {row['id']: (row['y'], row['x']) for _, row in coords_df.iterrows()}
    id_to_name = {row['id']: row['name'] for _, row in coords_df.iterrows()}
    id_to_type = {row['id']: row['type'] for _, row in coords_df.iterrows()}

    builder = GraphBuilder()
    G = builder.build_from_roads(data['existing_roads'], data['potential_roads'], coords_df=coords_df)
    critical_ids = data['facilities'].query("type in ['hospital', 'government']")['id'].tolist()
    mst = MSTPlanner(G).kruskal_mst(critical_nodes=critical_ids)
    mst_nodes = mst.number_of_nodes()
    mst_edges = mst.number_of_edges()
    mst_length = sum(G[u][v]['weight'] for u, v in mst.edges)
    st.markdown(f"""
    *📊 MST Summary*
    - 🧠 Nodes in MST: *{mst_nodes}*
    - 🔗 Edges in MST: *{mst_edges}*
    - 📏 Total MST Length: *{mst_length:.2f} km*
    """)
    center = [coords_df['y'].mean(), coords_df['x'].mean()]
    fmap = folium.Map(location=center, zoom_start=11, control_scale=True)

    icon_map = {
        "Medical": "plus-sign", "Airport": "plane", "Education": "book", "Government": "university",
        "Transit Hub": "bus", "Tourism": "camera", "Business": "briefcase", "Commercial": "shopping-cart",
        "Sports": "futbol"
    }
    for node in G.nodes:
        if node in id_to_pos:
            name = id_to_name.get(node, node)
            ntype = id_to_type.get(node, "")
            color = "red" if node in critical_ids else "blue"

            if ntype in icon_map:
                icon = folium.Icon(icon=icon_map[ntype], prefix="fa", color=color)
                folium.Marker(
                    location=id_to_pos[node],
                    tooltip=f"{name} ({ntype})",
                    icon=icon
                ).add_to(fmap)
            else:
                folium.Marker(
                    location=id_to_pos[node],
                    icon=folium.DivIcon(html=f"""
                        <div style="font-size: 9pt; color: black;"><b>{name}</b></div>
                    """)
                ).add_to(fmap)
    for u, v in G.edges:
        if u in id_to_pos and v in id_to_pos:
            folium.PolyLine(
                [id_to_pos[u], id_to_pos[v]],
                color="gray", weight=1.5, opacity=0.3
            ).add_to(fmap)
    for u, v in mst.edges:
        if u in id_to_pos and v in id_to_pos:
            folium.PolyLine(
                [id_to_pos[u], id_to_pos[v]],
                color="green", weight=3,
                tooltip=f"{id_to_name[u]} → {id_to_name[v]}"
            ).add_to(fmap)
    st_folium(fmap, width=1000, height=650)
    with st.expander("ℹ MST Map Legend"):
        st.markdown("""
        - 🟦 *Blue Icon*: Standard node (neighborhood or facility)
        - 🟥 *Red Icon*: Critical facility (hospital or government)
        - ⚪ *Gray Line*: All roads in the full graph
        - 🟢 *Green Line*: Selected MST edges (optimized road network)
        """)

elif tab == "Emergency Routing":
    st.header("🚑 Emergency Route Planner (A*) (Folium)")

    name_df = pd.concat([data['neighborhoods'], data['facilities']])
    id_to_name = {row['id']: row['name'] for _, row in name_df.iterrows()}
    id_to_coords = {row['id']: (row['y'], row['x']) for _, row in name_df.iterrows()}
    pos = {node: (G.nodes[node].get("x", 0), G.nodes[node].get("y", 0)) for node in G.nodes}

    nodes = list(G.nodes)
    display_names = [f"{nid} - {id_to_name.get(nid, 'Unknown')}" for nid in nodes]
    node_selector = dict(zip(display_names, nodes))

    start_display = st.selectbox("Emergency Start", display_names, key="e_start")
    end_display = st.selectbox("Emergency Target", display_names, key="e_end")
    start = node_selector[start_display]
    end = node_selector[end_display]

    algo = st.radio("Select A* Variant", ["A*", "A* (Time-Variant)"])
    time_period = "morning"
    if algo == "A* (Time-Variant)":
        time_period = st.selectbox("Select Time Period", ["morning", "evening", "offpeak"])
        route = PathFinder(G).a_star_time_variant(start, end, pos, time_period=time_period)
    else:
        route = PathFinder(G).a_star(start, end, pos)

    # Create base map with no tiles initially
    m = folium.Map(location=[30.05, 31.25], zoom_start=11, tiles=None)

    # Add tile layer based on algorithm and time
    def add_tile_layer(map_obj, algo_name, period):
        if algo_name == "A*":
            folium.TileLayer("OpenStreetMap", name="Classic Mode").add_to(map_obj)
        elif period == "morning":
            folium.TileLayer("CartoDB positron", name="Light Mode").add_to(map_obj)
        elif period == "evening":
            folium.TileLayer("OpenStreetMap", name="Evening (Default)").add_to(map_obj)
        elif period == "offpeak":
            folium.TileLayer(
                tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
                attr="© OpenStreetMap contributors, © CartoDB",
                name="Dark Visible Roads"
            ).add_to(map_obj)
        else:
            folium.TileLayer("OpenStreetMap").add_to(map_obj)

    add_tile_layer(m, algo, time_period)

    for node in G.nodes:
        if node in id_to_coords:
            folium.Marker(
                location=id_to_coords[node],
                popup=id_to_name.get(node, str(node)),
                icon=folium.Icon(color="gray", icon="info-sign"),
            ).add_to(m)

    path_coords = [id_to_coords[n] for n in route if n in id_to_coords]
    folium.PolyLine(path_coords, color="#FF4444", weight=5, opacity=0.9).add_to(m)

    st_folium(m, width=1000, height=600)

elif tab == "Transit Optimization":
    st.header("🚌 Transit Demand & Optimization")

    demand_df = data['public_transport_demand']
    bus_routes_df = data['bus_routes']
    coords_df = pd.concat([data['neighborhoods'], data['facilities']])
    id_to_coord = {row['id']: (row['y'], row['x']) for _, row in coords_df.iterrows()}

    # Allow user to choose vehicle budget
    vehicle_budget = st.slider("Select available vehicles (bus/metro):", 1, 50, 15)

    # Use route_id and daily_passengers from bus_routes_df to simulate demand
    synthetic_demand = pd.DataFrame({
        'route_id': bus_routes_df['route_id'],
        'morning_peak_demand': bus_routes_df['daily_passengers']
    })

    # Optimize with DP
    optimizer = TransitOptimizer(synthetic_demand)
    selected_routes = optimizer.dp_optimize(vehicle_budget=vehicle_budget)
    st.success(f"Optimized Transit Plan: {selected_routes}")

    st.subheader("📊 Full Bus Routes Demand Table")
    st.dataframe(bus_routes_df)

    st.subheader("🗺 Transit Routes Map (Bus Only)")
    transit_map = folium.Map(location=[30.05, 31.25], zoom_start=10)

    def color_by_demand(val):
        if val >= 40000:
            return "#800000"
        elif val >= 20000:
            return "#FFA500"
        else:
            return "#228B22"

    for _, row in bus_routes_df.iterrows():
        try:
            stops = eval(row['stops'])  # lowercase + renamed by DataLoader
            coords = [id_to_coord[s] for s in stops if s in id_to_coord]
            if len(coords) >= 2:
                val = int(row['daily_passengers'])  # lowercase
                folium.PolyLine(
                    coords,
                    color=color_by_demand(val),
                    weight=4,
                    dash_array="5",
                    tooltip=row['route_id']
                ).add_to(transit_map)
        except Exception as e:
            st.warning(f"Skipping route {row.get('route_id', '?')} due to error: {e}")

    for node_id, (y, x) in id_to_coord.items():
        folium.Marker(
            location=(y, x),
            icon=BeautifyIcon(icon="bus", icon_shape="marker", background_color="#007BFF"),
            popup=node_id
        ).add_to(transit_map)

    st_folium(transit_map, width=1000, height=600)

elif tab == "Traffic Simulation":
    st.header("🚦 Traffic Flow Simulator")

    simulator = TrafficSimulator(data['traffic_flow'])

    st.subheader("🔄 Real-Time Congestion Simulation (Greedy Allocation)")
    report = simulator.simulate_congestion()
    st.json(report)

    st.subheader("🚨 Emergency Vehicle Priority Plan")
    emergency_roads = {
        "1-3": "morning",
        "4-2": "evening",
        "F1-5": "night"
    }  # Example override; consider making this user-selectable
    emergency_plan = simulator.prioritize_emergency(emergency_roads)
    st.json(emergency_plan)

    st.subheader("📊 Greedy vs Fixed Timing Analysis")
    analysis = simulator.analyze_greedy_vs_fixed()
    st.dataframe(pd.DataFrame(analysis))

    # Optimization Pie Chart Summary
    optimal_count = sum(1 for a in analysis if a['is_optimal'])
    suboptimal_count = len(analysis) - optimal_count

    st.markdown("#### 🧮 Optimization Effectiveness")
    st.write(f"✔ Optimal: {optimal_count}  |  ❌ Suboptimal: {suboptimal_count}")

    if optimal_count + suboptimal_count > 0:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.pie(
            [optimal_count, suboptimal_count],
            labels=["Optimal", "Suboptimal"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.warning("No data available for optimization effectiveness chart.")

else:
    st.error("Unknown tab")