import pandas as pd
import matplotlib.pyplot as plt


damage = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\SRIM\Planned fluence-based He irradiations\Test 3 - processed\Test 3 - damage.txt",
                        sep='\t', header = 0)

damage_df = pd.DataFrame(damage)
print(damage_df.head())


 
# implantation = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\SRIM\Planned fluence-based He irradiations\FC Raw test data\Test 10\RANGE.txt",
#                             sep='\t', header=0)
# implantation_df = pd.DataFrame(implantation)
# implantation_df["Depth (um)"] = implantation_df["DEPTH"] / 10000

# print(implantation_df.head())





########## Variables #############

fluences = ['1.5E+15',	'3.00E+15',	'7.50E+15',	'1.50E+16']

fluence_labels = ['1.5E+15 (ions/cm$^2$)',	'3.00E+15 (ions/cm$^2$)',	'7.50E+15 (ions/cm$^2$)',	'1.50E+16 (ions/cm$^2$)']

# convert dpa damage to mdpa
# for fluence in fluences:
#     damage_df[fluence] = damage_df[fluence]


############# Implantation Plot ###############
# plt.plot(implantation_df['Depth (um)'], implantation_df['He'], label = 'He implantation')

# plt.title('1 MeV He implantation into 3 $\mu$m of YBCO and 2 $\mu$m of Ni')
# plt.xlabel('Depth ($\mu$m)')
# plt.ylabel('He Implantation (atoms)')

# plt.axvline(x=3, linestyle='--', linewidth = 1, color = 'black') # vline of REBCO-Ni Interface penetration depth
# plt.show()

############# Damage Plot ###############
for fluence, label in zip(fluences, fluence_labels):
    plt.plot(damage_df["Depth (um)"], damage_df[fluence], label = fluence + " (ions/cm$^2$)")

# plt.plot(damage_df['Depth'], damage_df['2E+15'], label = '2E+15 (ions/cm$^2$)')
plt.axvline(x=3, linestyle='--', linewidth = 1, color = 'grey') 
# plt.axvline(x=2.5, linestyle='--', linewidth = 1, color = 'black') 

# Adding labels at specific points
# plt.text(0.5, 15, 'Silver layer', ha='center', va='bottom')
# plt.text(1.25, 15, 'REBCO', ha='center', va='bottom')
# plt.text(4, 60, 'Ni substrate', ha='center', va='bottom')

plt.title('2 MeV He$^+$ ion damage into 3 $\mu$m REBCO and 2 $\mu$m Ni')
# plt.xlim(0, 10)
# plt.ylim(0, 300)
plt.xlabel('Depth ($\mu$m)')
plt.ylabel('Damage (mdpa)')
plt.legend(loc='upper left')
plt.show()

############

# plt.plot(damage_df['Depth'], damage_df['Implantation'])
# plt.axvline(x=1, linestyle='--', linewidth = 1, color = 'black') 
# plt.axvline(x=2.5, linestyle='--', linewidth = 1, color = 'black') 

# # Adding labels at specific points
# plt.text(0.5, 25000, 'Ag', ha='center', va='bottom')
# plt.text(1.75, 25000, 'REBCO', ha='center', va='bottom')
# plt.text(4, 25000, 'Ni substrate', ha='center', va='bottom')

# plt.title('4 MeV He$^+$ ion implantation into SCS4050-AP tape.')
# plt.xlim(0, 10)
# plt.xlabel('Depth ($\mu$m)')
# plt.ylabel('Implantation (atoms)')
# plt.show()
