# printing raw jt1.1-1 data


import pandas as pd
import numpy
import matplotlib.pyplot as plt
from pandas import DataFrame

# set variables
x_lim = 950

raw = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\DPhil_files_for_python\REBCO RAMAN Measurements\Background_subtraction_comparisons\JT1.1-1asymmetricleastsquares.xlsx",
                    usecols=[0, 1], skiprows=[0])

print(raw)

plt.plot(raw['Unnamed: 0'], raw['Unnamed: 1'])
plt.xlim(right = x_lim)
plt.show()
