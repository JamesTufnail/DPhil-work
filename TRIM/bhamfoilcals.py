import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.integrate import odeint
import radioactivedecay as rd

####################################### Import data ########################### ###
flux = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Birmingham Neutron Irradiation\bhamfoildata1.xls", sheet_name = 'flux')
flux = flux.rename(columns={'Flux Energy (MeV)': 'Energy (MeV)', 'True flux': 'Flux'})
flux = flux.dropna()

sc_data = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Birmingham Neutron Irradiation\bhamfoildata1.xls", sheet_name = 'scandium foil')
co_data = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Birmingham Neutron Irradiation\bhamfoildata1.xls", sheet_name = 'cobalt foil')
# sn_data = pd.read_excel(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Birmingham Neutron Irradiation\bhamfoildata1.xls", sheet_name = 'tin foil')

sc_cross_sec = sc_data[['Cross-sec Energy (MeV)','cross-sec (barns)']]
sc_cross_sec = sc_cross_sec.rename(columns={'Cross-sec Energy (MeV)': 'Energy (MeV)', 'cross-sec (barns)': 'cross-sec (barns)'})
sc_cross_sec = sc_cross_sec.dropna()

# flux = sc_data[['Flux Energy (MeV)', 'Flux']]
# flux = flux.rename(columns={'Flux Energy (MeV)': 'Energy (MeV)', 'True flux': 'Flux'})
# flux = flux.dropna()

co_cross_sec = co_data[['Cross-sec Energy (MeV)','cross-sec (barns)']]
co_cross_sec = co_cross_sec.rename(columns={'Cross-sec Energy (MeV)': 'Energy (MeV)', 'cross-sec (barns)': 'cross-sec (barns)'})
co_cross_sec = co_cross_sec.dropna()

# flux = co_data[['Flux Energy (MeV)', 'Flux']]
# flux = flux.rename(columns={'Flux Energy (MeV)': 'Energy (MeV)', 'True flux': 'Flux'})
# co_cross_sec = co_cross_sec.dropna()


####################################### Functions ########################################
def n_increasing(N, t, decay_prob, RR):
    """ Function to calculate the rate of exponential increaes of atoms in the foil.
    Parameters
    ----------
    N : float
        Number of 46Sc atoms at time t.
    t : float
        Time in days."""
    dNdt = RR - (decay_prob * N) # ground state reaction rate - decay rate
    return dNdt

def n_decreasing(N, t, decay_prob):
    """ Function to calculate the rate of exponential decay of atoms in the foil.
    Parameters
    ----------
    N : float
        Number of atoms at time t.
    t : float
        Time in days."""
    dNdt = - decay_prob * N 
    return dNdt


def calculated_gamma_spec_counts(activity, time, efficiency):
    """Function to calculate the number of counts in a gamma spectrum.
    Parameters
    ----------
    activity : float
        Activity of the gamma source in Bq. 
    time : float
        Time of the gamma spectrum in seconds.
    efficiency : float
        Efficiency of the detector.
    """
    spectrometry = activity * time * efficiency
    return spectrometry

def discretise_interval_and_integrate_for_RR(flux, cross_sec, n0):
    """Function to discretise the energy values into the same region and integrate the product of flux and cross section to calculate the reaction rate.
    Parameters
    ----------
    flux : Pandas dataframe of flux data.
    cross_sec : Pandas dataframe of cross section data.
    """
    # Set upper and lower bounds of discretisation
    flux_E_pts, xs_E_pts = flux['Energy (MeV)'], cross_sec['Energy (MeV)']
    lower_bound_E, upper_bound_E = min(flux_E_pts), max(flux_E_pts)

    # Sort all values into one list
    unsorted_energies = list(flux_E_pts)
    for energy in xs_E_pts:
        if (lower_bound_E<=energy<=upper_bound_E) and (energy not in unsorted_energies):
            unsorted_energies.append(energy)
    final_energies = np.array(sorted(unsorted_energies))
    
    # Interpolate flux and cross section values
    cross_sec_interpolated = interp1d(cross_sec['Energy (MeV)'], cross_sec['cross-sec (barns)'], kind='linear')(final_energies)
    flux_interpolated = interp1d(flux['Energy (MeV)'], flux['Flux'], kind='linear')(final_energies)

    # Calculate reaction rate
    product_curve = (cross_sec_interpolated * barns) * (flux_interpolated * meV_to_eV) 
    integral_trapz = np.trapz(product_curve, final_energies)
    RR = n0 * integral_trapz
    return RR, final_energies, flux_interpolated, cross_sec_interpolated


