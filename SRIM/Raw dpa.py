import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1,3, figsize=(10, 6))


O_2MeV = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\SRIM\Processed data\2 MeV O into 3um YBCO.xlsx")
O_depth, O2_dpa = O_2MeV["Depth (um)"], O_2MeV["mdpa per slice"]

He_300KeV = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\SRIM\Processed data\300 KeV He into 3um YBCO.xlsx")
He_300_depth, He_300_dpa = He_300KeV["Depth (um)"], He_300KeV["mdpa per slice"]

He_2MeV = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\SRIM\Processed data\2 MeV He into 5um YBCO.xlsx")
He_2_depth, He_2_dpa = He_2MeV["Depth (um)"], He_2MeV["mdpa per slice"]


axes[0].plot(O_depth, O2_dpa,  label='')
axes[0].set_ylabel('Displacements per atom (mdpa)')
axes[0].set_title("2 MeV O$+$ in 5E14 ions/cm$^2$")
axes[0].axvline(x=2, color='gray', linestyle='dashed')

axes[1].plot(He_300_depth, He_300_dpa, color='orange')
axes[1].set_title("300 KeV He$+$ in 8.6E15 ions/cm$^2$")
axes[1].axvline(x=2, color='gray', linestyle='dashed')

axes[2].plot(He_2_depth, He_2_dpa, color='red')
axes[2].set_title("2 MeV He$+$ in 3.6E16 ions/cm$^2$")
axes[2].axvline(x=2, color='gray', linestyle='dashed')

fig.suptitle('SRIM Calculations of ion irradiation into YBCO', fontsize=16)
fig.text(0.5, 0.04, "Depth ($\mu$m)", ha='center')
plt.tight_layout
plt.show()

