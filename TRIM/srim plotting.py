import pandas as pd
import matplotlib.pyplot as plt


# Specify the Excel file path and sheet name
file_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\SRIM\Planned He irradiatios of YBCO for Raman\Planned SRIM Calcs.xlsx"
sheet_name = 'Plotting Data'

# Read the specific sheet into a DataFrame
he_plots = pd.read_excel(file_path, sheet_name=sheet_name)
data = pd.DataFrame(he_plots)

all_energies = ['200 keV', '400 keV', '600 keV', '800 keV', '1000 keV', '1200 keV', '1400 keV', '1600 keV', '1800 keV']
plot_energies = ['200 keV', '400 keV', '600 keV', '800 keV', '1200 keV'] 
########## Variables #############
title = 'Damage events into 3 $\mu$m of YBCO'


################### Script ####################
for energy in all_energies:
    plt.plot(data['Depth (um)'], data[energy], label = energy)

# vline of Branescu penetration depth
plt.axvline(x=0.2, linestyle='--', linewidth = 1, color = 'black')

plt.title(title)
plt.xlim(0, 3)
plt.ylim(0, 300)
plt.xlabel('Depth ($\mu$m)')
plt.ylabel('Damage (mdpa)')
plt.legend(loc='upper right')
plt.show()
