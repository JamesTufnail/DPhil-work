import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from brokenaxes import brokenaxes

x_labels = ["Pristine", "300 keV He", "2 MeV O"]

Cu_vals = [145.9, 136.3, 137.0]
Cu_errors = [0.575, 0.575, 0.575]

Cu1_O1_vals = [231.0, 223.0, 222.0]
Cu1_O1_errors = [0.575, 0.635, 0.636]

Out_of_phase_vals = [331.7, 325.9, 327.4]
Out_of_phase_errors = [0.575, 0.575, 0.575]

################ FWHM #################
Cu_fwhm_vals = [12.3, 22.7, 32.5]
Cu_fwhm_errors = [0.575, 0.575, 0.575]

Cu1_O1_fwhm_vals = [22.7, 35.7, 36.0]
Cu1_O1_fwhm_errors = [0.575, 1.184, 2.297]

Out_of_phase_fwhm_vals = [21.3, 22.3, 20.4]
Out_of_phase_fwhm_errors = [0.575, 0.678, 0.596]

Cu_colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

# First subplot
bax = brokenaxes(ylims=((0, 35), (135, 150)), hspace=.1)

for i in range(len(Cu_vals)):
    bax.errorbar(i + 1, Cu_vals[i], yerr=Cu_errors[i], fmt='o', capsize=5, markersize=5, color=Cu_colors[i], label='Cu Peak')
    bax.errorbar(i + 1, Cu_fwhm_vals[i], yerr=Cu_fwhm_errors[i], fmt='x', color=Cu_colors[i], label='Cu FWHM')
bax.xticks(range(1, len(x_labels) + 1), x_labels, rotation=45)
bax.title('Cu2 Mode')
bax.xlim(0.5, 3.5)
bax.legend()
bax.ylabel('Wavenumber {cm${^-1}$)')
# plt.tight_layout()
bax.show()