####### Plotting functions ##########
def plot_decays(N1, N2, xlabel, ylabel):
    """Function to plot the decay of a nuclide.
    Parameters
    ----------
    N1 : Array of number of atoms at time t1.
    N2 : Array of number of atoms at time t2.
    xlabel : Label for x-axis.
    ylabel : Label for y-axis.
""" 
    plt.plot(t1, N1, label='Beam on')
    plt.plot(t2, N2, label='Beam off')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title('Decay of {} in the HFADNF'.format(ylabel))
    plt.legend()
    plt.grid(True)
    plt.plot()
    plt.show()

def loglog_cross_sec(x, y, title):
    """Function to plot cross section against energy in log-log scale.
    Parameters
    ----------
    x : Array of energy values.
    y : Array of cross section values.
    title : Title of the plot.
    """
    plt.loglog(x, y, marker='x', linestyle='-')
    plt.xlabel('Energy (MeV)')
    plt.ylabel('Cross Section (barns)')
    plt.title(title)
    plt.xlim(1e-7,1)
    plt.grid(True)
    plt.show()

def loglog_birmingham_spectra(x, y, title):
    """Function to plot neutron spectra from Birmingham.
    Parameters
    ----------
    x : Array of energy values.
    y : Array of flux values.
    title : Title of the plot.
    """
    plt.loglog(x, y)
    plt.xlabel('Energy (MeV)')
    plt.ylabel('Flux (n/cm2/s)')
    plt.title(title)
    plt.grid(True)
    plt.show()

def check_cross_sec_interp(x, y, cross_sec, name):
    """Function to check interpolation by plotting cross section against energy in log-log scale.
    Parameters
    ----------
    x : Array of energy values.
    y : Array of cross section values.
    """
    plt.figure(figsize=(10, 6))
    plt.loglog(x, y, label='Interpolated Cross Section')
    plt.loglog(cross_sec['Energy (MeV)'], cross_sec['cross-sec (barns)'], label = 'real cross sec')
    plt.legend()
    plt.title('Interpolated {} Cross Section Comparison'.format(name))
    plt.grid(True)
    plt.show()

def check_flux_interp(x, y, flux, name):
    """Function to check interpolation by plotting cross section against energy in log-log scale.
    Parameters
    ----------
    x : Array of energy values.
    y : Array of cross section values.
    """
    plt.figure(figsize=(10, 6))
    plt.semilogx(x, y, label='Interpolated Flux')
    plt.semilogx(flux['Energy (MeV)'], flux['Flux'], label='Real ')
    plt.legend()
    plt.title('Interpolated Flux {} Comparison'.format(name))
    plt.grid(True)
    plt.show()

######################################### Parameter setup ################################
barns = 1e-24
meV_to_eV = 1e6 # 1 meV = 1e6 eV
N_A = 6.02214076e23 # Avogadro's constant

t1 = np.linspace(0,180,100) #start, stop, number - the start and stop in reality will be based on Birmingham data for when beam on.
t2 = np.linspace(180, 270, 100) # cool-down time

Sc46_decay_prob_s = 9.5745785501e-8 # Decay probability of 46Sc in second
Sc46_decay_prob_d = Sc46_decay_prob_s * 86400 # Decay probability of 46Sc in day

n0_60co = 1.5e18 # Number of 60Co atoms calculated in foil
Co60_decay_prob_s = 4.166945489506e-9 # Decay probability of 60Co in second
Co60_decay_prob_d = Co60_decay_prob_s * 86400 # Decay probability of 60Co in day

#### Foil properties and dimensions ####
sc_thickness = 0.0125e-3 # thickness of foil in m
sc_density = 2985 # density of scandium in kg/m3
sc_molar_mass = 44.955912 # molar mass of scandium in g/mol

co_thickness = 0.01e-3 #0.5mm thickness
co_density = 8860 # density of cobalt in kg/m3
co_molar_mass = 58.933195

# sn_thickness = 0.5e-3  // TODO: check for different abundances and densities of each sn isotope
# sn_density = 7310
# sn_molar_mass = 118.710

radius = 1.5e-3 # radius of foil in m


#### Calculating number of atoms in sample
def n0_atoms_in_sample(thickness, density, molar_mass):
    volume = np.pi * radius**2 * thickness # volume of foil in m3
    mass = volume * density * 1000 # mass of foil in g
    n0_atoms = (mass / molar_mass) * N_A # number of atoms in foil
    return n0_atoms

n0_45sc = n0_atoms_in_sample(sc_thickness, sc_density, sc_molar_mass)
n0_59co = n0_atoms_in_sample(co_thickness, co_density, co_molar_mass)
# n0_120sn = n0_atoms_in_sample(sn_thickness, sn_density, sn_molar_mass)
# n0_117sn = 
# n0_112sn =



######################################### Plotting cross section and flux ##########################

