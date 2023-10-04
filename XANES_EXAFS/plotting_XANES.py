import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np

xanes_10 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Plotting\marked10.nor",
                       delim_whitespace=' ',
                       skiprows=10,
                       names = ['Energy', 'Pristine', '2 MeV O', 'Annealed']
                       )
xanes_45 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Plotting\marked45.nor",
                          delim_whitespace=' ',
                            skiprows=10,
                            names = ['Energy', 'Pristine', '2 MeV O', 'Annealed']
                            )

xanes_80 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Plotting\marked80.nor",
                            delim_whitespace=' ',
                            skiprows=10,
                            names = ['Energy', 'Pristine', '2 MeV O', 'Annealed']
                            )

print(xanes_10.head())
data_sets = [(xanes_10, 'Pristine', '2 MeV O$^+$', '10 Degrees'),
             (xanes_45, 'Pristine', '2 MeV O$^+$', '45 Degrees'),
             (xanes_80, 'Pristine', '2 MeV O$^+$', '80 Degrees')]

fig, axs = plt.subplots(3, 1, figsize=(4, 6), sharex=True)

for i, (data, pristine_label, mev_label, title) in enumerate(data_sets):
    axs[i].plot(data['Energy'], data['Pristine'], label=pristine_label)
    axs[i].plot(data['Energy'], data['2 MeV O'] , linestyle = '--', label=mev_label)
    # axs[i].plot(data['Energy'], data['Annealed'], linestyle = '-.', label= 'Annealed')
    axs[i].legend()
    axs[i].set_title(title)

axs[2].set_xlim(8960, 9060)
axs[1].set_ylabel('Normalised Counts', fontsize=12)
axs[2].set_xlabel('Energy', fontsize=12)

fig.suptitle('XANES of Pristine and 2 MeV O Irradiated Fujikura YBCO Tape', fontsize=14)
plt.legend()
plt.tight_layout()
plt.show()
