import pandas as pd

data = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James Tufnail\JT1_1_1.txt", skiprows = 38, delimiter='\t', encoding='cp1252')
print(data)