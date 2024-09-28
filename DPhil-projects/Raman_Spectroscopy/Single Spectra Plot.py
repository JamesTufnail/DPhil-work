import matplotlib.pyplot as plt
import pandas as pd

##### Variables ######
filename = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\Coated Conductors\Fu21Y\Fu21Y_p_area.txt"
title = 'Fu21Y Pristine Fitted Raman Spectra'

#########
data = pd.read_csv(filename, delimiter = '\t', names=['Wavenumber', 'Counts']).dropna()

data_df = pd.DataFrame(data)
print(data_df)

plt.plot(data_df['Wavenumber'], data_df['Counts'], label='Pristine')
plt.xlabel('Wavenumber (cm$^{-1}$)')
plt.ylabel('Counts')
plt.title(title)
plt.show()