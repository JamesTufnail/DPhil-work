import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.optimize as opt
from scipy.optimize import minimize


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

def fit_normal_state(temp, fit_temps, fit_res, start, end, label, lines = True):
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
        plt.plot(fit_x, fit_y, linestyle = '--', linewidth = 1.0, label=label)
    else:
        pass

    return params

def line_difference(point, params1, params2):
    x, y = point
    m1, c1 = params1
    m2, c2 = params2
    return (m1*x + c1 - y)**2 + (m2*x + c2 - y)**2


def read_data(path, zero = True, T1 = 80, T2 = 100):
    data = pd.read_csv(path, header = 0)

    resistance = data['Resistance (Ohm)'] *1e3 # convert to mOhm
    temp = data['Temperature (K)']

    indices = np.where((temp >= T1) & (temp <= T2))
    start, end = indices[0][0], indices[0][-1]
    # print('Start ({} K index):'.format(T1), start, 'End ({} K index)'.format(T2), end)

    if zero:
        # Offsetting data vertically to zero 
        c = resistance[start:end].min() # Only looking through the T1 to T2 range to ignore hysteresis effect while cooling starts to warm
        resistance = resistance - c
    else:
        pass

    return temp, resistance, start, end


def find_interpolation_Tc(temp, resistance, interp_lines = True,  t_fit_range= 'Top'):
    '''
    Find the intersection between the normal state and transition lines
    '''

    # Finding indices for critical temperatures and normal state based on R(100K) value to be used as rough indices for fitting
    r_100K = resistance[np.argmin(np.abs(temp - 100))]
    r_100_ix = np.argmin(np.abs(resistance - r_100K))
    tc_10_ix = np.argmin(np.abs(resistance - r_100K*0.1))
    tc_50_ix = np.argmin(np.abs(resistance - r_100K*0.5))
    tc_75_ix = np.argmin(np.abs(resistance - r_100K*0.75))
    tc_90_ix = np.argmin(np.abs(resistance - r_100K*0.9))

    # Finding indices for SC state
    t_SC_0 = np.argmin(temp)
    t_SC_1 = np.argmin(np.abs(temp-88))
    print('t_SC_0:', t_SC_0, 't_SC_1:', t_SC_1)

    # Finding temperature and resistance arrays for normal state and transition for fitting
    temp_normal_state, res_normal_state = temp[tc_90_ix:r_100_ix], resistance[tc_90_ix:r_100_ix] # Fitting linear line to normal state
    normal_params = fit_normal_state(temp, temp_normal_state, res_normal_state, start, end, 'Normal region', lines = interp_lines) # fitting linear line to normal state

    if t_fit_range == 'Top':
        temp_2, res_2 = temp[tc_50_ix:tc_75_ix], resistance[tc_50_ix:tc_75_ix] # Fitting top half of slope in transition if 'Top' selected
        transition_params = fit_transition(temp, resistance, temp_2, res_2, lines = interp_lines)
    else:
        temp_1, res_1 = temp[tc_10_ix:tc_75_ix], resistance[tc_10_ix:tc_75_ix] # Fitting whole slope in transition if nothing selected
        transition_params = fit_transition(temp, resistance, temp_1, res_1, lines = interp_lines)

    # Find the intersection between the normal state and transition lines
    initial_guess = [89, 15] # Initial guess for the intersection point (can be any point)
    result = minimize(line_difference, initial_guess, args=(normal_params, transition_params)) # Minimize the difference function
    tc_x1, tc_y = result.x # Extract the intersection point
    print('Tc1 =', tc_x1, ' K')


    # Finding arrays for SC state and transition for fitting
    temp_SC_state, res_normal_state = temp[t_SC_0:t_SC_1], resistance[t_SC_0:t_SC_1] # Fitting linear line to SC state
    SC_params = fit_normal_state(temp, temp_SC_state, res_normal_state, start, end, 'SC Region', lines = interp_lines) # fitting linear line to normal state
    
    # Find the intersection between the normal state and transition lines
    initial_guess = [89, 15] # Initial guess for the intersection point (can be any point)
    result = minimize(line_difference, initial_guess, args=(SC_params, transition_params)) # Minimize the difference function
    tc_x2, tc_y = result.x # Extract the intersection point
    print('Tc2 =', tc_x2, ' K')

    # print('Tc =', tc_x, 'Tc_10', temp[tc_10_ix], 'Tc_50', temp[tc_50_ix], 'R_100K =', r_100K, 'mOhm')
    return tc_x1, tc_x2

##################
path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Tc\20240317_james gammaice tc 4 warming\V_T_Log2024-03-17-13-15-43.csv"
sample_name = 'Tc#4 Pristine' # 2 mdpa He$^{2+}$'

# Reading data
temp, resistance, start, end = read_data(path, zero = True, T1 = 80, T2 = 100)

# Plotting raw data
plt.plot(temp[start:end], resistance[start:end], label='Raw') 

# Interpolating Tc
Tc1, Tc2 = find_interpolation_Tc(temp, resistance, interp_lines = True, t_fit_range='Bottom')
del_tc = Tc1 - Tc2

# Annotating plot
plt.xlim(84.5,95.5)
plt.ylim(-0.5, resistance[np.argmin(np.abs(temp - 100))] + 0.5)
plt.title(sample_name)
plt.ylabel('Resistance (mOhm)')
plt.xlabel('Temperature (K)')
plt.legend(loc='upper left')

# Plot vertical line at intersection Tc
plt.vlines(Tc1, min(resistance[start:end]), max(resistance[start:end]),
            color='k', linestyle='--', linewidth=1.0, label='T$_c1$'.format(round(Tc1, 2)))
plt.vlines(Tc2, min(resistance[start:end]), max(resistance[start:end]),
            color='k', linestyle='--', linewidth=1.0, label='T$_c2$'.format(round(Tc2, 2)))

# Add text boz with Tc and transition width
plt.text(0.7, 0.15,
        'Tc1 = {} K\n'
        'Tc2 = {} K\n'
        'ΔT$_c$ = {} K'
            .format(round(Tc1, 2), round(Tc2, 2), round(del_tc, 3)),
            transform=plt.gca().transAxes, fontsize=10, ha='left', va='center',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))

print('Tc1', Tc1, 'Tc2', Tc2, 'ΔTc', del_tc)
plt.show()