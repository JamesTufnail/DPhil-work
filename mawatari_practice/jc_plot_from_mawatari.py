import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate as interp

####### Defining functions ########

def find_index_from_temp(data):
    ix=[0]
    labels = []
    
    for i in range(1, len(data)):
        # Compare with the temperature of the previous row
        ix.append(i) if data['Temperature (K)'][i] < data['Temperature (K)'][i-1] - 5 else None

    # ensure last measurement is included
    ix.append(data.index[-1])

    
    return ix

def clean_data(data, std_err):

    # Inserting additional columns
    data.insert(3, 'Magnetic Field (T)', data['Magnetic Field (Oe)'] * 1e-4)
    data.insert(5, 'DC Moment (A m2)', data['DC Moment (emu)'] * 1e-3)
    data['Comment'] = data['Comment'].astype(str)
    data = data[data['Magnetic Field (T)'] > 0]
    data.reset_index(drop=True, inplace=True)

    # Cleaning data based on std err column to remove spurious data points
    data.loc[data['DC Std. Err. (emu)'] > std_err, 'DC Moment (A m2)'] = None

    return data

def extrapolate_range(data, max_fields, min_fields):

    # checking for the max value of the min field rows, ignoring final value 
    min_field_max = data['Magnetic Field (T)'][min_fields[:-1]].idxmax() 
    max_field_min = data['Magnetic Field (T)'][max_fields].idxmin()
    lin_start, lin_end = data['Magnetic Field (T)'][min_field_max], data['Magnetic Field (T)'][max_field_min]


    return lin_start, lin_end

def test_indices(data, fields_for_extrapolate):
    '''Function to plot the positive field part of mawatari loop to check if the indices that have been found are correct.

    Args:
    data: pandas dataframe
    fields_for_extrapolate: list of integers representing the indices of the data where the magnetic field is at a maximum or minimum

    Returns:
    None
    '''
    for i in range(len(fields_for_extrapolate)-1):
        # print(fields_for_extrapolate[i], fields_for_extrapolate[i+1])
        start, end = fields_for_extrapolate[i] + 5, fields_for_extrapolate[i+1] -5

        if fields_for_extrapolate[i+1] - fields_for_extrapolate[i] > 10:
            plt.scatter(data['Magnetic Field (T)'][start:end], data['DC Moment (A m2)'][start:end], s=5)
    
    plt.ylabel('Magnetisation (A m$^2$)')
    plt.xlabel('Magnetic Field (T)')
    plt.title('Checking Indices for Interpolation')
    plt.show()
     
    print('Indices test complete')
    return None

def finding_max_min_fields(data, ix):
    '''
    Function to find the indices of the data where the magnetic field is at a maximum or minimum.

    Args:
    data: pandas dataframe
    ix: list of integers representing the indices of the data where the temperature changes

    Returns:
    max_fields: list of integers representing the indices of the data where the magnetic field is at a maximum
    min_fields: list of integers representing the indices of the data where the magnetic field is at a minimum
    fields_for_extrapolate: list of integers representing the indices of the data where the magnetic field is at a maximum or minimum
    '''
    fields = []
    max_fields = []
    min_fields = []
    prev_ix = None

    for index, i in enumerate(ix[:-1]):
        start, end = ix[index], ix[index + 1] 
        subset = data['Magnetic Field (T)'][start:end]
        max_val = subset.max()

        for step, val in subset.items():
            if val == max_val and val != prev_ix:
                fields.append(step)
                max_fields.append(step)
                prev_ix = val

    # sort the indices
    iterate = sorted(ix + fields)

    # Then find the other indices between those
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

    return max_fields, min_fields, fields_for_extrapolate

