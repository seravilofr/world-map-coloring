# world_map_coloring.py
# 🌍 Dynamic ±4 h world map – matching by ISO-3 codes

import geopandas as gpd
import matplotlib.pyplot as plt
import pytz
import pycountry
import pycountry_convert
from datetime import datetime, timezone

WORLD_MAP_URL = (
    "https://raw.githubusercontent.com/nvkelso/"
    "natural-earth-vector/master/geojson/"
    "ne_110m_admin_0_countries.geojson"
)

# ───────────────────────────── 1. Static definitions
ORANGE_COUNTRY_NAMES = [
    "France", "Germany", "United Kingdom",
    "Netherlands", "Switzerland", "Austria",
]

BLACK_COUNTRY_NAMES = [
    "China", "Russia", "Belarus",
    "Iran", "North Korea",
]

def to_iso3(name: str) -> str:
    """Return ISO-3 code from a common country name."""
    try:
        return pycountry.countries.lookup(name).alpha_3
    except LookupError:
        return pycountry.countries.search_fuzzy(name)[0].alpha_3

# Build static ISO-3 sets
ORANGE_ALPHA3 = {to_iso3(name) for name in ORANGE_COUNTRY_NAMES}
BLACK_ALPHA3  = {to_iso3(name) for name in BLACK_COUNTRY_NAMES}

# ───────────────────────────── 2. Helper functions
def primary_offset(alpha2: str, now_utc: datetime) -> float | None:
    """Return current UTC offset (in hours) for a country's primary timezone."""
    tz_list = pytz.country_timezones.get(alpha2)
    if not tz_list:
        return None
    tz = pytz.timezone(tz_list[0])
    offset = tz.fromutc(now_utc.replace(tzinfo=None)).utcoffset()
    return offset.total_seconds() / 3600

def build_blue_alpha3() -> set[str]:
    """Return a set of α-3 codes of countries within ±4 h of France."""
    now_utc   = datetime.now(timezone.utc)
    tz_paris  = pytz.timezone("Europe/Paris")
    fr_offset = tz_paris.fromutc(now_utc.replace(tzinfo=None)).utcoffset().total_seconds() / 3600

    blue = set()
    for c in pycountry.countries:
        off = primary_offset(c.alpha_2, now_utc)
        if off is None or abs(off - fr_offset) > 4:
            continue
        blue.add(c.alpha_3)

    # Exclude Orange and Black countries
    return blue - ORANGE_ALPHA3 - BLACK_ALPHA3

# Build BLUE_ALPHA3 dynamically
BLUE_ALPHA3 = build_blue_alpha3()

# ───────────────────────────── 3. Color selector
def color_from_iso3(iso3: str) -> str:
    """Return color based on ISO-3 code."""
    if iso3 in ORANGE_ALPHA3:
        return "orange"
    if iso3 in BLACK_ALPHA3:
        return "black"
    if iso3 in BLUE_ALPHA3:
        return "blue"
    return "white"

# ───────────────────────────── 4. Main script
def main() -> None:
    world = gpd.read_file(WORLD_MAP_URL)

    # Color by iso_a3 code
    world["color"] = world["ADM0_A3"].str.upper().apply(color_from_iso3)

    fig, ax = plt.subplots(figsize=(24, 12))
    world.boundary.plot(ax=ax, linewidth=0.8, color="grey")
    world.plot(ax=ax, color=world["color"], edgecolor="grey", linewidth=0.5)

    ax.set_title("World Map – Countries within ±4 h of France in Blue", fontsize=20)
    ax.set_axis_off()

    plt.savefig("colored_world_map.png", bbox_inches="tight", dpi=300)
    plt.show()

if __name__ == "__main__":
    main()