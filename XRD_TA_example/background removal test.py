import matplotlib.pyplot as plt
from BaselineRemoval import BaselineRemoval
import numpy as np
from scipy import interpolate

## TODO: Check if this approach is even better than using the Origin method. You can try other smoothing functions, maybe also it's better to do the smoothing before the background subtraction?

### Running all four background sub types ###
run_all = False
if run_all:
    figure_name = 'all four tests'

    # Reading data
    counts = np.loadtxt(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\Background subtraction python practice\01 810ybco-2b--Spectrum--002--Spec.Data 1 (Y-Axis).txt")
    wavenumber = np.loadtxt(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\Background subtraction python practice\01 810ybco-2b--Spectrum--002--Spec.Data 1 (X-Axis).txt")

    # Setting up raw array and inputting it as an object to BaselineRemoval
    baseObj=BaselineRemoval(counts)

    # Background removal for ModPoly and IModPoly algorithms
    ## TODO: Run a for loop that plots different polynomials to determine which is good enough
    poly_degree=16

    # Performing different background subtractions
    Modpoly_subtracted=baseObj.ModPoly(poly_degree)
    Imodpoly_subtracted=baseObj.IModPoly(poly_degree)
    Zhangfit_subtracted=baseObj.ZhangFit()

    fig, axes = plt.subplots(2, 2, figsize=(16,16))

    # Raw data
    axes[0,0].plot(wavenumber, counts)
    axes[0,0].set_title('Raw Data')

    axes[0,1].plot(Modpoly_subtracted)
    axes[0,1].set_title('Modpoly (p=2)')

    axes[1,0].plot(Imodpoly_subtracted)
    axes[1,0].set_title('Imodpoly (p=2)')

    axes[1,1].plot(Zhangfit_subtracted)
    axes[1,1].set_title('Zhangfit')

    #plt.show()

    save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\Background subtraction python practice\{}.png".format(figure_name)
    plt.savefig(save_path)

### Run for loop to test polynomial functions ###
polynomial_test = False
if polynomial_test:
    # Reading data
    counts = np.loadtxt(
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\Background subtraction python practice\01 810ybco-2b--Spectrum--002--Spec.Data 1 (Y-Axis).txt")
    wavenumber = np.loadtxt(
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\Background subtraction python practice\01 810ybco-2b--Spectrum--002--Spec.Data 1 (X-Axis).txt")

    poly_degree = 1
    poly_limit = 16

    for x_file, y_file in zip(wavenumber, counts):
        while poly_degree < poly_limit + 1:
            # Setting up raw array and inputting it as an object to BaselineRemoval
            baseObj = BaselineRemoval(counts)

            # Performing different background subtractions
            Modpoly_subtracted = baseObj.ModPoly(poly_degree)
            Imodpoly_subtracted = baseObj.IModPoly(poly_degree)

            fig, axes = plt.subplots(1, 3, figsize=(12, 8))

            # Raw data
            axes[0].plot(wavenumber, counts)
            axes[0].set_title('Raw Data')

            axes[1].plot(Modpoly_subtracted)
            axes[1].set_title('Modpoly (p = {})'.format(poly_degree))

            axes[2].plot(Imodpoly_subtracted)
            axes[2].set_title('Imodpoly (p = {})'.format(poly_degree))

            poly_degree += 1

            plt.tight_layout()
            save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\Background subtraction python practice\polynomial_variation\Polynomialdegree{}.png".format(poly_degree)
            plt.savefig(save_path)
            plt.close()
            #plt.show()

        print('Figures are saved in {}'.format(save_path))



### Run for loop to test smoothing using scipy smoothing functions ###
smoothing_test = True
if smoothing_test:
    # Reading data
    counts = np.loadtxt(
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\Background subtraction python practice\01 810ybco-2b--Spectrum--002--Spec.Data 1 (Y-Axis).txt")
    wavenumber = np.loadtxt(
        r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\Background subtraction python practice\01 810ybco-2b--Spectrum--002--Spec.Data 1 (X-Axis).txt")

    # Performing different smoothing functions
    counts_spline=interpolate.UnivariateSpline(wavenumber, counts)

    fig, axes = plt.subplots(1, 2, figsize=(12,12))

    # Raw data
    axes[0].plot(wavenumber, counts)
    axes[0].set_title('Raw Data')

    axes[1].plot(wavenumber, counts_spline(wavenumber))
    axes[1].set_title('Univariate Spline (k=3)')

    plt.show()

    # axes[1,0].plot(Imodpoly_subtracted)
    # axes[1,0].set_title('Imodpoly (p=2)')
    #
    # axes[1,1].plot(Zhangfit_subtracted)
    # axes[1,1].set_title('Zhangfit')




    # poly_degree = 1
    # poly_limit = 16
    #
    # for x_file, y_file in zip(wavenumber, counts):
    #     while poly_degree < poly_limit + 1:
    #         # Setting up raw array and inputting it as an object to BaselineRemoval
    #         baseObj = BaselineRemoval(counts)
    #
    #         fig, axes = plt.subplots(1, 3, figsize=(12, 8))
    #
    #         # Raw data
    #         axes[0].plot(wavenumber, counts)
    #         axes[0].set_title('Raw Data')
    #
    #         axes[1].plot(Modpoly_subtracted)
    #         axes[1].set_title('Modpoly (p = {})'.format(poly_degree))
    #
    #         axes[2].plot(Imodpoly_subtracted)
    #         axes[2].set_title('Imodpoly (p = {})'.format(poly_degree))
    #
    #         poly_degree += 1
    #
    #         plt.tight_layout()
    #         save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\Background subtraction python practice\polynomial_variation\Polynomialdegree{}.png".format(poly_degree)
    #         plt.savefig(save_path)
    #         plt.close()
    #         #plt.show()
    #
    #     print('Figures are saved in {}'.format(save_path))

