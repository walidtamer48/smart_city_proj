import pandas as pd
import matplotlib.pyplot as plt

def plot_all_locations(neighborhoods_path, facilities_path):
    neighborhoods = pd.read_csv(neighborhoods_path)
    facilities = pd.read_csv(facilities_path)

    plt.figure(figsize=(12, 9))

    # Plot neighborhoods
    plt.scatter(neighborhoods['x'], neighborhoods['y'], c='blue', s=80, label='Neighborhoods')
    for _, row in neighborhoods.iterrows():
        plt.text(row['x'], row['y'], row['name'], fontsize=9, ha='right', va='bottom')

    # Plot facilities by type
    colors = {
        'hospital': 'red',
        'government': 'green',
        'fire_station': 'orange',
        'police': 'purple'
    }

    for ftype, group in facilities.groupby('type'):
        plt.scatter(group['x'], group['y'], s=120, c=colors.get(ftype, 'gray'), label=ftype.title())
        for _, row in group.iterrows():
            plt.text(row['x'], row['y'], row['name'], fontsize=9, ha='left', va='bottom')

    plt.title("Cairo Transportation Nodes Map")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
