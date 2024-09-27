import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate as interp

# Read in the data
data = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Techniques\PPMS\practice_data_for_scripting\Fu21Gd_practice\Magnetisation Measurements.csv",
                   header=33, usecols = ['Comment', 'Temperature (K)', 'Magnetic Field (Oe)', 'DC Moment (emu)', 'DC Std. Err. (emu)'])

# Inserting additional columns
data.insert(3, 'Magnetic Field (T)', data['Magnetic Field (Oe)'] * 1e-4)
data.insert(5, 'DC Moment (A m2)', data['DC Moment (emu)'] * 1e-3)
data['Comment'] = data['Comment'].astype(str)

data = data[data['Magnetic Field (T)'] > 0]
data.reset_index(drop=True, inplace=True)


print(data.head())

####### Defining functions ########

def find_index_from_temp(data):
    ix=[0]
    
    for i in range(1, len(data)):
        # Compare with the temperature of the previous row
        ix.append(i) if data['Temperature (K)'][i] < data['Temperature (K)'][i-1] - 5 else None

    # ensure last measurement is included
    ix.append(data.index[-1])

    return ix

def clean_data(data, std_err):
# Cleaning data based on std err column to remove spurious data points
    data.loc[data['DC Std. Err. (emu)'] > std_err, 'DC Moment (A m2)'] = None
    return data

def extrapolate_range(data, max_fields, min_fields):
# checking for the max value of the min field rows, ignoring final value 
    min_field_max = data['Magnetic Field (T)'][min_fields[:-1]].idxmax() 
    max_field_min = data['Magnetic Field (T)'][max_fields].idxmin()
    lin_start, lin_end = data['Magnetic Field (T)'][min_field_max], data['Magnetic Field (T)'][max_field_min]

    # print('Lin start:', lin_start, 'Lin end:', lin_end)
    # print('Min field max:', min_field_max, 'Max field min:', max_field_min)

    return lin_start, lin_end

##################

data = clean_data(data, 0.01)

# ix are the indices where the temperature changes
ix = find_index_from_temp(data)
print('Indices:', ix)



# Finding max B indices first
fields = []
max_Fields = []
prev_ix = None

for index, i in enumerate(ix[:-1]):
    start, end = ix[index], ix[index + 1] 
    subset = data['Magnetic Field (T)'][start:end]
    max_val = subset.max()

    for step, val in subset.items():
        if val == max_val and val != prev_ix:
            fields.append(step)
            max_Fields.append(step)
            prev_ix = val


# print('Fields:', fields)

iterate = sorted(ix + fields)
# print(iterate)

# Then find the other indices between those
min_fields = []
for i in range(len(iterate)-1):
    start, end = iterate[i], iterate[i+1]
    # print('Start:', start, 'End:', end)

    subset = data['Magnetic Field (T)'][start:end]
    min_val = subset.min()
    

    for step, val in subset.items():
        if val == min_val and val != prev_ix:
            fields.append(step)
            min_fields.append(step)
            prev_ix = val
print('Fields:', fields)

fields_for_extrapolate = sorted(fields)
print('Fields for extrapolating:', fields_for_extrapolate)
# success



####################
# Checking we have the right indices
# for i in range(len(fields_for_extrapolate)-1):
#     # print(fields_for_extrapolate[i], fields_for_extrapolate[i+1])
#     start, end = fields_for_extrapolate[i] + 5, fields_for_extrapolate[i+1] -5

#     if fields_for_extrapolate[i+1] - fields_for_extrapolate[i] > 10:
#         plt.scatter(data['Magnetic Field (T)'][start:end], data['DC Moment (A m2)'][start:end], s=5)
# plt.show()


lin_start, lin_end = extrapolate_range(data, max_Fields, min_fields)



# Interpolating the data with the same B range
fields_interp = np.linspace(lin_start, lin_end, 1000) # Interpolating between max_min and min_max B values
interpolated_df = pd.DataFrame(fields_interp, columns =['Interpolated Fields (T)']) # Creating a new dataframe to store the interpolated data

for i in range(len(fields_for_extrapolate)-1):
    if fields_for_extrapolate[i+1] - fields_for_extrapolate[i] > 10:
        # Choosing range of raw data
        start, end = fields_for_extrapolate[i], fields_for_extrapolate[i+1]
        fields_raw = data['Magnetic Field (T)'][start:end] 
        emu_raw = data['DC Moment (A m2)'][start:end]

        # Interpolating the data
        interp_func = interp.interp1d(fields_raw, emu_raw, kind='linear', fill_value='extrapolate')
        mag_interp = interp_func(fields_interp)

        # Storing the interpolated data in a new datafram
        interpolated_df[f'Magnetisation_iteration_{i}'] = mag_interp
        # plt.plot(fields_interp, mag_interp)
plt.show()


differences_df = pd.DataFrame(fields_interp, columns =['Interpolated Fields (T)'])

# Calculating Jc
# radius of CC disc
r = 1.5e-3 

# thickness of SC layer 
t = 1.5e-6 

# volume of SC layer
V = np.pi * r **2 * t


for i in range(1, len(interpolated_df.columns), 2):
    # Get the column names for the pair
    col1 = interpolated_df.columns[i]
    col2 = interpolated_df.columns[i + 1]
 
    
    # Calculate the difference between the pair of columns and store in the differences DataFrame
    differences_df[f'delta mag_{i//2}'] = interpolated_df[col2] - interpolated_df[col1] 
    differences_df[f'Jc_{i//2}'] = differences_df[f'delta mag_{i//2}'] / V * 1.5 / r
    # plt.plot(fields_interp, differences_df[f'Jc_{i//2}'])
    plt.loglog(fields_interp, differences_df[f'Jc_{i//2}']*1e-6)

# Display the differences DataFrame
plt.ylim(1e2,1e6)
plt.ylabel('J$_c$ (A/mm$^2$)')
plt.xlabel('Magnetic Field (T)')
plt.show()


# print(interpolated_df.head())
# print(differences_df.head())
interpolated_df.to_excel('interpolated_data.xlsx')
differences_df.to_excel('differences_data.xlsx')


 



