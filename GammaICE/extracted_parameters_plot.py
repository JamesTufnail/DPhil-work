import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats

def plot_extracted_Jc_n_values(file, title):

    # Read in the data
    data = pd.read_csv(file, header=0, index_col=0, sep='\t')
    data = pd.DataFrame(data)
    print(data.head())
    
    sample = data.index
    Jc, Jc_err = data['Jc - Mean'], 1.96*data['Jc - Std'] # calculating 95% confidence interval based on std
    n, n_err = data['n - Mean'], 1.96*data['n - Std']
    # Jc, Jc_err = data['Jc77K (A)'], data['Jc77K err (A)']
    # n, n_err = data['n'], data['n err']

    # calculate the mean and standard deviation
    Ic_mean, Ic_std = np.average(Jc), np.std(Jc)
    n_mean, n_std = np.average(n), np.std(n)

    # Plot the data
    fig, ax = plt.subplots(1,2, figsize=(10,5))

    ax[0].errorbar(sample, Jc, yerr=Jc_err, fmt='x', elinewidth=1.0, capsize = 5.0, label='Ic')
    ax[0].set_ylabel('J$_c$ (A)')
    ax[0].set_title('Critical Current Density')
    ax[0].text(0.05, 0.3, '$\mu$ = {} A \n $\sigma$ = {} A'.format(round(Ic_mean, 2), round(Ic_std, 2)), transform=ax[0].transAxes, fontsize=10, ha='left', va='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))
    
    ax[1].errorbar(sample, n, yerr=n_err, fmt='xg', elinewidth=1.0, capsize = 5.0, label='n')
    ax[1].set_ylabel('n-value')
    ax[1].set_title('n-value')
    ax[1].text(0.05, 0.1, '$\mu$ = {} \n $\sigma$ = {}'.format(round(n_mean, 2), round(n_std, 2)), transform=ax[1].transAxes, fontsize=10, ha='left', va='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))

    # annotate the plot
    fig.suptitle(title)
    fig.supxlabel('Sample')
    plt.tight_layout()
    plt.show()

    print('Plotted Ic and n values')
    print('Not saved!')

    return 

def plot_extracted_Tc_values(sheetname):

    data = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\extracted_Jc_values.xlsx",
                    header=0, sheet_name =  sheetname)
    print(data.head())

    if sheetname == 'percent':
        title = 'T$_c$ and $\Delta$ T$_c$ of Pristine Samples Based on Percentages of 100K Resistance'
        sample = data['Sample']
        _10_percent, _50_percent, _90_percent = data['Tc_10_percent'], data['Tc_50_percent'], data['Tc_90_percent']
        tc_transition = data['Tc_transition']
        tc_transition_mean, tc_transition_std = np.average(tc_transition), np.std(tc_transition)
    elif sheetname == 'extrapolate':
        title = 'T$_c$ and $\Delta$ T$_c$ of Pristine Samples Based on Interpolation of Normal and Transition Lines'
        sample = data['Sample']
        _10_percent, _50_percent, _90_percent = data['Tc_10_percent'], data['Tc_50_percent'], data['Tc (90%)']
        tc_transition = data['Tc_transition']
        tc_transition_mean, tc_transition_std = np.average(tc_transition), np.std(tc_transition)

    # Plot the data
    fig, ax = plt.subplots(1,2, figsize=(10,5))

    ax[0].xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax[0].scatter(sample, _10_percent, marker = 'x', color = 'red', label='T$_c$ (10%)')
    ax[0].scatter(sample, _50_percent, marker = 'x', color = 'green', label='T$_c$ (50%)')
    ax[0].scatter(sample, _90_percent, marker = 'x', color = 'blue', label='T$_c$ (90%)')
    ax[0].set_ylabel('T$_c$ (K)')
    ax[0].set_title('Critical Temperature')
    ax[0].legend()
    ax[0].set_xlabel('Sample Number')
    # ax[0].text(0.05, 0.9, '$\mu$ = {} A \n $\sigma$ = {} A'.format(round(Ic_mean, 2), round(Ic_std, 2)), transform=ax[0].transAxes, fontsize=10, ha='left', va='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))

    ax[1].xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax[1].scatter(sample, tc_transition)
    ax[1].set_ylabel('$\Delta$ T$_c$ (K)')
    ax[1].set_title('Transition Width')
    ax[1].text(0.75, 0.9, '$\mu$ = {} K\n $\sigma$ = {} K'.format(round(tc_transition_mean, 3), round(tc_transition_std, 2)), transform=ax[1].transAxes, fontsize=10, ha='left', va='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))
    ax[1].set_xlabel('Sample Number')

    
    fig.suptitle(title)
    plt.tight_layout()
    plt.show()

    return
############# Main Script ############
file = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine jc.txt"
title = 'Pristine Jc and n values'

# plot_extracted_Jc_n_values(file, title)
# plot_extracted_Tc_values('percent')
# plot_extracted_Tc_values('extrapolate')


##############

file = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\post-gamma jc.txt"
title = 'Jc and n post-gamma values'

plot_extracted_Jc_n_values(file, title)

data = pd.read_csv(file, header=0, index_col=0, sep='\t')
print(data.head())

















################# New for trimmed samples #############
# files = [
# r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Jc\Sample A (0)\extracted_data.csv",
# r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Jc\Sample D (3)\extracted_data.csv",
# r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Jc\Sample E (4)\extracted_data.csv"
# ]
# names = ['Sample A (0)', 'Sample D (3)', 'Sample E (4)']
# state = ' Pristine'

# files = [r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\irradiated\Jc\Sample B (1)\extracted_data.csv",
#          r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\irradiated\Jc\Sample C (2)\extracted_data.csv"]
# names = ['Sample B (1)', 'Sample C (2)']
# state = ' Irradiated'

# files = [r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\post gamma\Sample A (0)\extracted_data.csv",
#             r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\post gamma\Sample B (1)\extracted_data.csv",
#             r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\post gamma\Sample C (2)\extracted_data.csv",
#             r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\post gamma\Sample D (3)\extracted_data.csv",
# ]
# names = ['Sample A (0)', 'Sample B (1)', 'Sample C (2)', 'Sample D (3)']
# state = ' Post-gamma'

# for file, name in zip(files, names):
#     data = pd.read_csv(file)
#     # print(data.head())

#     # Extract the data
#     sample = data['Sample'].str.extract(r'(\d+)').astype(int)
#     Jc, Jc_err = data['Jc'], data['Jc_err']
#     n, n_err = data['n'], data['n_err']

#     # calculate the mean and standard deviation
#     Jc_mean, Jc_std = np.average(Jc), np.std(Jc)
#     n_mean, n_std = np.average(n), np.std(n)
#     Jc_mean_err, n_mean_err = 1.96*Jc_std, 1.96*n_std

#     # Plot the data
#     fig, ax = plt.subplots(1,2, figsize=(10,5))

#     ax[0].errorbar(sample, Jc, yerr=Jc_err, fmt='x', elinewidth=1.0, capsize = 5.0, label='Jc')
#     ax[0].set_ylabel('J$_c$ (A)')
#     ax[0].set_title('Critical Current Density')
#     ax[0].text(0.5, 0.5, '$\mu$ = {} $\pm$ {} A (95%) \n $\sigma$ = {} A'.format(
#         round(Jc_mean, 2), round(Jc_mean_err, 2), round(Jc_std, 2)), transform=ax[0].transAxes, fontsize=10, ha='left', va='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))

#     ax[1].errorbar(sample, n, yerr=n_err, fmt='xg', elinewidth=1.0, capsize = 5.0, label='n')
#     ax[1].set_ylabel('n-value')
#     ax[1].set_title('n-value')
#     ax[1].text(0.5, 0.9, '$\mu$ = {} $\pm$ {} (95%) \n $\sigma$ = {}'.format(
#         round(n_mean, 2), round(n_mean_err, 2), round(n_std, 2)), transform=ax[1].transAxes, fontsize=10, ha='left', va='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))

#     fig.suptitle(name + state)
#     fig.supxlabel('Test Number')
#     plt.tight_layout()
#     plt.show()


