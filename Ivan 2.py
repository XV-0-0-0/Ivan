import pandas as pd

file_path = r"C:\Users\admin\Desktop\Development of automated vehicles_ purpose of use, risk management, engineering challenges and how to Gain People’s Trust. (Ответы).xlsx"
df = pd.read_excel(file_path)
country_column = "What country are you from?"
countries = sorted(df[country_column].dropna().unique())
print("List of countries:")
for country in countries:
    print(country)