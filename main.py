import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

file_path = r"C:\Users\admin\Desktop\Survey287.xlsx"
df = pd.read_excel(file_path)

df["raw_name"] = df["What country are you from?"].astype(str).str.strip().str.lower()

name_fix = {
    "america": "USA",
    "united states of america": "USA",
    "united states": "USA",
    "unites states": "USA",
    "usa": "USA",
    "us": "USA",
    "us ": "USA",
    "england": "England",
    "uk": "England",
    "united kingdom": "England",
    "united kingdom ": "England",
    "united king": "England",
    "united kin": "England",
    "ukraine": "Ukraine",
    "ukrainian": "Ukraine",
    "ua": "Ukraine",
    "russia": "Russia",
    "ru ru": "Russia",
    ".": "Russia",
    "türkiye": "Turkey",
    "turkey": "Turkey",
    "greece.": "Greece",
    "greece": "Greece",
    "hong kong": "China",
    "china": "China",
    "mozambican": "Mozambique",
    "belarusian": "Belarus",
    "uae": "United Arab Emirates",
    "india": "India",
    "india ": "India",
    "india.": "India",
    "korea": "South Korea",
    "south korea": "South Korea",
    "switzerland": "Switzerland",
    "netherlands": "Netherlands",
    "austria": "Austria",
    "mozambic": "Mozambique"
}

df["name"] = df["raw_name"].map(name_fix).fillna(df["raw_name"].str.title())

counts = df["name"].value_counts().reset_index()
counts.columns = ["name", "counts"]

world = gpd.read_file(r"C:\Users\admin\Desktop\world.geojson")
world = world.merge(counts, on="name", how="left")
world["counts"] = world["counts"].fillna(0)

def get_color(count):
    if count <= 0 or pd.isna(count):
        return "#F5F5F5"
    elif 1 <= count <= 10: return "#7a0000"
    elif 11 <= count <= 20: return "#cc0000"
    elif 21 <= count <= 30: return "#ff8c00"
    elif 31 <= count <= 40: return "#ffa500"
    elif 41 <= count <= 50: return "#b59b00"
    elif 51 <= count <= 60: return "#ffd700"
    elif 61 <= count <= 70: return "#006400"
    elif 71 <= count <= 80: return "#32cd32"
    else:                  return "#32cd32"

world["color_hex"] = world["counts"].apply(get_color)

fig, ax = plt.subplots(figsize=(20, 12))
ax.set_facecolor("white")

world.plot(ax=ax, color="#F5F5F5", edgecolor="black", linewidth=0.1)

participants_only = world[world["counts"] > 0]
participants_only.plot(
    ax=ax,
    color=participants_only["color_hex"],
    edgecolor="black",
    linewidth=0.2
)

legend_elements = [
    mpatches.Patch(color='#F5F5F5', label='0 respondents'),
    mpatches.Patch(color='#7a0000', label='1 - 10 respondents'),
    mpatches.Patch(color='#cc0000', label='11 - 20 respondents'),
    mpatches.Patch(color='#ff8c00', label='21 - 30 respondents'),
    mpatches.Patch(color='#ffa500', label='31 - 40 respondents'),
    mpatches.Patch(color='#b59b00', label='41 - 50 respondents'),
    mpatches.Patch(color='#ffd700', label='51 - 60 respondents'),
    mpatches.Patch(color='#006400', label='61 - 70 respondents'),
    mpatches.Patch(color='#32cd32', label='71+ respondents')
]

ax.legend(handles=legend_elements, loc='lower left', title="Agenda", frameon=True, fontsize=10)

ax.axis("off")
plt.title("Geographical Distribution of Respondents", fontsize=22, pad=20)

print("\n--- Final Statistics (Participants only) ---")
print(counts[counts["counts"] > 0].sort_values(by="counts", ascending=False).to_string(index=False))

plt.tight_layout()
plt.show()