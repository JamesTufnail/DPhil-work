import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from raman_functions import *
import sklearn.linear_model as lm
from sklearn.preprocessing import PolynomialFeatures

#
## TODO: write plotting, naing an saving function and use within each script
## TODO: Currently the first two won't work properly until I implement function to plot and save each in turn
def polynomial_regression(x, y, degree):
    """ JT - Plots a polynomial fit of the input variables

    :param x: x values - independent variable(s)
    :param y: y values - dependent variable
    :return:
    """
    x_trans = PolynomialFeatures(degree=degree)
    x_trans = x_trans.fit_transform(x)

    lin_reg = lm.LinearRegression()
    lin_reg.fit(x_trans, y)
    y_pred = lin_reg.predict(x_trans)

    r2_error = lin_reg.score(x_trans, y)
    print("R^2 is:", r2_error)

    plt.scatter(x, y, s=5)
    plt.title("Polynomial Regression of Fu21 edge with R^2 of {}".format(r2_error))
    plt.plot(x, y_pred, color='orange', label = "Fit Order: {}".format(degree))
    plt.legend()

    title = "Polynomial Regression of Fu21 edge with order {}".format(degree)
    save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\FU21 and SP11 calibration\10 degree diff plots\Interp_FU21" + '\\' + title
    plt.savefig(save_path)
    plt.close()

calibration_checking = False # This is used to plot several figures to compare whether there is systematic energy shift between samples
Fu21_plot = False # This plots standard pristine, irradiated and annealed spectra for Fu21 at 10,45,80 degrees
diff_Fu21 = False # This plots standard pristine, irradiated and annealed spectra for Fu21 at 10,45,80 degrees
diff_spectra_SP11_Fu21 = False # This is unshifted in x currently. I.e. assuming no calibration errors between samples...

edge_start = 8979.3 # Define start point for XANES region
# shifts = [0.15, 0.16, 0.17]

# calibration_checking_diff

""" TODO: either you can try difference pltos by shifting one column verticaly - will then have to determine the energy shift between each row (crica 3 eV),
    alternativaly, you can try interpolating the values between each energy iteration with a resolution of 0.1 eV and then do the subtraction
    based on the interpolated values...
"""

calibration_check_diff = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21-Python-Plots-normalised\check_FU21_Sp11_calibration.nor",
                                    skiprows=13,
                                    delim_whitespace=' ')

calibration_check_diff = pd.DataFrame(calibration_check_diff.values,
                                        columns = ['energy',  'FU21Y_p_10deg', 'FU21Y_p_45deg',  'FU21Y_p_80deg',
                                                   'SP11_p_10deg', 'SP11_p_45deg',  'SP11_p_80deg'])

# print(calibration_check_diff)
calibration_check_diff['energy'] = calibration_check_diff['energy'] - edge_start

# save = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21-Python-Plots-normalised\xanes_calibration.xlsx"
# calibration_check_diff.to_excel(save, index=False)


edge = calibration_check_diff.iloc[60:128]
x_vals = edge[["energy"]]
y_vals = edge["SP11_p_10deg"]
y_vals2 = edge["FU21Y_p_10deg"]

x_trans = PolynomialFeatures(degree=12)
x_trans = x_trans.fit_transform(x_vals)

lin_reg = lm.LinearRegression()
lin_reg.fit(x_trans, y_vals)
y_pred = lin_reg.predict(x_trans)

lin_reg2 = lm.LinearRegression()
lin_reg2.fit(x_trans, y_vals2)
y_pred2 = lin_reg2.predict(x_trans)

y_diff = y_pred - y_pred2

Fu21_SP11_diff = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21-Python-Plots-normalised\marked_SP11_diff_Fu21.nor",
                                 delim_whitespace=' ',
                                 skiprows = 14)

energy_diff_diff=Fu21_SP11_diff.iloc[:,0]
energy_diff_diff_shifted = energy_diff_diff.sub(edge_start)
Fu21_SP11_10deg_diff = Fu21_SP11_diff.iloc[:,1]

title = 'XANES Diff Spectra Experimental and Interpolated 0 eV shift values'
plt.plot(energy_diff_diff_shifted, Fu21_SP11_10deg_diff, label = 'Experimental')
plt.plot(x_vals, y_diff, label = 'Interpolated')
plt.axhline(y=0, linestyle='--', color='black', linewidth = 0.5)
plt.title(title)
plt.xlim(-5, 20)
plt.legend()
plt.show()




# orders = list(range(1, 19))
# for order in orders:
#     polynomial_regression(x_vals, y_vals2, order)








# print(calibration_check_diff.head())
# shifts = [-2, -1, 0, 1, 2]
# for i in shifts:
#     # calibration_check_diff['energy_shift'] = calibration_check_diff['energy'] + i
#
#     calibration_check_diff["Difference Plot"] = calibration_check_diff["SP11_p_10deg"] - calibration_check_diff["FU21Y_p_10deg"].shift(i)
#
#     plt.plot(calibration_check_diff["energy"], calibration_check_diff["Difference Plot"], label='{} row shift'.format(i))
# # plt.title(title)
# plt.xlim(8975 - edge_start, 20)
# plt.axhline(y=0, linestyle='--', color='black', linewidth=0.5)
# plt.legend()
# plt.show()