def interp_and_plot_jc(ax, data, max_fields, min_fields, fields_for_extrapolate, labels, linestyle, colour):
    '''Function to interpolate the data and calculate the critical current density.

    Args:
    data: pandas dataframe
    max_fields: list of integers representing the indices of the data where the magnetic field is at a maximum
    min_fields: list of integers representing the indices of the data where the magnetic field is at a minimum
    fields_for_extrapolate: list of integers representing the indices of the data where the magnetic field is at a maximum or minimum
    
    Returns:
    interpolated_df: pandas dataframe containing the interpolated data
    differences_df: pandas dataframe containing the differences between the interpolated data and the critical current density
    '''

    # Interpolating the data with the same B range
    lin_start, lin_end = extrapolate_range(data, max_fields, min_fields)
    fields_interp = np.linspace(lin_start, lin_end, 10000) # Interpolating between max_min and min_max B values
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

    differences_df = pd.DataFrame(fields_interp, columns =['Interpolated Fields (T)'])

    # Calculating Jc
    r = 1.5e-3 # radius of CC disc
    t = 1.5e-6 # thickness of SC layer 
    V = np.pi * r **2 * t # volume of SC layer

    labels = pd.Series(labels)

    for i in range(1, len(interpolated_df.columns), 2):
        # Get the column names for the pair
        col1, col2 = interpolated_df.columns[i], interpolated_df.columns[i + 1]
        
        # Calculate the difference between the pair of columns and store in the differences DataFrame
        differences_df[f'delta mag_{i//2}'] = interpolated_df[col2] - interpolated_df[col1] 
        differences_df[f'Jc_{i//2}'] = differences_df[f'delta mag_{i//2}'] / V * 1.5 / r

        # section the plotting data to aid in visibility (dropping last 25 and plotting every 10th)
        field_plot = fields_interp[:-150:3]
        diff_plot = differences_df[f'Jc_{i//2}'][:-150:3]  
        ax.plot(field_plot, diff_plot * 1e-6, linestyle=linestyle,  c = colour[i//2])#, label=labels.iloc[i//2])
  
    print('Interpolation and Jc calculation complete')
    return fig, interpolated_df, differences_df

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Main Script ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# Add multiple files if you want to add multiple datasets to one plot (e.g. for pristine and irradiated 
files = [r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Magnetometry Data\OneDrive_2024-07-26\2024-01-25 James Tufnail\Fu21Gd_SM1a\24 01 24\Magnetisation Measurements.dat",
         r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Magnetometry Data\OneDrive_2024-07-26\2024-01-25 James Tufnail\Fu21Gd_SM1a\24 07 09\Magnetisation Measurements.dat"
        ]


linestyles = ['-', '--']
colours = plt.cm.viridis(np.linspace(0,1,6))


# Create a single figure and axis to plot on
fig, ax = plt.subplots(figsize=(10, 6))


for file, linestyle in zip(files, linestyles):
    print('--------------------------------- \n Running file \n', file)
    
    lin_start, lin_end = None, None
    ix, max_fields, min_fields, fields_for_extrapolate = [], [], [], []

    data = pd.read_csv(file,
                       header=33, usecols=['Comment', 'Temperature (K)', 'Magnetic Field (Oe)', 'DC Moment (emu)', 'DC Std. Err. (emu)'], low_memory=False)

    data = clean_data(data, 0.01)

    ix = find_index_from_temp(data)
    print('Indices:', ix)

    labels = [data['Temperature (K)'][i].round(0) for i in ix]
    labels = labels[:-1]
    labels = [str(int(i)) + ' K' for i in labels]
    print('Labels:', labels)
    

    max_fields, min_fields, fields_for_extrapolate = finding_max_min_fields(data, ix)

    # test_indices(data, fields_for_extrapolate)
    fig, interpolated_df, differences_df = interp_and_plot_jc(ax, data, max_fields, min_fields, fields_for_extrapolate, labels, linestyle, colours)


    print('File complete')

# This shit just to mess around with the legend for the ASC poster
# ax.plot([], [], linestyle='-', color='k', label='= Pristine')
# ax.plot([], [], linestyle='--', color='k', label='= 1.6 mdpa')
for i in range(len(colours)):
    ax.plot([], [],  c = colours[i], label=labels[i])

# Final formatting of the plot
ax.set_title('Critical Current Density vs Magnetic Field for Fu21Gd_SM1a', fontsize='large')
ax.grid(True)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylim(1e3, 1e6)
ax.set_xlim(1e-2,15)
ax.set_ylabel('J$_c$ (A/mm$^2$)', fontsize='large')
ax.set_xlabel('Applied Field (T)', fontsize='large')
ax.legend(loc='lower left', fontsize='large')
plt.show()





# interpolated_df.to_excel('interpolated_data.xlsx')
# differences_df.to_excel('differences_data.xlsx')


 



