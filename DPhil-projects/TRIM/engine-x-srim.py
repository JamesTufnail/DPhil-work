import matplotlib.pyplot as plt
import pandas as pd


damage = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\SRIM\Planned fluence-based He irradiations\Test 7 - processed\Test 7 - damage.txt",
                        sep='\t', header = 0)
print(damage.head())

damage_df = pd.DataFrame(damage)

# fluences = ['1E+15', '5E+15', '1E+16', '5E+16', '1E+17']
fluences = ['1E+15',	'2.5E+15',	'5E+15',	'7.5E+15',	'1E+16']

for fluence in fluences:
    plt.plot(damage_df["Depth (um)"], damage_df[fluence], label = fluence + " (ions/cm$^2$)")

plt.axvline(x=3, linestyle='--', linewidth = 1, color = 'grey') # REBCO layer thickness
plt.title('1 MeV He damage into 3 $\mu$m of GdBCO (Test 7)')
plt.xlabel('Depth (um)')
plt.ylabel('Damage (mdpa)')
plt.legend(loc='upper left')
plt.show()


# implantation_range = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Engine-X Experiment\EngineX SRIM\Full p range.txt",
#                             sep='\t', header=0)
# implantation_range_df= pd.DataFrame(implantation_range)

# print(implantation_range_df.head())

# plt.plot(implantation_range_df['Depth (um)'], implantation_range_df['H'], label = 'H implantation')
# # plt.axvline(x=2, linestyle='--', linewidth = 1, color = 'grey') # REBCO layer thickness
# plt.title('10 MeV H implantation into 2 $\mu$m of YBCO and 1000 $\mu$m of Hastelloy')
# plt.xlabel('Depth (um)')
# plt.ylabel('H Implantation (Atoms/cm3)')
# plt.legend(loc='upper right')
# plt.show()


# recoils = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Engine-X Experiment\EngineX SRIM\2 um YBCO - recoils.txt",
#                         sep='\t', header = 0)
# print(recoils.head())
# recoils_df= pd.DataFrame(recoils)


# plt.plot(recoils_df['Depth (um)'], recoils_df['H'] * 1000, label = 'H')
# plt.plot(recoils_df['Depth (um)'], recoils_df['O'] * 1000, label = 'O')
# plt.plot(recoils_df['Depth (um)'], recoils_df['Y'] * 1000, label = 'Y')
# plt.plot(recoils_df['Depth (um)'], recoils_df['Ba'] * 1000, label = 'Ba')
# plt.plot(recoils_df['Depth (um)'], recoils_df['Cu'] * 1000, label = 'Cu')
# plt.legend(loc='upper right')
# plt.title('10 MeV proton energy dissipation and recoil energy absorbed in 2 $\mu$m of YBCO')
# plt.xlabel('Depth (um)')
# plt.ylabel('Dissipated/Absorbed Energy (meV/Angstrom-ion)')
# plt.show()