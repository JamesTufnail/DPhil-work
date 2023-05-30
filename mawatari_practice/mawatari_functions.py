import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def mawatari
    # read into pandas raw mawatari data, ignoring first 33 rows of preamble
    data = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Birmingham Neutron Irradiation"
                       r"\Birmingham data\data-for-manipulation-pristine-measurements\Fu21Gdo_1\Irr0\PPMS Data\22 12 07"
                       r"\Mawatari_20K,5T.csv", skiprows=33)

    df = pd.DataFrame(data, columns=['Comment', 'Magnetic Field (Oe)', 'DC Moment (emu)'])
