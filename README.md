# 🚦 Smart Cairo Transportation Optimizer

A comprehensive transportation analysis and optimization platform for Cairo, Egypt, featuring interactive visualizations, route planning, and traffic simulation capabilities.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Requirements](#data-requirements)
- [Core Modules](#core-modules)
- [Algorithm Features](#algorithm-features)

## 🌟 Overview

The Smart Cairo Transportation Optimizer is an advanced urban transportation analysis tool that combines graph theory, optimization algorithms, and interactive mapping to provide insights into Cairo's transportation network. The platform supports route optimization, emergency planning, transit demand analysis, and traffic flow simulation.

## ✨ Features

### 🗺️ Interactive City Map
- Real-time visualization of Cairo's neighborhoods, facilities, and road networks
- Support for existing and potential road infrastructure
- Metro lines and bus route overlays
- Filterable layers for different location types
- Population-based neighborhood sizing

### 🚗 Intelligent Route Planning
- **Dijkstra's Algorithm**: Standard shortest path routing
- **Time-Variant Dijkstra**: Traffic-aware routing for different time periods
- **A* Algorithm**: Heuristic-based emergency routing
- **Time-Variant A***: Emergency routing with traffic considerations

### 🛣️ Network Optimization
- **Minimum Spanning Tree (MST)**: Optimized road network planning using Kruskal's algorithm
- Critical facility prioritization (hospitals, government buildings)
- Infrastructure cost optimization

### 🚑 Emergency Services
- Priority routing for emergency vehicles
- Critical facility identification and connection
- Time-sensitive pathfinding algorithms

### 🚌 Public Transit Optimization
- Transit demand analysis and visualization
- Dynamic programming-based route optimization
- Bus and metro route planning with capacity constraints
- Demand-based resource allocation

### 🚦 Traffic Simulation
- Real-time congestion simulation using greedy allocation
- Emergency vehicle priority management
- Comparative analysis of timing strategies
- Traffic flow optimization recommendations

## 📁 Project Structure

```
cairo-transport-optimizer/
├── app.py                      # Main Streamlit application
├── main.py                     # Command-line interface
├── requirements.txt            # Python dependencies
├── core/
│   └── data_loader.py         # Data loading and preprocessing
├── graphs/
│   └── graph_builder.py       # Transportation network graph construction
├── algorithms/
│   ├── mst_planner.py         # Minimum Spanning Tree algorithms
│   ├── path_finder.py         # Routing algorithms (Dijkstra, A*)
│   ├── transit_optimizer.py   # Public transit optimization
│   └── traffic_simulator.py   # Traffic flow simulation
└── data/                      # Data files (CSV format)
    ├── neighborhoods.csv
    ├── facilities.csv
    ├── existing_roads.csv
    ├── potential_roads.csv
    ├── metro_lines.csv
    ├── bus_routes.csv
    ├── traffic_flow.csv
    └── public_transport_demand.csv
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/cairo-transport-optimizer.git
   cd cairo-transport-optimizer
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Additional dependencies for full functionality:**
   ```bash
   pip install folium streamlit-folium networkx scipy
   ```

## 🎮 Usage

### Web Application (Streamlit)
Launch the interactive web interface:
```bash
streamlit run app.py
```

Navigate through different features using the sidebar:
- **City Map**: Explore Cairo's infrastructure
- **Route Finder**: Plan optimal routes
- **MST Network**: View optimized road networks
- **Emergency Routing**: Emergency vehicle pathfinding
- **Transit Optimization**: Public transport planning
- **Traffic Simulation**: Traffic flow analysis

### Command Line Interface
Run basic optimization analysis:
```bash
python main.py
```

## 📊 Data Requirements

The application expects CSV files in the `data/` directory with the following structure:

### neighborhoods.csv
```csv
id,name,type,population,x,y
1,Downtown,Business,50000,31.235,30.045
```

### facilities.csv
```csv
id,name,type,x,y
F1,Cairo Hospital,Medical,31.240,30.050
```

### existing_roads.csv
```csv
from_id,to_id,distance,road_type
1,2,5.2,highway
```

### potential_roads.csv
```csv
from_id,to_id,distance,cost,priority
3,4,3.1,1000000,high
```

### traffic_flow.csv
```csv
road_id,morning_flow,evening_flow,offpeak_flow
1-2,2500,3000,1200
```

## 🧠 Core Modules

### DataLoader (`core/data_loader.py`)
- Centralized data loading and preprocessing
- Column normalization and validation
- Support for multiple data formats

### GraphBuilder (`graphs/graph_builder.py`)
- Transportation network graph construction
- Integration of road networks with traffic data
- Node and edge attribute management

### MSTPlanner (`algorithms/mst_planner.py`)
- Kruskal's algorithm implementation
- Critical node prioritization
- Network optimization strategies

### PathFinder (`algorithms/path_finder.py`)
- Dijkstra's shortest path algorithm
- A* heuristic search
- Time-variant routing capabilities

### TransitOptimizer (`algorithms/transit_optimizer.py`)
- Dynamic programming optimization
- Resource allocation algorithms
- Demand-based route planning

### TrafficSimulator (`algorithms/traffic_simulator.py`)
- Congestion simulation models
- Emergency vehicle prioritization
- Performance analysis tools

## 🎯 Algorithm Features

### Routing Algorithms
- **Standard Dijkstra**: Classic shortest path finding
- **Time-Variant Dijkstra**: Adapts to traffic conditions by time of day
- **A* Search**: Heuristic-based pathfinding for emergency scenarios
- **Time-Variant A***: Emergency routing considering traffic patterns

### Optimization Techniques
- **Kruskal's MST**: Optimal network connectivity with minimal cost
- **Dynamic Programming**: Resource allocation for transit systems
- **Greedy Algorithms**: Traffic flow optimization

### Time-Aware Features
- **Morning Peak**: High traffic periods (7-10 AM)
- **Evening Peak**: Rush hour conditions (4-7 PM)
- **Off-Peak**: Normal traffic flow

## 🙏 Acknowledgments

- OpenStreetMap for geographical data
- NetworkX library for graph algorithms
- Streamlit for the web interface framework
- Folium for interactive mapping capabilities
