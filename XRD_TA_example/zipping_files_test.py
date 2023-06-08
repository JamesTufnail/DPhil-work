import numpy as np


counts = np.loadtxt(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\Background subtraction python practice\01 810ybco-2b--Spectrum--002--Spec.Data 1 (Y-Axis).txt")
wavenumber = np.loadtxt(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\Background subtraction python practice\01 810ybco-2b--Spectrum--002--Spec.Data 1 (X-Axis).txt")

file_name = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\Background subtraction python practice\01 810ybco-2b--Spectrum--002--Spec.Data 1 (Y-Axis).txt"
zipped_name = file_name[-51:-13]
save_path = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Raman Spectroscopy\MRF Raman\YBCO Thin Films Comparison Data - RAW\Setting22_light_RAW\Zipped Files for Origin\{}.txt".format(zipped_name)

zipped = np.column_stack((wavenumber, counts))

np.savetxt(save_path, zipped)




