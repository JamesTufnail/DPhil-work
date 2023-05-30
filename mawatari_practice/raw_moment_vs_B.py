# hzd to write pip install pandas in terminal to install pandas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# defining read csv as data, then creating dataframe for the two columns (r in bracket below is to take care of special characters in the path)
#   TODO: sum the below over each of the three samples measured i the MRF. Probably
#       by reading into here and then manipulating pandas to find mean values
Fu21Gd1_20K_5T_data = pd.read_csv(
    r'/home/jt2030/Documents/Birmingham data/Fu21Gd1_processsed/Mawatari_20K,5T_proc.csv')
Fu21Gd1_20K_135T_data = pd.read_csv(
    r'/home/jt2030/Documents/Birmingham data/Fu21Gd1_processsed/Mawatari_20K,13,5T_proc.csv')
Fu21Gd1_30K_5T_data = pd.read_csv(r'/home/jt2030/Documents/Birmingham data/Fu21Gd1_processsed/Mawatari_30K,5T_proc.csv')
Fu21Gd1_30K_135T_data = pd.read_csv(
    r'/home/jt2030/Documents/Birmingham data/Fu21Gd1_processsed/Mawatari_30K,13,5T_proc.csv')
Fu21Gd1_70K_05T_data = pd.read_csv(
    r'/home/jt2030/Documents/Birmingham data/Fu21Gd1_processsed/Mawatari_77K,0,5T_proc.csv')

# assigning csv file to panda dataframe
Fu21Gd1_20K_5T = pd.DataFrame(Fu21Gd1_20K_5T_data, columns=['Magnetic Field (Oe)', 'DC Moment (emu)'])
Fu21Gd1_20K_135T = pd.DataFrame(Fu21Gd1_20K_135T_data, columns=['Magnetic Field (Oe)', 'DC Moment (emu)'])
Fu21Gd1_30K_5T = pd.DataFrame(Fu21Gd1_30K_5T_data, columns=['Magnetic Field (Oe)', 'DC Moment (emu)'])
Fu21Gd1_30K_135T = pd.DataFrame(Fu21Gd1_30K_135T_data, columns=['Magnetic Field (Oe)', 'DC Moment (emu)'])
Fu21Gd1_77K_05T = pd.DataFrame(Fu21Gd1_70K_05T_data, columns=['Magnetic Field (Oe)', 'DC Moment (emu)'])

# appending another column by converting to tesla
Fu21Gd1_20K_5T['Magnetic Field (T)'] = Fu21Gd1_20K_5T['Magnetic Field (Oe)'] * 0.0001
Fu21Gd1_20K_135T['Magnetic Field (T)'] = Fu21Gd1_20K_135T['Magnetic Field (Oe)'] * 0.0001
Fu21Gd1_30K_5T['Magnetic Field (T)'] = Fu21Gd1_30K_5T['Magnetic Field (Oe)'] * 0.0001
Fu21Gd1_30K_135T['Magnetic Field (T)'] = Fu21Gd1_30K_135T['Magnetic Field (Oe)'] * 0.0001
Fu21Gd1_77K_05T['Magnetic Field (T)'] = Fu21Gd1_77K_05T['Magnetic Field (Oe)'] * 0.0001

# creating subplot environment
# fig, axes = plt.subplots(nrows=2, ncols=2)
# Fu21Gd1_20K_5T.plot(ax=axes[0, 0])
# df2.plot(ax=axes[0, 1])
# df3.plot(ax=axes[1,0])
# df4.plot(ax=axes[1, 1])

# plotting moment vs B (T)
Fu21Gd1_20K_5T.plot.scatter('Magnetic Field (T)', 'DC Moment (emu)', marker='.')
plt.title('20K, 5T')
plt.xlabel('Field (T)')
plt.ylabel('Magnetic Moment (Am^2)')

Fu21Gd1_20K_135T.plot.scatter('Magnetic Field (T)', 'DC Moment (emu)', marker='.')
plt.title('20K, 13.5T')
plt.xlabel('Field (T)')
plt.ylabel('Magnetic Moment (Am^2)')

Fu21Gd1_30K_5T.plot.scatter('Magnetic Field (T)', 'DC Moment (emu)', marker='.')
plt.title('30K, 5T')
plt.xlabel('Field (T)')
plt.ylabel('Magnetic Moment (Am^2)')

Fu21Gd1_30K_135T.plot.scatter('Magnetic Field (T)', 'DC Moment (emu)', marker='.')
plt.title('30K, 13.5T')
plt.xlabel('Field (T)')
plt.ylabel('Magnetic Moment (Am^2)')

Fu21Gd1_77K_05T.plot.scatter('Magnetic Field (T)', 'DC Moment (emu)', marker='.')
plt.title('77K, 0.5T')
plt.xlabel('Field (T)')
plt.ylabel('Magnetic Moment (Am^2)')

plt.show()
# print(df)
