# world_map_coloring.py
# 🌍 World Map Coloring Script – ±4 h from France with enlarged legend text

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pytz
import pycountry
import pycountry_convert
from datetime import datetime, timezone

# ───────────────────────────── 1. Data source (Natural Earth 50m GeoJSON)
WORLD_MAP_URL = (
    "https://raw.githubusercontent.com/nvkelso/"
    "natural-earth-vector/master/geojson/"
    "ne_50m_admin_0_countries.geojson"
)

# ───────────────────────────── 2. Static definitions
ORANGE_COUNTRY_NAMES = [
    "France", "Germany", "United Kingdom",
    "Netherlands", "Switzerland", "Austria",
]
BLACK_COUNTRY_NAMES = [
    "China", "Russia", "Belarus",
    "Iran", "North Korea",
]
# Corrections for missing timezones
manual_timezones = {
    'SS': 'Africa/Juba',      # South Sudan
    'ER': 'Africa/Asmara',    # Eritrea
}

def to_iso3(name: str) -> str:
    """Return ISO-3 code from a country name (fallback to fuzzy search)."""
    try:
        return pycountry.countries.lookup(name).alpha_3
    except LookupError:
        return pycountry.countries.search_fuzzy(name)[0].alpha_3

ORANGE_ALPHA3 = {to_iso3(n) for n in ORANGE_COUNTRY_NAMES}
BLACK_ALPHA3  = {to_iso3(n) for n in BLACK_COUNTRY_NAMES}

# ───────────────────────────── 3. Helper functions
def primary_offset(alpha2: str, now_utc: datetime) -> float | None:
    """Return current UTC offset (in hours) for a country's primary timezone."""
    tzs = pytz.country_timezones.get(alpha2)
    if not tzs and alpha2 in manual_timezones:
        tzs = [manual_timezones[alpha2]]
    if not tzs:
        return None
    tz = pytz.timezone(tzs[0])
    offset = tz.fromutc(now_utc.replace(tzinfo=None)).utcoffset()
    return offset.total_seconds() / 3600

def build_blue_alpha3() -> set[str]:
    """Compute ISO-3 codes of countries within ±4 h of France (Europe/Paris)."""
    now_utc = datetime.now(timezone.utc)
    fr_off = pytz.timezone("Europe/Paris") \
        .fromutc(now_utc.replace(tzinfo=None)) \
        .utcoffset().total_seconds() / 3600

    blue = set()
    for country in pycountry.countries:
        off = primary_offset(country.alpha_2, now_utc)
        if off is None or abs(off - fr_off) > 4:
            continue
        blue.add(country.alpha_3)
    return blue - ORANGE_ALPHA3 - BLACK_ALPHA3

BLUE_ALPHA3 = build_blue_alpha3()

def color_from_iso3(iso3: str) -> str:
    """Return a color based on the ISO-3 code."""
    if iso3 in ORANGE_ALPHA3:
        return "orange"
    if iso3 in BLACK_ALPHA3:
        return "black"
    if iso3 in BLUE_ALPHA3:
        return "blue"
    return "white"

# ───────────────────────────── 4. Main plotting
def main() -> None:
    # Load the Natural Earth GeoJSON (50m)
    world = gpd.read_file(WORLD_MAP_URL)

    # Map ISO-3 codes to colors
    world["color"] = world["ADM0_A3"].str.upper().apply(color_from_iso3)

    fig, ax = plt.subplots(figsize=(20, 10))
    world.boundary.plot(ax=ax, linewidth=0.6, color="grey")
    world.plot(ax=ax, color=world["color"], edgecolor="grey", linewidth=0.4)

    # Legend with individual borders and larger font size
    orange_patch = mpatches.Patch(
        facecolor="orange", edgecolor="black", linewidth=1,
        label="EPEX offices"
    )
    blue_patch = mpatches.Patch(
        facecolor="blue", edgecolor="black", linewidth=1,
        label="Workation possible (pending risk assessment)"
    )
    white_patch = mpatches.Patch(
        facecolor="white", edgecolor="black", linewidth=1,
        label="Workation not possible (due to timezones)"
    )
    black_patch = mpatches.Patch(
        facecolor="black", edgecolor="black", linewidth=1,
        label="Blacklisted countries"
    )
    legend = ax.legend(
        handles=[orange_patch, blue_patch, white_patch, black_patch],
        loc="lower left",
        frameon=True,
        facecolor="white",
        edgecolor="black",
        fontsize=14    # increase legend text size
    )
    legend.get_frame().set_linewidth(1)

    ax.set_axis_off()
    plt.savefig("colored_world_map.png", bbox_inches="tight", dpi=300)
    plt.show()

if __name__ == "__main__":
    main()