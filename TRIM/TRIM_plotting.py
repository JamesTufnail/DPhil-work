import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame

# SCRIPT PURPOSE: convert .txt files from TRIM to plots

# note that full damage cascade overestiamtes dpa by factor of 2
# also displacement energy always assumed at 25 eV


cascades = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\CDT Activities\SRIM-CDT-Practice\Task 1\VACANCY.txt",
                       skiprows=27, sep="  ", engine='python')

# manipulating columns
cascades_df = pd.DataFrame(cascades)
cascades_df = cascades_df.drop(100)
cascades_df = cascades_df.drop(columns=cascades_df.columns[1])

# rename column values from .csv and change from SI to numerical
cascades_df.columns.values[0:2] = ['Ion Penetration Depth', 'Vacancies']
cascades_df['Ion Penetration Depth'] = pd.to_numeric(cascades_df['Ion Penetration Depth'], errors='coerce')
cascades_df['Vacancies'] = pd.to_numeric(cascades_df['Vacancies'], errors='coerce')

print(cascades_df)



# plotting figure
plt.plot(cascades_df['Ion Penetration Depth'], cascades_df['Vacancies'])
plt.show()
