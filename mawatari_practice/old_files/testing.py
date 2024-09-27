import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate as interp

# Read in the data
data = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Techniques\PPMS\practice_data_for_scripting\Fu21Gd_practice\Magnetisation Measurements.csv",
                   header=33, usecols = ['Comment', 'Temperature (K)', 'Magnetic Field (Oe)', 'DC Moment (emu)', 'DC Std. Err. (emu)'])

data.insert(3, 'Magnetic Field (T)', data['Magnetic Field (Oe)'] * 1e-4)
data.insert(5, 'DC Moment (A m2)', data['DC Moment (emu)'] * 1e-3)
data['Comment'] = data['Comment'].astype(str)
# data = data[data['Magnetic Field (T)'] > 0]

################################
def find_index_from_temp(data):
    ix=[0]
    
    for i in range(1, len(data)):
        # Compare with the temperature of the previous row
        ix.append(i) if data['Temperature (K)'][i] < data['Temperature (K)'][i-1] - 5 else None
    # ensure last measurement is included
    ix.append(data.index[-1])
    # intervals = list(zip(start, end))

    return ix


def create_intervals(ix):
    for i in range(len(ix)-1):
        start.append(ix[i] + 1)
        end.append(ix[i+1])
    return start, end

        
def clean_data(data, std_err):
# Cleaning data based on std err column to remove spurious data points
    data.loc[data['DC Std. Err. (emu)'] > std_err, 'DC Moment (A m2)'] = None
    return data

############################################

def find_max_and_min_fields(data, ix):
    """ Function to find the max and min field values for each temperature range and return the indices as a list (1-D). This is the correct function.
    """

    fields, fields_ix = [], []
    max_ix, min_ix, zero_ix = [], [], []
    prev_ix = None

    for index, i in enumerate(ix[:-1]):
        start, end = ix[index], ix[index + 1] 

        subset = data['Magnetic Field (T)'][start:end]
        # print('----- Subset:', subset)

        max_val = subset.max()
        min_val = subset.min()
        zero_1 = abs(subset - 0).idxmin()
        # B_0 = data['Magnetic Field (T)'][B_0_index + start]  # Adjusting index for global position

        for step, val in subset.items():
            if val == max_val and val != prev_ix:
                max_ix.append(step)
                fields.append(step)
                prev_ix = val
            elif val == min_val and val != prev_ix:
                min_ix.append(step)
                fields.append(step)
                prev_ix = min_val
            elif step == zero_1 and val != prev_ix:
                zero_ix.append(step)
                prev_ix = zero_ix

    # print(max_ix, min_ix, fields)

    return max_ix, min_ix, fields

# This works, general order is min > zero > max > zero > min 

##########################################################
def plotting_raw_mawatari(data, fields):
    for i, f in enumerate(fields[:-1]):
        field = data['Magnetic Field (T)'][fields[i]:fields[i+1]]
        emu = data['DC Moment (A m2)'][fields[i]:fields[i+1]]
        plt.scatter(field, emu)
    plt.show()


###########################################################################

data = clean_data(data, 0.01)

ix = find_index_from_temp(data)
print(data)

start, end = [], []
start, end = create_intervals(ix)

max_ix, min_ix, fields = find_max_and_min_fields(data, ix)

fields = []

for index, i in enumerate(ix[:-1]):
    start, end = ix[index], ix[index + 1] 
    subset = data['Magnetic Field (T)'][start:end]
    if subset.idxmax():
        fields.append(i)
    elif abs(subset[i] - 0).idxmin():
        fields.append(i)

print('New Fields are:', fields)


###################################################################

plotting_raw_mawatari(data, fields)
##################################

# fields_plot = 




##################################################################
    # This currently plots the raw data and the interpolated data based on the max and min fields
    # However it does this by using the sorted list of indices of max and min fields
    ## TODO: check if this format works to iterate for next field, since list is ordered.

print('------ Fields:', fields)
fields_raw = data['Magnetic Field (T)'][fields[0]:fields[0+1]]
print('Fields raw:', fields_raw.iloc[0], fields_raw.iloc[-1])
emu_raw = data['DC Moment (A m2)'][fields[0]:fields[0+1]]
print('Emu raw:', emu_raw.iloc[0], emu_raw.iloc[-1])




lin_start = fields_raw.iloc[0]
lin_end = fields_raw.iloc[-1]
interp_func = interp.interp1d(fields_raw, emu_raw, kind='linear')
fields_interp = np.linspace(lin_start, lin_end, 1000)
print(len(fields_interp))

mag_interp = interp_func(fields_interp)


plt.plot(fields_interp, mag_interp, label = 'interp')
plt.plot(fields_raw, emu_raw, label = 'raw')
plt.legend()
plt.show()

### checking if it works as a loop - IT DOES!! bit wonky though
for i in range(len(fields)-1):
    fields_raw = data['Magnetic Field (T)'][fields[i]:fields[i+1]]
    emu_raw = data['DC Moment (A m2)'][fields[i]:fields[i+1]]
    # plt.plot(fields_raw, emu_raw, label = 'raw')

    lin_start = fields_raw.iloc[0]
    lin_end = fields_raw.iloc[-1]
    interp_func = interp.interp1d(fields_raw, emu_raw, kind='linear')
    fields_interp = np.linspace(lin_start, lin_end, 1000)
    mag_interp = interp_func(fields_interp)
    plt.plot(fields_interp, mag_interp, label = 'interp')
plt.show()

## TODO: rectify this as you only need Jc for B > 0!!!









# This code currently works to plot raw and interpolated data but uses max and min field idx

# fields_neg = data['Magnetic Field (T)'][min_ix[0]:max_ix[0]]
# # fields_pos = fields_neg.reverse()
# emu_neg = data['DC Moment (A m2)'][min_ix[0]:max_ix[0]]

# # setting up interp
# interp_func = interp.interp1d(fields_neg, emu_neg, kind='linear')
# fields_interp = np.linspace(fields_neg.iloc[0], fields_neg.iloc[-1], 1000)
# del_mag_interp = interp_func(fields_interp)

# plt.plot(fields_interp, del_mag_interp, label = 'interp')
# plt.plot(fields_neg, emu_neg, label = 'raw')