#################################################################
if calibration_checking:
    calibration_check = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21-Python-Plots-normalised\check_FU21_Sp11_calibration.nor",
                                    skiprows=13,
                                    delim_whitespace=' ')

    calibration_check_df = pd.DataFrame(calibration_check.values,
                                        columns = ['energy',  'FU21Y_p_10deg', 'FU21Y_p_45deg',  'FU21Y_p_80deg',
                                                   'SP11_p_10deg', 'SP11_p_45deg',  'SP11_p_80deg'])
    calibration_check_df['energy'] = calibration_check_df['energy'] - edge_start

    for i in shifts:
        calibration_check_df['energy_shift'] = calibration_check_df['energy'] + i

        plt.plot(calibration_check_df['energy'], calibration_check_df['FU21Y_p_10deg'],
                 label='FU21Y_p_10deg')
        plt.plot(calibration_check_df['energy_shift'], calibration_check_df['SP11_p_10deg'],
                 label = 'SP11_p_10deg + {} eV'.format(i),
                 linewidth=1)

        title = '10 degree SP11 and Fu21 comparison with {} eV shift in SP11'.format(i)
        plt.title(title)
        plt.xlim(8975 - edge_start, 20)
        plt.legend()
        plt.savefig(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\FU21 and SP11 calibration\10degree" +
                    '\\{}.png'.format(title))
        plt.close()





if Fu21_plot:
    Fu21 = pd.read_csv(
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21-Python-Plots-normalised\marked.nor",
        delim_whitespace=' ',
        skiprows=14)
    energy = Fu21.iloc[:, 0]
    energy_shifted = energy.sub(edge_start)

    pristine_10deg = Fu21.iloc[:, 1].astype(float)
    pristine_45deg = Fu21.iloc[:, 2].astype(float)
    pristine_80deg = Fu21.iloc[:, 3].astype(float)

    two_MeVO_10deg = Fu21.iloc[:, 4].astype(float)
    two_MeVO_80deg = Fu21.iloc[:, 5].astype(float)

    two_MeVO_ann_10deg = Fu21.iloc[:, 6].astype(float)
    two_MeVO_ann_80deg = Fu21.iloc[:, 7].astype(float)

    plt.plot(energy_shifted, pristine_10deg, label='10 Degrees')
    plt.plot(energy_shifted, pristine_45deg, label='45 Degrees')
    plt.plot(energy_shifted, pristine_80deg, label='80 Degrees')

    plt.plot(energy_shifted, pristine_10deg, label='Pristine')
    plt.plot(energy_shifted, two_MeVO_10deg, label='2 MeV O$^+$')
    plt.plot(energy_shifted, two_MeVO_ann_10deg, label='Annealed')

    plt.plot(energy_shifted, pristine_80deg, label='Pristine')
    plt.plot(energy_shifted, two_MeVO_80deg, label='2 MeV O$^+$')
    plt.plot(energy_shifted, two_MeVO_ann_80deg, label='Annealed')


if diff_Fu21:
    diff_Fu21 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21-Python-Plots-normalised\marked_diff_plots.nor",
                            delim_whitespace=' ',
                            skiprows=14)

    energy_diff = diff_Fu21.iloc[:, 0]
    energy_diff_shifted = energy_diff.sub(edge_start)

    ann_10deg_sub_p_10deg = diff_Fu21.iloc[:,1]
    _10deg_sub_p_10deg = diff_Fu21.iloc[:,2]

    ann_80deg_sub_p_80deg = diff_Fu21.iloc[:,3]
    _80deg_sub_p_80deg = diff_Fu21.iloc[:,4]

    plt.plot(energy_diff_shifted, ann_10deg_sub_p_10deg, label='Annealed')
    plt.plot(energy_diff_shifted, _10deg_sub_p_10deg, label='2 MeV O$^+$')

    plt.plot(energy_diff_shifted, ann_80deg_sub_p_80deg, label='Annealed')
    plt.plot(energy_diff_shifted, _80deg_sub_p_80deg, label='2 MeV O$^+$')


if diff_spectra_SP11_Fu21:
    Fu21_SP11_diff = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\Fu21-Python-Plots-normalised\marked_SP11_diff_Fu21.nor",
                                 delim_whitespace=' ',
                                 skiprows = 14)

    energy_diff_diff=Fu21_SP11_diff.iloc[:,0]
    energy_diff_diff_shifted = energy_diff_diff.sub(edge_start)


    Fu21_SP11_80deg_diff = Fu21_SP11_diff.iloc[:,3]
    Fu21_SP11_45deg_diff = Fu21_SP11_diff.iloc[:,2]
    Fu21_SP11_10deg_diff = Fu21_SP11_diff.iloc[:,1]

    title = 'XANES Diff Spectra for Pristine Sp11 and Fu21 Tapes at Different Degrees Beam Angles'
    plt.plot(energy_diff_diff_shifted, Fu21_SP11_10deg_diff, label = '10 Degrees')
    plt.plot(energy_diff_diff_shifted, Fu21_SP11_45deg_diff, label = '45 Degrees')
    plt.plot(energy_diff_diff_shifted, Fu21_SP11_80deg_diff, label = '80 Degrees')



