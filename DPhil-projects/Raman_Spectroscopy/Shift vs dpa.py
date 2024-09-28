import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

x_labels = ['0 (Pristine)', '20.2', '39.0']
Cu_centre = [0, -8.9, -9.6]
Cu_fwhwm = [0, 20.2, 10.4]

Cu1_O1_centre = [0, -9, -8]
Cu1_O1_fwhm = [0, 13.3, 13]

out_of_phase_centre = [0, 4.3, 5.8]
out_of_phase_fwhm = [0, -0.9, 1]



plt.errorbar([1,2,3], Cu_centre, yerr=[0, 0.81, 0.81], marker='o', capsize=5, label = 'Cu2 Peak')
plt.errorbar([1,2,3], Cu1_O1_centre, yerr=[0, 0.86,0.86], marker='o', capsize=5, label = 'Cu1-O1 Peak')
plt.errorbar([1,2,3], out_of_phase_centre, yerr=[0, 0.81, 0.81], marker='o', capsize=5, label = 'Out-of-phase Peak')

plt.errorbar([1,2,3], Cu_fwhwm, yerr=[0, 0.81, 0.81], marker='x', markersize=10, capsize=5, label = 'Cu2 FWHM', color = '#1f77b4' )
plt.errorbar([1,2,3], Cu1_O1_fwhm, yerr=[0, 1.32, 2.37], marker='x', markersize=10,capsize=5, label ='Cu1-O1 FWHM', color = '#ff7f0e')
plt.errorbar([1,2,3], out_of_phase_fwhm, yerr=[0, 0.83, 0.89], marker='x',markersize=10,capsize=5, label ='Out-of-phase FWHM', color = '#2ca02c' )

plt.axhline(y=0, linestyle='--', color='grey')
plt.xticks(range(1, len(x_labels) + 1), x_labels)  # Use set_xticklabels() here
plt.title('Centre and FWHM change per mdpa damage', fontsize=16)
plt.ylabel('Wavenumber shift (cm$^{-1}$)', fontsize=12)
plt.xlabel('Damage Level (mdpa)', fontsize=12)
plt.legend()
plt.tight_layout()
plt.show()