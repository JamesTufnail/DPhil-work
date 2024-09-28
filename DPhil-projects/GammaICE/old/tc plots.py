import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt
from scipy.optimize import minimize

# Fischer
# To obtain the transition temperature, 
# Tc, the transition tangent was intersected with the 
# linear extrapolation of the normal state behavior in zero field

# Prokopec
# Tc and Tirr (B) were obtained from the intersection of the transition
# tangent with a linear fit of the normal conducting region (Tc) or zero (Tirr), respectively.

# Iliffe
# Tc is defined in this work as the temperature at which the sample resistance falls to 50% of that measured at 100 K (Tc,50%). 
# The width of the transition (∆Tc) is defined as the temperature range over which the sample resistance changes from 10% (Tc,10%) to 90% (Tc,90%) of that measured at 100 K
# Tc was measured during sample warming to minimise temperature errors using a constant current of ≈0.11 A. 

################################ Functions ###############
# Importing data - NOTE use warming file
def read_data(path, zero = True, T1 = 80, T2 = 100):
    data = pd.read_csv(path, header = 0)

    resistance = data['Resistance (Ohm)'] *1e3 # convert to mOhm
    temp = data['Temperature (K)']

    indices = np.where((temp >= T1) & (temp <= T2))
    start, end = indices[0][0], indices[0][-1]
    print('Start ({} K index):'.format(T1), start, 'End ({} K index)'.format(T2), end)

    if zero:
        # Offsetting data vertically to zero 
        c = resistance[start:end].min() # Only looking through the T1 to T2 range to ignore hysteresis effect while cooling starts to warm
        resistance = resistance - c
    else:
        pass

    return temp, resistance, start, end

def find_percentage_Tc(temp, resistance, r_100 = 100, vlines = True, save=False, save_path = None):

    r_100K = resistance[np.argmin(np.abs(temp - r_100))] # find resistance at 100K in Ohms
    Tc_50_percent = temp[np.argmin(np.abs(resistance - r_100K*0.5))] # find temperature at which resistance is 50% of 100K resistance
    Tc_10_percent = temp[np.argmin(np.abs(resistance - r_100K*0.1))] # find temperature at which resistance is 10% of 100K resistance
    Tc_90_percent = temp[np.argmin(np.abs(resistance - r_100K*0.9))] # find temperature at which resistance is 90% of 100K resistance
    Tc_transition = Tc_90_percent - Tc_10_percent # find width of transition
    
    print('Based on percentages of normal state resistance:')
    print('Tc_10_percent:', Tc_10_percent, 'Tc_50_percent:', Tc_50_percent, 'Tc_90_percent:', Tc_90_percent)
    print('Tc_transition:', Tc_transition, 'R_100K:', r_100K, 'mOhm')

    
    if vlines:
        ## TODO - remove start:end 
        plt.vlines(Tc_90_percent, min(resistance[start:end]), max(resistance[start:end]), color='r', linestyle='--', linewidth=1.0, label='T$_{c, 90\%}$')
        plt.vlines(Tc_50_percent, min(resistance[start:end]), max(resistance[start:end]), color='b', linestyle='--', linewidth=1.0, label='T$_{c, 50\%}$')
        plt.vlines(Tc_10_percent, min(resistance[start:end]), max(resistance[start:end]), color='g', linestyle='--', linewidth=1.0, label='T$_{c, 10\%}$')

        plt.text(0.6, 0.2,
                'T$_c$ (10%) = {} K\n'
                'T$_c$ (50%) = {} K\n'
                'T$_c$ (90%) = {} K\n'
                '$\Delta$T$_c$ = {} K\n'
                'R(100K) = {} m$\Omega$'
                 .format(round(Tc_10_percent, 2), round(Tc_50_percent, 2), round(Tc_90_percent, 2), 
                         round(Tc_transition, 2), round(resistance[np.argmin(np.abs(temp - 100))], 2)),
                 transform=plt.gca().transAxes, fontsize=10, ha='left', va='center',
                 bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))
    else:
        pass

    return Tc_50_percent, Tc_transition


def linear_fit(x, m, c):
    return m*x + c

def fit_transition(temp, resistance, fit_temps, fit_res, lines = True):
    '''
    Fit linear line to transition

    Inputs:
    temp: temperature array of entire data
    resistance: resistance array of entire data
    fit_temps: temperature array for transition for fitting
    fit_res: resistance array for transition for fitting

    Returns:
    None
    '''
    # print(fit_res)
    # print('Length of fit_res:', len(fit_res))

    params, covariance = opt.curve_fit(linear_fit, fit_temps, fit_res)
    m, c = params
    fit_x = np.linspace(temp[np.argmin(resistance)], temp[np.argmax(resistance)], 1000)
    fit_y = linear_fit(fit_x, m, c)

    if lines:
        plt.plot(fit_x, fit_y, linestyle = '--', linewidth = 1.0, label='Transition Fit')
    else:
        pass

    return params

def fit_normal_state(temp, fit_temps, fit_res, start, end, lines = True):
    '''
    Fit linear line to normal state
    
    Inputs:
    temp: temperature array
    fit_temps: temperature array for normal state for fitting
    fit_res: resistance array for normal state for fitting
    start: start index for normal state for plotting (Tc_90 index)
    end: end index for normal state for plotting (R_100K index)
    
    Returns:
    None
    '''
    params, covariance = opt.curve_fit(linear_fit, fit_temps, fit_res)
    m, c = params

    fit_x = np.linspace(temp[start], temp[end], 1000)
    fit_y = linear_fit(fit_x, m, c)

    if lines:
        plt.plot(fit_x, fit_y, linestyle = '--', linewidth = 1.0, label='Normal State Fit')
    else:
        pass

    return params

