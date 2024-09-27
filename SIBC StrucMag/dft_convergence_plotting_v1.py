"""
Author: James Tufnail
Date: 21/08/2024

Just a quick script to plot convergence data for DFT calculations.


"""


import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Vals

e_cut_off = [500, 600, 900, 1000, 1100, 1200, 1300, 1400]
cu_pc_change = [0.010733652, 0, 0.005438327, 0.001082867, 0.000879448, 0.000741842, 0.000622186, 0.000538427]
o_pc_change = [1.92253, 0, 0.072254017, 0.000718594, 0.000649049, 0.000533144, 0.000440422, 0.00032452]

# k_spacing = [0.08, 0.05, 0.04]
# k_pc_change = [0.303, 0.136, 0.051]



# Plotting
fig, ax = plt.subplots(figsize=(3,6))

ax.plot(e_cut_off, cu_pc_change, marker='o', linestyle='-', label='Cu')
ax.plot(e_cut_off, o_pc_change, marker='o', linestyle='-', label='O')


ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
ax.set_xlabel('Energy Cut-off (eV)', fontsize='large')
ax.set_ylabel('Percentage Change (%)', fontsize='large')
ax.set_title('Total Energy Convergence', fontsize='large')
# ax.grid(True)

# ax2 = ax.twiny()
# ax2.plot(k_spacing, k_pc_change, marker='o', linestyle='-', label='O1-Cu1')


inset_ax = inset_axes(ax, width="60%", height="60%", loc='upper right', borderpad = 1)  # Relative size and position
inset_ax.plot(e_cut_off[-5:], cu_pc_change[-5:], marker='o', linestyle='-')
inset_ax.plot(e_cut_off[-5:], o_pc_change[-5:], marker='o', linestyle='-')
inset_ax.legend(['Cu', 'O'], fontsize='large')
inset_ax.grid(True)
# inset_ax.set_xlabel('Energy Cut-off (eV)', fontsize='medium')
# inset_ax.set_ylabel('Percentage Change (%)', fontsize='medium')

# inset_ax.set_ylim(0, 0.001)
# inset_ax.set_title('Close up above 1000 eV', fontsize='medium')
# inset_ax.set_xticks([])
# inset_ax.set_yticks([])

plt.show()
