import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re

# Finding change in magnetisation

data = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Techniques\PPMS\practice_data_for_scripting\Fu21Gd_practice\Mawatari_20K,5T.csv",
                   header=33, usecols=['Comment', 'Temperature (K)', 'Magnetic Field (Oe)', 'DC Moment (emu)', 'DC Std. Err. (emu)'])

data.insert(3, 'Magnetic Field (T)', data['Magnetic Field (Oe)']/10000)
data['Comment'] = data['Comment'].astype(str)



# Cleaning data based on std err column to remove spurious data points
std_err = 0.01
data.loc[data['DC Std. Err. (emu)'] > std_err, 'DC Moment (emu)'] = None



# Indexing through 'comment' to find ramp rates
ix = []
sweep_rate = [] 

for index, comment in enumerate(data['Comment']):
    if isinstance(comment, str) and "Ramp" in comment:
        rate = int(re.findall(r'\d+', comment)[0]) / 10000 # in T/s
        ix.append(index)
        sweep_rate.append(rate)
ix.append(data.index[-1])

# print(sweep_rate)
# print(ix)
# print(data.head())
        


# Plotting Mawatari loop for cleaned data
delta_mag = []
for index, (rate, i) in enumerate(zip(sweep_rate, ix)):
    if index < len(ix) - 1:
        start = ix[index]
        end = ix[index + 1] - 1
        # print(start, end, 'rate (T/s):', rate)

        # Plot 
        plt.scatter(data['Magnetic Field (T)'][start:end], data['DC Moment (emu)'][start:end], label = '{} mT/s'.format(rate * 1e3), s=5)

        # Finding the max and min magnetisation values for each sweep rate
        max_mag = max(data['DC Moment (emu)'][start:end])
        min_mag = min(data['DC Moment (emu)'][start:end])
        delta_mag.append(max(data['DC Moment (emu)'][start:end]) - min(data['DC Moment (emu)'][start:end]))

        # print('Max mag:', max_mag, 'Min mag:', min_mag)
        # print('Delta mag:', delta_mag)

plt.legend()
plt.title('Mawatari data for the XXX sample')
plt.xlabel('Magnetic Field (T)')
plt.ylabel('DC Moment (10$^{-3}$ A m$^2$)')
plt.show()

## TODO: plot all mawatari files on same graph and make prettier

#print(delta_mag)
#print(sweep_rate)



# Calculating Jc
# radius of CC disc
r = 1.5e-3 

# thickness of SC layer 
t = 1.5e-6 

# volume of SC layer
V = np.pi * r **2 * t 



# creating dataframe for sweep rate, and delta mag
extracted_data = pd.DataFrame({'Sweep rate (T/s)': sweep_rate, 'Delta M (emu)': delta_mag})

# converting delta mag to A m^2
extracted_data['Delta M (emu)'] = extracted_data['Delta M (emu)'] * 1e-3 

# calculating Jc
extracted_data['Jc(r=R) (A/mm2)'] = 1e-6 * 1.5 * extracted_data['Delta M (emu)'] / (r*V) 

# calculating Ic per unit width
extracted_data['Icpw'] = 0.015 * extracted_data['Delta M (emu)'] / (np.pi * r **3)

# calculating E(r=R)
extracted_data['E(r=R)'] = extracted_data['Sweep rate (T/s)'] * r / 2

# Plotting Jc vs. E
plt.scatter(extracted_data['Jc(r=R) (A/mm2)'], extracted_data['E(r=R)'] * 1e6) # Converting to microV/m
plt.xscale('log'), plt.xlabel('$J_c$ ($A/mm^2$)')
plt.yscale('log'), plt.ylabel('E ($\mu$V/m)') 
# plt.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
plt.title('Jc vs. E for the XXX sample')

plt.show()


# print(extracted_data)
# print(data.head())
# 