def line_difference(point, params1, params2):
    x, y = point
    m1, c1 = params1
    m2, c2 = params2
    return (m1*x + c1 - y)**2 + (m2*x + c2 - y)**2

def find_interpolation_Tc(temp, resistance, interp_lines = True, vlines=True, t_fit_range= 'Top'):
    '''
    Find the intersection between the normal state and transition lines
  
    ## TODO confirm that Tc found here is 0.9 from Iliffe definition

    '''

    # Finding indices for critical temperatures and normal state based on R(100K) value to be used as rough indices for fitting
    r_100K = resistance[np.argmin(np.abs(temp - 100))]
    r_100_ix = np.argmin(np.abs(resistance - r_100K))
    tc_10_ix = np.argmin(np.abs(resistance - r_100K*0.1))
    tc_50_ix = np.argmin(np.abs(resistance - r_100K*0.5))
    tc_75_ix = np.argmin(np.abs(resistance - r_100K*0.75))
    tc_90_ix = np.argmin(np.abs(resistance - r_100K*0.9))

    # Finding temperature and resistance arrays for normal state and transition for fitting
    ##TODO: make this more general - offer input percentages to calculate Tc
    temp_normal_state, res_normal_state = temp[tc_90_ix:r_100_ix], resistance[tc_90_ix:r_100_ix] # Fitting linear line to normal state
    normal_params = fit_normal_state(temp, temp_normal_state, res_normal_state, start, end, lines = interp_lines) # fitting linear line to normal state

    if t_fit_range == 'Top':
        temp_2, res_2 = temp[tc_50_ix:tc_75_ix], resistance[tc_50_ix:tc_75_ix] # Fitting top half of slope in transition if 'Top' selected
        transition_params = fit_transition(temp, resistance, temp_2, res_2, lines = interp_lines)
    else:
        temp_1, res_1 = temp[tc_10_ix:tc_75_ix], resistance[tc_10_ix:tc_75_ix] # Fitting whole slope in transition if nothing selected
        transition_params = fit_transition(temp, resistance, temp_1, res_1, lines = interp_lines)

    # Find the intersection between the normal state and transition lines
    initial_guess = [89, 15] # Initial guess for the intersection point (can be any point)
    result = minimize(line_difference, initial_guess, args=(normal_params, transition_params)) # Minimize the difference function
    tc_x, tc_y = result.x # Extract the intersection point
    print('Tc =', tc_x, ' K')

    # Find the transition width based on using interpolated tc as 90% and finding 10% from that
    tc_ix = np.argmin(np.abs(tc_x - temp)) # Find the index of Tc assuming it is 90%
    tc_10_ix = np.argmin(np.abs(resistance - resistance[tc_ix] / 9)) # Find the index of 10%
    tc_50_ix = np.argmin(np.abs(resistance - resistance[tc_ix] * 5 / 9)) # Find the index of 50%

    Tc_transition = temp[tc_ix] - temp[tc_10_ix] # Find the width of the transition

    if vlines:
        # Plot vertical line at intersection Tc
        plt.vlines(tc_x, min(resistance[start:end]), max(resistance[start:end]),
                    color='k', linestyle='--', linewidth=1.0, label='T$_c$'.format(round(tc_x, 2)))
        
        # Add text boz with Tc and transition width
        plt.text(0.7, 0.15,
                'T$_c$ = {} K\n'
                '$\Delta$T$_c$ = {} K'
                 .format(round(tc_x, 2), round(Tc_transition, 2)),
                 transform=plt.gca().transAxes, fontsize=10, ha='left', va='center',
                 bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))
    else:
        pass

    print('Tc =', tc_x, 'Tc_10', temp[tc_10_ix], 'Tc_50', temp[tc_50_ix], 'Tc_transition =', Tc_transition, 'K', 'R_100K =', r_100K, 'mOhm')
    return tc_x, Tc_transition


######################### Variables #################################
path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Tc\20240319_james gammaice tc warming 8\V_T_Log2024-03-19-19-29-47.csv"
save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Pristine Tc"

sample_name = 'Pristine #8'
extrapolate = True
save = True
######################### Main Code #################################
temp, resistance, start, end = read_data(path, zero = True, T1 = 80, T2 = 100)

# Plotting raw data
plt.plot(temp[start:end], resistance[start:end], label='Raw') 

Tc, transition = find_interpolation_Tc(temp, resistance, interp_lines = True, vlines=True, t_fit_range='Bottom')
plot_type = '_extrapolated_Tc_plot'

# Annotating plot
plt.xlim(84.5,95.5)
plt.ylim(-0.5, resistance[np.argmin(np.abs(temp - 100))] + 0.5)
plt.title('T$_c$ Plot for {}'.format(sample_name))
plt.ylabel('Resistance (mOhm)')
plt.xlabel('Temperature (K)')
plt.legend(loc='upper left')



# if extrapolate:
#     # Finding Tc based on linear interpolation of tc and normal state lines
#     Tc, transition = find_interpolation_Tc(temp, resistance, interp_lines = True, vlines=True, t_fit_range='top')
#     plot_type = '_extrapolated_Tc_plot'
# else:
#     # Finding Tc based on Iliffe definition
#     Tc_50_percent, Tc_transition = find_percentage_Tc(temp, resistance, vlines=True)
#     plot_type = '_percentage_Tc_plot'

if save:
    plt.savefig(save_path + '\\' + sample_name + plot_type +'.png')
    print('Saved Tc plot for {}'.format(sample_name))
else:
    plt.show()






