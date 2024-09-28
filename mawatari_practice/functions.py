import numpy as np


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
    print(fit_res)
    print('Length of fit_res:', len(fit_res))

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

def line_difference(x, params1, params2):
    m1, c1 = params1
    m2, c2 = params2
    y1 = m1 * x + c1
    y2 = m2 * x + c2
    return np.sum((y1 - y2)**2)