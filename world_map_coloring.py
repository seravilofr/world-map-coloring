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
    # America
    'Venezuela', 'Guyana', 'Suriname', 'Dominican Republic', 'Haiti', 'Trinidad and Tobago',
    'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Grenada', 'Barbados',
    'Argentina', 'Uruguay', 'Brazil', 'Paraguay', 'Bolivia', 'Bahamas', 'Bermuda',
    
    # Europe
    'Ireland', 'Portugal', 'Spain', 'Italy', 'Belgium', 'Luxembourg', 'Norway', 'Sweden', 'Denmark',
    'Finland', 'Poland', 'Czechia', 'Slovakia', 'Hungary', 'Croatia', 'Slovenia', 'Serbia', 
    'Bosnia and Herzegovina', 'Montenegro', 'North Macedonia', 'Albania', 'Greece', 'Bulgaria',
    'Romania', 'Ukraine', 'Moldova', 'Estonia', 'Latvia', 'Lithuania', 'Malta', 'Cyprus',
    'Iceland', 'Andorra', 'San Marino', 'Monaco', 'Liechtenstein',
    
    # Africa
      'Mauritania', 'Western Sahara', 'Morocco', 'Algeria', 'Tunisia', 'Libya', 'Egypt',
    'Mali', 'Senegal', 'Gambia', 'Guinea', 'Guinea-Bissau', 'Sierra Leone', 'Liberia',
    'Ivory Coast', 'Ghana', 'Togo', 'Benin', 'Burkina Faso', 'Niger', 'Nigeria',
    'Chad', 'Cameroon', 'Central African Republic', 'South Sudan', 'Sudan',
    'Democratic Republic of the Congo', 'Republic of the Congo', 'Gabon', 'Equatorial Guinea',
    'Uganda', 'Kenya', 'Tanzania', 'Rwanda', 'Burundi', 'Malawi', 'Zambia', 'Zimbabwe',
    'Angola', 'Namibia', 'Botswana', 'South Africa', 'Lesotho', 'Eswatini', 'Madagascar',
    'Comoros', 'Seychelles', 'Mauritius',
    
    # Middle-East / West-Asia
    'Turkey', 'Cyprus', 'Israel', 'Palestine', 'Jordan', 'Lebanon', 'Syria', 'Iraq',
    'Saudi Arabia', 'Kuwait', 'Bahrain', 'Qatar', 'United Arab Emirates', 'Oman',
    'Armenia', 'Azerbaijan', 'Georgia'

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
