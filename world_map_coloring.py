# world_map_coloring.py
# 🌍 World Map Coloring Script

import geopandas as gpd
import matplotlib.pyplot as plt

# URL to the world countries data (GeoJSON format)
WORLD_MAP_URL = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson'

# Define countries to color
ORANGE_COUNTRIES = ['France', 'Germany', 'United Kingdom', 'Netherlands', 'Switzerland', 'Austria']
BLACK_COUNTRIES = ['China', 'Russia', 'Belarus', 'Iran', 'North Korea']
BLUE_COUNTRIES = [
    'Cape Verde', 'Greenland', 'Brazil', 'Argentina', 'Uruguay', 'Chile', 'Iceland', 'Portugal', 'Spain', 'France',
    'Germany', 'United Kingdom', 'Netherlands', 'Switzerland', 'Austria', 'Italy', 'Poland', 'Czechia', 'Slovakia',
    'Hungary', 'Belgium', 'Norway', 'Sweden', 'Denmark', 'Finland', 'Greece', 'Turkey', 'Israel', 'Saudi Arabia',
    'South Africa', 'Ukraine', 'Romania', 'Bulgaria', 'Estonia', 'Latvia', 'Lithuania', 'Morocco', 'Algeria',
    'Tunisia', 'Libya', 'Egypt', 'Jordan', 'Syria', 'Lebanon', 'Ethiopia', 'Kenya', 'Somalia'
]

def get_color(country_name):
    if country_name in ORANGE_COUNTRIES:
        return 'orange'
    elif country_name in BLACK_COUNTRIES:
        return 'black'
    elif country_name in BLUE_COUNTRIES:
        return 'blue'
    else:
        return 'white'

def main():
    # Load world map data
    world = gpd.read_file(WORLD_MAP_URL)

    # Assign colors
    world['color'] = world['ADMIN'].apply(get_color)

    # Create the plot
    fig, ax = plt.subplots(figsize=(24, 12))
    world.boundary.plot(ax=ax, linewidth=0.8, color='grey')
    world.plot(ax=ax, color=world['color'], edgecolor='grey', linewidth=0.5)

    ax.set_title('World Map - Colored by Specification', fontsize=24)
    ax.set_axis_off()

    # Save the plot
    plt.savefig('colored_world_map.png', bbox_inches='tight', dpi=300)
    plt.show()

if __name__ == "__main__":
    main()
