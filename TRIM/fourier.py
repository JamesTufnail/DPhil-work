# script to plot fourier series analytically
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-30, 30, 1000)
f = 2.5*np.cos(1.2*x) + 0.9*np.sin(0.4*x)

plt.plot(x, f)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.show()

