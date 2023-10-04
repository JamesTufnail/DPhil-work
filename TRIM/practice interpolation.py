import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import simps

# Sample data with different intervals
x1 = np.array([0, 1, 2, 3])  # X values for dataset 1
y1 = np.array([1, 2, 4, 3])  # Y values for dataset 1

x2 = np.array([2.5, 3.5, 4.5, 5.5])  # X values for dataset 2
y2 = np.array([2, 3, 5, 4])  # Y values for dataset 2

# Create a common x-axis grid that spans both datasets
common_x = np.linspace(min(x1.min(), x2.min()), max(x1.max(), x2.max()), num=1000)

# Interpolate both datasets onto the common grid
interp_func1 = interp1d(x1, y1, kind='linear', fill_value='extrapolate')
interp_func2 = interp1d(x2, y2, kind='linear', fill_value='extrapolate')

y1_on_common_grid = interp_func1(common_x)
y2_on_common_grid = interp_func2(common_x)

# Calculate the product of the interpolated values
product_values = y1_on_common_grid * y2_on_common_grid

# Calculate the integral using Simpson's rule
integral = simps(product_values, common_x)

print("Integral of the product:", integral)





