import os
import numpy as np
import matplotlib.pyplot as plt
from srim import TRIM, Ion, Layer, Target
from srim.output import Results
import yaml
import pandas as pd


def plot_damage_energy(folder, ax):
    results = Results(folder)
    phon = results.phonons
    dx = max(phon.depth) / 100.0 # to units of Angstroms
    energy_damage = (phon.ions + phon.recoils) * dx
    ax.plot(phon.depth, energy_damage / phon.num_ions, label='{}'.format(folder))
    return sum(energy_damage)

def plot_ionization(folder, ax):
    results = Results(folder)
    ioniz = results.ioniz
    dx = max(ioniz.depth) / 100.0 # to units of Angstroms
    ax.plot(ioniz.depth, ioniz.ions, label='Ionization from Ions')
    ax.plot(ioniz.depth, ioniz.recoils, label='Ionization from Recoils')

def plot_vacancies(folder, ax):
    results = Results(folder)
    vac = results.vacancy
    vacancy_depth = vac.knock_ons + np.sum(vac.vacancies, axis=1)
    ax.plot(vac.depth, vacancy_depth, label="Total vacancies at depth")
    return sum(vacancy_depth)


def plot_damage(source_folder, sample_name, rebco_thickness):
    """
    Script to plot avg damage for multiple levels of fluences (exported in usual way from excel)

    Inputs:
    s
    """
    avg_dpa_file = os.path.join(source_folder, 'processed_srim.txt')
    avg_dpa = pd.read_csv(avg_dpa_file, sep='\t', header=0)

    depth_um = avg_dpa['Depth (um)'] # extracting depth in um
    fluences = avg_dpa.columns[1:].tolist() # extracting list of flunces (column headers) in ions/cm2

    for fluence in fluences:
        plt.step(depth_um, avg_dpa[fluence], where='post', label = fluence + ' ions/cm$^2$')

    """Just REBCO"""
    plt.title('SRIM Damage Profile for {}'.format(sample_name))
    plt.xlim(0, 2)
    plt.ylim(0,35)

    """ REBCO + Ni"""
    # plt.title('SRIM Damage Profile for {} + Ni'.format(sample_name))


    plt.axvline(x=rebco_thickness, linestyle='--', linewidth=1, color='grey')
    plt.legend()

    plt.xlabel('Depth ($\mu m$)')
    plt.ylabel('Damage (mdpa)')
    plt.show()

    return 



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

source_folder = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\SRIM\GdBCO 2 MeV He"
sample_name = 'He$^+$ into GdBCO'
rebco_thickness = 2

image_directory = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\SRIM\GdBCO 2 MeV He"
os.makedirs(image_directory, exist_ok=True)
save = False

# ~~~~~~~~~~~~~~~~~~~~ Plotting Implantation as appm(x) ~~~~~~~~~~~~~~~~~~~~~~~ # 
ion_imp_file = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\SRIM\variable_E_into_GdBCO.txt"

ion_implantation = pd.read_csv(ion_imp_file, sep='\t', header=0)
depth= ion_implantation['Depth (um)']

energies = ion_implantation.columns[1:].tolist() # extracting energies from colum headers

plt.figure(figsize=(10,3))

for energy in energies:
    plt.step(depth, ion_implantation[energy], where='post', label = energy)

plt.axvline(x=rebco_thickness, linestyle='--', linewidth=1, color='grey')
plt.yscale('log')
plt.legend()
plt.xlim(0,4.5)
plt.xlabel('Depth ($\mu m$)')
plt.ylabel('Ion Implantation (appm)')
# plt.title('SRIM Implantation of {} at 1x10$^16$ ions/cm$^2$'.format(sample_name))
plt.title('SRIM Implantation at 1x10$^{16}$ ions/cm$^2$')
plt.tight_layout()
plt.show()



"""
# ~~~~~~~~~~~~~~~~~~~~~ Plot ionisation vs depth ~~~~~~~~~~~~~~~~~~~~~ #
fig, axes = plt.subplots(1, len(folders), sharey=True, sharex=True)

for ax, folder in zip(np.ravel(axes), folders):
    plot_damage_energy(folder, ax)
    plot_ionization(folder, ax)
    ax.legend()
    ax.set_ylabel('eV')
    ax.set_xlabel('Depth [Angstroms]')
fig.suptitle('Ionization Energy vs Depth', fontsize=15)
fig.set_size_inches((20, 6))
if save:
    fig.savefig(os.path.join(image_directory, 'ionizationvsdepth.png'), transparent=True)
else:
    plt.show()


# ~~~~~~~~~~~~~~~~~~~~~~ Plot vacancies vs depth (from vac folder) ~~~~~~~~~~~~~~~~~~~~ #
fig, ax = plt.subplots()

for i, folder in enumerate(folders):
    total_vacancies = plot_vacancies(folder, ax)
    print("Total number of vacancies {}: {}".format(folder, total_vacancies))

ax.set_xlabel('Depth [Angstroms]')
ax.set_ylabel('Number of Vacancies')
ax.set_title('Vacancies vs. Depth')
ax.legend()
fig.set_size_inches((15, 6))
if save:
    fig.savefig(os.path.join(image_directory, 'vacanciesvsdepth.png'), transparent=True)
else:
    plt.show()


# ~~~~~~~~~~~~~~~~~ Plot damage energy vs depth ~~~~~~~~~~~~~~~~~ #
fig, axes = plt.subplots(1, len(folders), sharex=True, sharey=True)

for ax, folder in zip(np.ravel(axes), folders):
    energy_damage = plot_damage_energy(folder, ax)
    print("Damage energy: {} eV".format(energy_damage))
    ax.set_xlabel('Depth [Angstroms]')
    ax.set_ylabel('eV')
    ax.legend()

fig.suptitle('Damage Energy vs. Depth', fontsize=15)
fig.set_size_inches((20, 6))
if save:
    fig.savefig(os.path.join(image_directory, 'damagevsdepth.png'), transparent=True)
else:
    plt.show()

    """