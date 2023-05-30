import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# read into pandas raw mawatari data, ignoring first 33 rows of preamble
data = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Birmingham Neutron Irradiation"
                   r"\Birmingham data\data-for-manipulation-pristine-measurements\Fu21Gdo_1\Irr0\PPMS Data\22 12 07"
                   r"\Mawatari_20K,5T.csv", skiprows=33)

df = pd.DataFrame(data, columns=['Comment', 'Magnetic Field (Oe)', 'DC Moment (emu)'])

#for i, x in enumerate(df):
   # if "Ramp" in x:
   #     indices.append(indices[i]) = 1
   # else:
    #    indices.append(indices[i]) = 0


# setting indices of where new ramp rate starts
ramp_groups = df['Comment'].str.contains('Ramp').sum()
print("There are", ramp_groups, "total sweep rates.")

Comment = df['Comment']
print(Comment)

# trying to fix this so that I can section up the individual sweep rates from
# the same big file
indices = [i for i, x in enumerate('Comment') if "Ramp" in x]
moments, fields = [], []
for i, n in enumerate(indices):
    if i < len(indices)-1:
        moments.append(Moments[indices[i]:mindices[i+1]-1])
        fields.append(Field[indices[i]:indices[i+1]-1])
    elif i == len(indices)-1:
        moments.append(Moments[indices[i]:])
        fields.append(Field[indices[i]:])

print(indices)








# this is reading through te column titled Comments and setting a value at where it finds the word "Ramp"
# indices = [i for i, x in enumerate(df[Comment]) if "Ramp" in x]
# Magnetic_Field, DC_Moment = [], []
# print(indices)

## TODO: create new data frame based on location of indices...

# Magnetic_Field.append(Magnetic_Field[i:i]-1)
# DC_Moment.append(DC_Moment[i:i])


df.plt('Magnetic Field (Oe)', 'DC Moment (emu)')

# plt.show()
# print(df)
