import matplotlib.pyplot as plot
import pandas as pd
import numpy as np

def read_data(path, zero = True, T1 = 80, T2 = 100):
    data = pd.read_csv(path, header = 0)

    resistance = data['Resistance (Ohm)'] *1e3 # convert to mOhm
    temp = data['Temperature (K)']

    indices = np.where((temp >= T1) & (temp <= T2))
    start, end = indices[0][0], indices[0][-1]
    # print('Start ({} K index):'.format(T1), start, 'End ({} K index)'.format(T2), end)

    if zero:
        # Offsetting data vertically to zero 
        c = resistance[start:end].min() # Only looking through the T1 to T2 range to ignore hysteresis effect while cooling starts to warm
        resistance = resistance - c
    else:
        pass

    return temp, resistance, start, end

# all pristine
# pristine1 = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Tc\20240315_james tc 1 warming\gamma-ice-12024-03-15-16-12-02.csv"
# pristine2 = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Tc\20240316_james gammaice tc2 warming\V_T_Log2024-03-16-13-47-15.csv"
# pristine3 = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Tc\20240316_james gammaice tc 3 warming\V_T_Log2024-03-16-16-23-24.csv"
# pristine4 = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Tc\20240317_james gammaice tc 4 warming\V_T_Log2024-03-17-13-15-43.csv"
# pristine5 = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Tc\20240317_james gammaice tc 5 warming\V_T_Log2024-03-17-15-24-28.csv"
# pristine6 = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Tc\20240318_james gamma ice tc 6 warming\V_T_Log2024-03-18-14-14-52.csv"
# pristine7 = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Tc\20240319_james gammaice 7 tc warming\V_T_Log2024-03-19-15-51-25.csv"
# pristine8 = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Tc\20240319_james gammaice tc warming 8\V_T_Log2024-03-19-19-29-47.csv"

# temp1, resistance1, start1, end1 = read_data(pristine1)
# temp2, resistance2, start2, end2 = read_data(pristine2)
# temp3, resistance3, start3, end3 = read_data(pristine3)
# temp4, resistance4, start4, end4 = read_data(pristine4)
# temp5, resistance5, start5, end5 = read_data(pristine5)
# temp6, resistance6, start6, end6 = read_data(pristine6)
# temp7, resistance7, start7, end7 = read_data(pristine7)
# temp8, resistance8, start8, end8 = read_data(pristine8)

# plot.plot(temp1[start1:end1], resistance1[start1:end1], label='Pristine 1')
# plot.plot(temp2[start2:end2], resistance2[start2:end2], label='Pristine 2')
# plot.plot(temp3[start3:end3], resistance3[start3:end3], label='Pristine 3')
# plot.plot(temp4[start4:end4], resistance4[start4:end4], label='Pristine 4')
# plot.plot(temp5[start5:end5], resistance5[start5:end5], label='Pristine 5')
# plot.plot(temp6[start6:end6], resistance6[start6:end6], label='Pristine 6')
# plot.plot(temp7[start7:end7], resistance7[start7:end7], label='Pristine 7')
# plot.plot(temp8[start8:end8], resistance8[start8:end8], label='Pristine 8')


# path1 = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Tc\20240315_james tc 1 warming\gamma-ice-12024-03-15-16-12-02.csv"
# path2 = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\ion irradiated 2nd attempt\20240504_james gammaice tc 1 irradiated warming\V_T_Log2024-05-04-16-42-30.csv"
# path3 = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\post gamma\Tc\20240612_james tc#1 warming\V_T_Log2024-06-12-17-16-21.csv"

# temp1, resistance1, start1, end1 = read_data(path1)
# temp2, resistance2, start2, end2 = read_data(path2)
# temp3, resistance3, start3, end3 = read_data(path3)

# plot.plot(temp1[start1:end1], resistance1[start1:end1], label='Pristine') 
# plot.plot(temp2[start2:end2], resistance2[start2:end2], label='4 mdpa')
# plot.plot(temp3[start3:end3], resistance3[start3:end3], label='Gamma')

path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\pristine\Tc\20240316_james gammaice tc 3 warming\V_T_Log2024-03-16-16-23-24.csv"
data = pd.read_csv(path, header = 0)

resistance = data['Resistance (Ohm)'] *1e3 # convert to mOhm
temp = data['Temperature (K)']
voltage = data['Voltage (V)'] *1e6 # convert to uV

T1 = 80
T2 = 100

indices = np.where((temp >= T1) & (temp <= T2))
start, end = indices[0][0], indices[0][-1]
# print('Start ({} K index):'.format(T1), start, 'End ({} K index)'.format(T2), end)

# c = resistance[start:end].min() # Only looking through the T1 to T2 range to ignore hysteresis effect while cooling starts to warm
# resistance = resistance - c

plot.plot(temp[start:end], voltage[start:end], label='Pristine')




plot.xlabel('Temperature (K)')
plot.ylabel('Voltage (uV)')
plot.title('Tc#3 curves')
plot.legend()
plot.xlim(80, 100)
plot.show()
