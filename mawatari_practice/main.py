import


######### Code snippet to plot Susceptibility - Temperature plot
susceptibility = False
if susceptibility:
    indices, data_df = find_field_start(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Birmingham Neutron "
                                             r"Irradiation\Birmingham "
                                             r"data\data-for-manipulation-pristine-measurements\Fu21Gdo_1\Irr0\PPMS "
                                             r"Data\22 12 07\Susceptibility_Measurements.dat")
    print(data_df.head())
    print(data_df.tail())
    print(indices)
    magnetisation_measurements(data_df, indices)




########### Code snippet to plot multiple Mawatari files in loop #############
mawatari = False
if mawatari:
    mawatari_files = sorted(
        glob.glob(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Birmingham Neutron Irradiation\Birmingham "
                  r"data\OneDrive_2023-01-30\2023-01-20 Neutron Irradiation of Disk Samples - Lot 1 ("
                  r"copy)\Fu21Gdo_1\Irr0\PPMS Data\22 12 07\Mawatari*.csv"))
    for file_no, file in enumerate(mawatari_files):
        indices, data_df = find_ramp_start(mawatari_files[file_no])
        title = find_title_from_filename(mawatari_files[file_no], '_', 1, -4)
        multiple_raw_mawatari(data_df, indices, title)
        #final_raw_mawatari(data_df, indices, file_no)
    print(indices)
