import pandas as pd
from pathlib import Path

file_path = r"C:\Users\admin\Desktop\Development of automated vehicles_ purpose of use, risk management, engineering challenges and how to Gain People’s Trust. (Ответы).xlsx"

df = pd.read_excel(file_path, dtype=str)

def get_continent(country):
    if pd.isna(country):
        return "Unknown"

    c = country.strip().lower()

    mapping = {
        'Europe': {
            'poland','austria','belarus','denmark','england','france','germany',
            'greece','italy','latvia','netherlands','norway','portugal','romania',
            'spain','switzerland','uk','united kingdom','ukraine','estonia','russia'
        },
        'America': {
            'canada','costa rica','us','usa','united states','united states of america'
        },
        'Asia': {
            'azerbaijan','bangladesh','china','india','kazakhstan','korea',
            'kyrgyzstan','malaysia','pakistan','taiwan','turkey','türkiye',
            'uae','hong kong','vietnam'
        },
        'Africa': {
            'algeria','mozambique','rwanda','south africa','tunisia','zimbabwe'
        }
    }

    for continent, countries in mapping.items():
        if c in countries:
            return continent
    return "Others"

df['Continent'] = df['What country are you from?'].apply(get_continent)
total_count = len(df)

def calculate_stats(group):
    n = len(group)
    gen_pc = (n / total_count) * 100 if total_count else 0

    males = group['What is your gender?'].str.lower().eq('male').sum()
    females = group['What is your gender?'].str.lower().eq('female').sum()

    male_pc = (males / n) * 100 if n else 0
    female_pc = (females / n) * 100 if n else 0

    has_license = group['Do you have a driving license?'] \
        .str.lower().str.startswith('yes').sum()

    lic_pc = (has_license / n) * 100 if n else 0
    no_lic_pc = 100 - lic_pc

    cont_code = {
        "Europe": "EU",
        "America": "NA",
        "Asia": "AS",
        "Africa": "AF",
        "Others": "Others"
    }.get(group.name, "Others")

    return pd.Series({
        'Gen. continent': f"{group.name} {gen_pc:.1f}%",
        'Men%': f"{male_pc:.1f}%",
        'Wom.%': f"{female_pc:.1f}%",
        '% driving licence of continent':
            f"{cont_code} from {lic_pc:.0f}% yes – {no_lic_pc:.0f}% no"
    })

summary = (
    df.groupby('Continent')
      .apply(calculate_stats, include_groups=False)
      .reset_index(drop=True)
)

output_path = Path.home() / "Desktop" / "Final_Continent_Statistics_NEW.xlsx"
summary.to_excel(output_path, index=False, engine="openpyxl")

print("Table created successfully!")
print(summary.to_string(index=False))