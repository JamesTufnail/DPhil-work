import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# Read the data
data = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\Pristine XRD Data\c axis\SM-pristine.xlsx",
                     sheet_name='Fu21Gd1', header=None)

print(data)