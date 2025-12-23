import pandas as pd

file_path = r"C:\Users\admin\Desktop\Survey287.xlsx"

df = pd.read_excel(file_path, dtype=str)
rows_to_delete = [144, 154, 189, 196, 202, 203, 215, 222, 223, 227, 235, 256, 259, 262]
df = df.drop([r - 2 for r in rows_to_delete], errors="ignore")
df.to_excel(file_path, index=False)

print("Done")