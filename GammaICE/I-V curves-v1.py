import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt
from scipy.stats import norm
import glob as glob
import os

################ Functions ###############
def check_data(I, V):

    plt.scatter(I, V, marker='x', s=10)
    plt.xlabel('Current (A)'), plt.ylabel('Voltage ($\mu$V)')
    plt.title('Raw Data')
    plt.show()

    return

def extract_data(path):

    data = pd.read_csv(path, header = 0)
    print(data.head())
    data.dropna(inplace=True)
    data = data.drop(data[data['Measured Current [A]'] < 0].index) # dropping all neg values removes too many data points
    # data = data.drop(data[data['Keithley Voltage [V]'] < - 1e-6].index) # dropping all neg values removes too many data points

    V = data['Keithley Voltage [V]'] * 1e6
    I = data['Measured Current [A]']
    print(V, I)

    return I, V

def power_law(x, Jc, n, c):
    return Vc*(x/Jc)**n + c

def fit_power_law(x, y):
    params, covariance = opt.curve_fit(power_law, x, y)
    Jc, n, c = params
    perr = np.sqrt(np.diag(covariance))
    conf_95_percent = 1.96 * perr
    # print('Confidence intervals (95%) =', conf_95_percent)


    I_fit = np.linspace(I.min(), max(I), 100)
    V_fit = power_law(I_fit, Jc, n, c) - c
    # print('Jc =', Jc, 'n =', n, 'c =', c)
    return I_fit, V_fit, params, conf_95_percent

def I_V_plot(I, V, sample_name, save_path, save=False):
    
    I_fit, V_fit, params, conf = fit_power_law(I, V)
    Jc, n, c = params
    Jc_err, n_err, c_err = conf
    V_shift = V - c
    
    # Plot raw data
    plt.scatter(I, V_shift, marker='x', s=10,  label = 'Raw Data')

    # Plot fit
    plt.plot(I_fit, V_fit, label=r'Fit: $V = V_c \left(\frac{J}{J_c}\right)^n + c$', color='orange', linewidth=1.5)

    # Annotate plot
    plt.text(0, 2.5, 'Constants (95% Confidence)\n'
                    'J$_c$ = {} $\pm$ {:.2e} A\n'
                    'n = {} $\pm$ {}\n'
                    'c = {} $\pm$ {:.2e}'.format(round(Jc, 2), round(Jc_err, 3),
                                                round(n, 2), round(n_err, 2),
                                                round(c, 2), round(c_err, 2)),
            fontsize=8, bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.5'))


    plt.axhline(y=Vc,label = 'V$_c$ = 4 $\mu$V', color='grey', linestyle='--', linewidth=0.5)
    plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    plt.xlabel('Current (A)'), plt.ylabel('Voltage ($\mu V$)')
    plt.title('I-V Curve for {}'.format(sample_name))
    plt.legend(loc = 'upper left')

    if save:
        plt.savefig(save_path + '\\' + sample_name + '_I-V.png')
        plt.savefig(r'C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Figures' + '\\' + sample_name + '_I-V.png')
        print('Saved I-V curve for {}'.format(sample_name))
        plt.close()
    else:   
        plt.show()
        print('Plotted I-V curve for {}'.format(sample_name))

    return 

def residual_plot(I, V, params, sample_name, save_path, save=False, bin_num = 50):
    
    Jc, n, c = params
    
    fig, axs = plt.subplots(1, 2, figsize = (10, 5))

    # Calculate residuals
    residuals = V - power_law(I, Jc, n, c)

    # Scatter plot of residuals
    axs[0].scatter(I, residuals, label='Residuals', color='green', s=10)
    axs[0].axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    axs[0].set_ylabel('Residuals ($\mu V$)'), axs[0].set_xlabel('Current (A)')
    axs[0].set_title('Residuals')

    # Plot histogram of residuals
    axs[1].hist(residuals, bins=bin_num, color='green', label='Residuals', alpha=0.7, density=True)

    # Fit a normal distribution to the residuals
    mu, std = norm.fit(residuals)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)

    # Plot the PDF
    axs[1].plot(x, p, 'k', linewidth=2,label = 'Fit: $\mu$ = {:.2e}, $\sigma$ = {}'.format(mu, round(std, 2)))

    # Annotate plot
    axs[1].set_xlabel('Residuals ($\mu V$)'), axs[1].set_ylabel('Frequency')
    axs[1].set_title('Histogram with {} bins'.format(bin_num))
    axs[1].legend(loc='upper right')
    fig.suptitle('{}'.format(sample_name))
    plt.tight_layout()

    if save:
        plt.savefig(save_path + '\\' + sample_name + '_residuals.png')
        plt.savefig(r'C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Figures' + '\\' + sample_name + '_residuals.png')
        print('Saved residual plot for {}'.format(sample_name))
        plt.close()
    else:    
        plt.show()
        print('Plotted residual plot for {}'.format(sample_name))

    return