# Plot cross section
loglog_cross_sec(sc_cross_sec['Energy (MeV)'], sc_cross_sec['cross-sec (barns)'], 'Log-Log Plot of Sc45 Cross Section vs. Energy')
loglog_cross_sec(co_cross_sec['Energy (MeV)'], co_cross_sec['cross-sec (barns)'], 'Log-Log Plot of Co59 Cross Section vs. Energy')

# # Plot Birmingham flux
loglog_birmingham_spectra(flux['Energy (MeV)'], flux['Flux'], 'Birmingham Neutron Spectra')



############################# Discretising energy values into the same region ###########################

sc_RR, sc_final_energies, sc_interp_flux, sc_interp_cross_sec = discretise_interval_and_integrate_for_RR(flux, sc_cross_sec, n0_45sc)
# print("Scandium reaction rate:", sc_RR, "(transmutations / second)")

co_RR, co_final_energies, co_interp_flux, co_interp_cross_sec = discretise_interval_and_integrate_for_RR(flux, co_cross_sec, n0_59co)
# print("Cobalt reaction rate:", co_RR, "(transmutations / second)")

####################### Printing interpolated flux and cross section to check fit #####################################

# Check interpolation of flux and cross section
check_flux_interp(sc_final_energies, sc_interp_flux, flux, 'Sc45')
check_cross_sec_interp(sc_final_energies, sc_interp_cross_sec, sc_cross_sec, 'Sc45')

check_flux_interp(co_final_energies, co_interp_flux, flux, 'Co59')
check_cross_sec_interp(co_final_energies, co_interp_cross_sec, co_cross_sec, 'Co59')



#################################### Calculating decays for 46Sc ########################################
N46Sc_0 = 1

# First increasing case of 46Sc production
N46Sc_1 = odeint(n_increasing, N46Sc_0, t1, args=(Sc46_decay_prob_d, sc_RR,))
# First decreasing decay of 46Sc, result1[-1] is the last value of result1, which is the value of N46Sc at the end of the first odeint
N46Sc_2 = odeint(n_decreasing, N46Sc_1[-1], t2, args=(Sc46_decay_prob_d,)) 

# activity (Bq) at the end of the cool down
sc_end_of_cool_down_activity = N46Sc_2[-1] * Sc46_decay_prob_s 

# activity (Bq) of 1120 keV gamma at the end of the cool down
Sc46_1120_gamma = 0.999964 * 0.999870 * sc_end_of_cool_down_activity 

# counts in 1120 keV gamma spectrum after 10 minutes
Sc46_1120_gamma_counts = calculated_gamma_spec_counts(Sc46_1120_gamma, 3600, 1e-5)

print("Number of 46Sc atoms at the end of the cool down:", N46Sc_2[-1])
print("Activity of 1120 keV gamma at the end of the cool down:", Sc46_1120_gamma, "Bq")
print("Counts in 1120 keV gamma spectrum after 60 minutes:", Sc46_1120_gamma_counts)

# Plotting decay curve for scandium
plot_decays(N46Sc_1, N46Sc_2, 'Time (days)', 'N46Sc')

# using radiaoctivedecay module to set inventory of 46Sc using number of atoms
# Sc46_t0 = rd.Inventory({'Sc-46': N46Sc_1[-1]}, 'num') 
# Sc46_t1 = Sc46_t0.decay(20.0, 'h')
# print(Sc46_t1.cumulative_decays(20, 'h'))

#################################### Calculating decays for 60Co ########################################
# N60Co_0 = 1

# # First increasing case of 60Co production
# N60Co_1 = odeint(n_increasing, N60Co_0, t1, args=(Co60_decay_prob_d,))
# # First decreasing decay of 60Co
# N60Co_2 = odeint(n_decreasing, N60Co_1[-1], t2, args=(Co60_decay_prob_d,))

# # activity (Bq) at the end of the cool down
# co_end_of_cool_down_activity = N60Co_2[-1] * Co60_decay_prob_s
# # activity (Bq) of 1173 keV gamma at the end of the cool down
# Co60_1173_gamma = 0.9988 * 0.9985 * co_end_of_cool_down_activity
# # counts in 1173 keV gamma spectrum after 10 minutes
# Co60_1173_gamma_counts = calculated_gamma_spec_counts(Co60_1173_gamma, 3600, 1e-5) ## TODO: check if 1e-5 is the correct efficiency


# print("Number of 60Co atoms at the end of the cool down:", N60Co_2[-1])
# print("Activity of 1173 keV gamma at the end of the cool down:", Co60_1173_gamma, "Bq")
# print("Counts in 1173 keV gamma spectrum after 60 minutes:", Co60_1173_gamma_counts)

# Plotting decay curve for cobalt
# plot_decays(N60Co_1, N60Co_2, 'Time (days)', 'N60Co')











