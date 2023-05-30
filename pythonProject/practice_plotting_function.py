import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
import os

# Folder Path
path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\23_188 James Tufnail"

# Change the directory
os.chdir(path)

def raman_plot_txt(sample_ID):
    data = pd.read_table(path + sample_ID)
    print(data)

raman_plot_txt(SS2_1)

#raman_plot_txt(JT 1_1_1)