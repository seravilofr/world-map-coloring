# 🌍 World Map Coloring Project

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

This project generates a custom world map where countries are colored based on specific rules:

- 🟠 **Orange**: France, Germany, United Kingdom, Netherlands, Switzerland, Austria
- ⚫ **Black**: China, Russia, Belarus, Iran, North Korea
- 🔵 **Blue**: Countries located between UTC-4 and UTC+4
- ⚪ **White**: All other countries

---

## 📂 Project Structure

```
world-map-coloring/
├── world_map_coloring.py
├── colored_world_map.png (generated after running the script)
└── README.md
```

---

## 🚀 How to Run

1. Make sure you have Python 3.8+ installed.
2. Install the required libraries:

```bash
pip install geopandas matplotlib
```

3. Run the script:

```bash
python world_map_coloring.py
```

4. The map will be saved as `colored_world_map.png` in the project folder.

---

## 📥 Output Preview

After running the script, you will obtain a world map colored as specified.

> Note: The generated file is named `colored_world_map.png`.

---

## 🛠 Requirements

- [GeoPandas](https://geopandas.org/)
- [Matplotlib](https://matplotlib.org/)

You can install them easily using:

```bash
pip install geopandas matplotlib
```

---

## 📜 License

This project is open-source and free to use.