############### Constants ############
Vc = 4.0  # voltage criterion (in uV)
save = True

# state = ' Irradiated'
# base_dir = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\irradiated\Jc\Sample B (1)"
# file_names = ['Sample B_1', 'Sample B_2', 'Sample B_3', 'Sample B_4', 'Sample B_5', 'Sample B_6']

# base_dir = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\irradiated\Jc\Sample C (2)"
# file_names = ['Sample C_3', 'Sample C_4', 'Sample C_5', 'Sample C_6', 'Sample C_7', 'Sample C_8']

# state = ' Pristine'
# base_dir = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Jc\Sample A (0)"
# file_names = ['Sample A_1', 'Sample A_2', 'Sample A_3', 'Sample A_4', 'Sample A_5', 'Sample A_6']

# base_dir = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Jc\Sample D (3)"
# file_names = ['Sample D_1', 'Sample D_2', 'Sample D_3', 'Sample D_4', 'Sample D_5', 'Sample D_6']

# base_dir = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Jc\Sample E (4)"
# file_names = ['Sample E_1', 'Sample E_2', 'Sample E_3', 'Sample E_4', 'Sample E_5', 'Sample E_6']

# base_dir = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Jc\Sample F (5)"
# file_names = ['Sample F_1', 'Sample F_2', 'Sample F_3']

##########################################################################

state = ' Post-gamma'
# base_dir = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\post gamma\Sample A (0)"
# file_names = ['Sample A_1', 'Sample A_2', 'Sample A_3', 'Sample A_4', 'Sample A_5', 'Sample A_6']

# base_dir = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\post gamma\Sample B (1)"
# file_names = ['Sample B_1', 'Sample B_2', 'Sample B_3', 'Sample B_4', 'Sample B_5', 'Sample B_6']

# base_dir = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\post gamma\Sample C (2)"
# file_names = ['Sample C_1', 'Sample C_2', 'Sample C_3', 'Sample C_4', 'Sample C_5', 'Sample C_6']

# base_dir = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\post gamma\Sample D (3)"
# file_names = ['Sample D_1', 'Sample D_2', 'Sample D_3', 'Sample D_4', 'Sample D_5', 'Sample D_6']

base_dir = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\post gamma\Jc\Damaged Sample"
file_names = ['Run 1', 'Run 2', 'Run 3', 'Run 4', 'Run 5', 'Run 6']

############### Script ############

save_path = base_dir

# Use glob to search within each subfolder of "Sample B"
files = glob.glob(os.path.join(base_dir, "*", "ALL*"))


# Filter files based on size
min_size_bytes = 10000  # Specify the minimum size in bytes
filtered_files = [file for file in files if os.path.getsize(file) >= min_size_bytes]

for file in filtered_files:
    print(file[-50:], 'with size', os.path.getsize(file))

# Create an empty list to store rows
data_rows = []

for path, sample_name in zip(files, file_names):
    sample_name = sample_name + state
    I, V = extract_data(path)

    # check_data(I, V)

    I_fit, V_fit, params, conf = fit_power_law(I, V)

    Jc, n, c = params
    Jc_err, n_err, c_err = conf
    print('Jc =', Jc, 'n =', n, 'c =', c, 'with errors', Jc_err, n_err, c_err)

    # Plot I-V curve and residuals
    I_V_plot(I, V, sample_name, save_path, save=save)
    residual_plot(I, V, params, sample_name, save_path, save=save)

    # Append data to list of rows
    data_rows.append([sample_name, Jc, n, c, Jc_err, n_err, c_err])

# Create a DataFrame from the list of rows
columns = ['Sample', 'Jc', 'n', 'c', 'Jc_err', 'n_err', 'c_err']
extracted_data = pd.DataFrame(data_rows, columns=columns)
extracted_data.to_csv(save_path + '\\' + 'extracted_data.csv', index=False)

print(extracted_data)

