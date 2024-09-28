import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from scipy.stats import norm
from scipy.optimize import curve_fit

# Gaussian function
def gaussian(x, mu, sigma, amplitude):
    return amplitude * np.exp(-((x - mu)**2) / (2 * sigma**2))


# Lorentzian function
def lorentzian(x, x0, gamma, amplitude):
    return (amplitude /2*np.pi) * (gamma) / ((x - x0)**2 + (gamma/2)**2)


# Sample name
sample_name = 'Tc#6 Gamma'
path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\post gamma\Tc\20240618_james tc #6 warming\tc #6 gamma.csv"

# Load the data
data = pd.read_csv(path)
print(data.head())

plt.plot(data['Temperature (K)'], data['Voltage (V)'])
plt.show()




# Calculate the first derivative
data['dV/dT'] = np.gradient(data['Voltage (V)'], data['Temperature (K)'])

# Remove NaN values and infinite values
data = data[~data.isin([np.nan, np.inf, -np.inf]).any(axis=1)]
data.reset_index(drop=True, inplace=True)

# Find the index of the maximum value in dV/dT
transition_region = data[(data['Temperature (K)'] > 85) & (data['Temperature (K)'] < 95)]
dvdt_max_ix = transition_region['dV/dT'].idxmax() 

# Plot the first derivative
plt.scatter(data['Temperature (K)'], data['dV/dT'], marker='x', label='dV/dT')

# Find the temperature corresponding to the maximum dV/dT
tc = data['Temperature (K)'][dvdt_max_ix]
dVdT = data['dV/dT'][dvdt_max_ix]

# Plot tc and highlight the specific point with a hollow red circle
plt.scatter(tc, dVdT, facecolors='none', edgecolors='green', s=100, label='T$_c$ = {:.3f} K'.format(tc))

##################################### Fit a Gaussian curve to the transition region #################################################################
# Extract temperature and dV/dT values
x_data = transition_region['Temperature (K)']
y_data = transition_region['dV/dT']

# Initial guess for the parameters (mu, sigma, amplitude)
initial_guess = [x_data.mean(), x_data.std(), max(y_data)]

# Fit the Gaussian function to the data
params, covariance = curve_fit(gaussian, x_data, y_data, p0=initial_guess)

# Extract the fitted parameters
mu, sigma, amplitude = params
print(f"Fitted parameters: mu = {mu:.3f}, sigma = {sigma:.3f}, amplitude = {amplitude:.3f}")

# Generate points for the fitted Gaussian curve
x_fit = np.linspace(x_data.min(), x_data.max(), 1000)
y_fit = gaussian(x_fit, mu, sigma, amplitude)
plt.plot(x_fit, y_fit, 'r-', label='Fitted Gaussian, mu = {:.3f}'.format(mu), linewidth=2)



##################################### Fit a Lorentzian curve to the transition region #################################################################
# Initial guess for the parameters (x0, gamma, amplitude)
initial_guess = [x_data.mean(), 1.0, max(y_data)]

# Fit the Lorentzian function to the data
params, covariance = curve_fit(lorentzian, x_data, y_data, p0=initial_guess)

# Extract the fitted parameters
x0, gamma, amplitude = params
print(f"Fitted parameters: x0 = {x0:.3f}, gamma = {gamma:.3f}, amplitude = {amplitude:.3f}")

# Generate points for the fitted Lorentzian curve
x_fit = np.linspace(x_data.min(), x_data.max(), 1000)
y_fit = lorentzian(x_fit, x0, gamma, amplitude)
plt.plot(x_fit, y_fit, color = 'orange', label='Fitted Lorentzian, x0 = {:.3f}'.format(x0), linewidth=2)


###############################################
# annotate the plot
plt.legend()
plt.xlabel('Temperature (K)')
plt.ylabel(r'$\frac{dV}{dT}$', fontsize=16)
plt.title('First Derivative of Voltage vs Temperature for {}'.format(sample_name))
plt.tight_layout()



print("Tc: ", tc)
plt.show()


