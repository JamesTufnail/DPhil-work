import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

O_2MeV = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\SRIM\Processed data\2 MeV O into 3um YBCO.xlsx")
O_depth, O2_dpa = O_2MeV["Depth (um)"], O_2MeV["mdpa per slice"]
# normalized_O2_dpa = (O2_dpa - np.min(O2_dpa)) / (np.max(O2_dpa) - np.min(O2_dpa))

He_300KeV = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\SRIM\Processed data\300 KeV He into 3um YBCO.xlsx")
He_300_depth, He_300_dpa = He_300KeV["Depth (um)"], He_300KeV["mdpa per slice"]
# normalized_300_dpa = (He_300_dpa - np.min(He_300_dpa)) / (np.max(He_300_dpa) - np.min(He_300_dpa))

He_2MeV = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\SRIM\Processed data\2 MeV He into 5um YBCO.xlsx")
He_2_depth, He_2_dpa = He_2MeV["Depth (um)"], He_2MeV["mdpa per slice"]
# normalized_2_dpa = (He_2_dpa - np.min(He_2_dpa)) / (np.max(He_2_dpa) - np.min(He_2_dpa))

# Plot the data
plt.plot(O_depth, O2_dpa,  label='2 MeV O')
plt.plot(He_300_depth, He_300_dpa,label='300 keV He')
plt.plot(He_2_depth, He_2_dpa, label='2 MeV He')

# Add vertical lines to show the depth of the YBCO layer
plt.axvline(x=2, color='k', linestyle='--')

# Add a legend, etc
plt.yscale('log')  # Set the y-axis scale to logarithmic
plt.ylim(1, 1e4)  # Set the y-axis limits
plt.xlim(0, 5)  # Set the x-axis limits
plt.ylabel('Damage (mdpa)', fontsize=12)
plt.xlabel('Depth ($\mu$m)', fontsize=12)
plt.title('Logarithmic Damage vs Depth', fontsize=16)
plt.legend()
plt.grid(True)
plt.show()