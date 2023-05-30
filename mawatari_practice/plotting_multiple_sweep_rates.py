# hzd to write pip install pandas in terminal to install pandas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# defining read csv as data, then creating dataframe for the two columns (r in bracket below is to take care of special characters in the path)
#   TODO: sum the below over each of the three samples measured i the MRF. Probably
#       by reading into here and then manipulating pandas to find mean values
Fu21Gd1_20K_5T_data = pd.read_csv(
    r'/home/jt2030/Documents/Birmingham data/Fu21Gd1_processsed/Mawatari_20K,5T_proc1.csv')
Fu21Gd1_20K_135T_data = pd.read_csv(
    r'/home/jt2030/Documents/Birmingham data/Fu21Gd1_processsed/Mawatari_20K,13,5T_proc.csv')
Fu21Gd1_30K_5T_data = pd.read_csv(r'/home/jt2030/Documents/Birmingham data/Fu21Gd1_processsed/Mawatari_30K,5T_proc.csv')
Fu21Gd1_30K_135T_data = pd.read_csv(
    r'/home/jt2030/Documents/Birmingham data/Fu21Gd1_processsed/Mawatari_30K,13,5T_proc.csv')
Fu21Gd1_70K_05T_data = pd.read_csv(
    r'/home/jt2030/Documents/Birmingham data/Fu21Gd1_processsed/Mawatari_77K,0,5T_proc.csv')

# assigning csv file to panda dataframe
Fu21Gd1_20K_5T = pd.DataFrame(Fu21Gd1_20K_5T_data, columns=['DC Moment (emu)', 'Magnetic Field (Oe) 100 Oe/s'
    , 'Magnetic Field (Oe) 75 Oe/s', 'Magnetic Field (Oe) 50 Oe/s', 'Magnetic Field (Oe) 25 Oe/s', 'Magnetic Field (Oe) 10 Oe/s',
                                                            'Magnetic Field (Oe) 5 Oe/s'])

# Fu21Gd1_20K_135T = pd.DataFrame(Fu21Gd1_20K_135T_data, columns=['Magnetic Field (Oe)', 'DC Moment (emu)'])
# Fu21Gd1_30K_5T = pd.DataFrame(Fu21Gd1_30K_5T_data, columns=['Magnetic Field (Oe)', 'DC Moment (emu)'])
# Fu21Gd1_30K_135T = pd.DataFrame(Fu21Gd1_30K_135T_data, columns=['Magnetic Field (Oe)', 'DC Moment (emu)'])
# Fu21Gd1_77K_05T = pd.DataFrame(Fu21Gd1_70K_05T_data, columns=['Magnetic Field (Oe)', 'DC Moment (emu)'])

# appending another column by converting to tesla
Fu21Gd1_20K_5T['Magnetic Field (T) 10 mT/s'
    , 'Magnetic Field (T) 7.5 mT/s', 'Magnetic Field (T) 5 mT/s', 'Magnetic Field (T) 2.5 mT/s', 'Magnetic Field (T) 1.0 mT/s',
                                                            'Magnetic Field (T) 0.5 mT/s'] = Fu21Gd1_20K_5T['Magnetic Field (Oe) 100 Oe/s'
    , 'Magnetic Field (Oe) 75 Oe/s', 'Magnetic Field (Oe) 50 Oe/s', 'Magnetic Field (Oe) 25 Oe/s', 'Magnetic Field (Oe) 10 Oe/s',
                                                            'Magnetic Field (Oe) 5 Oe/s'] * 0.0001
# Fu21Gd1_20K_135T['Magnetic Field (T)'] = Fu21Gd1_20K_135T['Magnetic Field (Oe)'] * 0.0001
# Fu21Gd1_30K_5T['Magnetic Field (T)'] = Fu21Gd1_30K_5T['Magnetic Field (Oe)'] * 0.0001
# Fu21Gd1_30K_135T['Magnetic Field (T)'] = Fu21Gd1_30K_135T['Magnetic Field (Oe)'] * 0.0001
# Fu21Gd1_77K_05T['Magnetic Field (T)'] = Fu21Gd1_77K_05T['Magnetic Field (Oe)'] * 0.0001


# plotting moment vs B (T)
Fu21Gd1_20K_5T.plot.scatter('Magnetic Field (T) 10 mT/s'
    , 'Magnetic Field (T) 5 mT/s', 'Magnetic Field (T) 2.5 mT/s', 'Magnetic Field (T) 1.0 mT/s',
                                                            'Magnetic Field (T) 0.5 mT/s' 'DC Moment (emu)', marker='.')
plt.title('20K, 5T')
plt.xlabel('Field (T)')
plt.ylabel('Magnetic Moment (Am^2)')
