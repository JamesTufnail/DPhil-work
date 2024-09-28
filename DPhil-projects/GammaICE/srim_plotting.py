import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


file = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Techniques\SRIM\Gamma Irradiation Experiments\processed_SRIM_for_plotting.xlsx"




data = pd.read_excel(file, header=0, sheet_name='Single')
print(data.head())

sample_name = '4 MeV He$^{2+}$ ions into SCS4050 Tape'

for col in data.columns[1:]:
    depth = data['Depth (um)']
    dpa = data[col]

plt.plot(depth, dpa, label='1.1e+15 ions/cm$^2$')

plt.xlabel('Depth ($\mu$m)')
plt.axvline(x=2, color = 'grey', linestyle='--'), plt.axvline(x=4.9, color = 'grey', linestyle='--')
plt.text(.8, 10, '2 $\mu$m Ag', fontsize=11, ha='center', va='center'), plt.text(3.5, 10, '2.9 $\mu$m REBCO', fontsize=11, ha='center', va='center')#, plt.text(8, 20, 'Ni Substrate', fontsize=10, ha='center', va='center')
plt.ylabel('Damage (mdpa)')
plt.title(sample_name)

# Create the legend
legend = plt.legend(loc='upper left', title='Irradiation Dose', facecolor='white')
# Set the legend frame to be fully opaque
legend.get_frame().set_alpha(1)

# plt.legend(loc='upper left', title='Irradiation Dose', alpha=1)
plt.show()
