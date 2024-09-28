import matplotlib.pyplot as plt
import pandas as pd

# Load data from Excel file
file = r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Techniques\SRIM\Gamma Irradiation Experiments\processed_SRIM_for_plotting.xlsx"
data_sheet1 = pd.read_excel(file, header=0, sheet_name='New_test_1')
data_sheet3 = pd.read_excel(file, header=0, sheet_name='New_test_3')

sample_name = '4 MeV He$^{2+}$ Ions into SCS4050 Tape'

# Create figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Plot for sheet_name 1 (Full Tape)
for col in data_sheet1.columns[1:]:
    depth = data_sheet1['Depth (um)']
    dpa = data_sheet1[col]
    ax1.plot(depth, dpa, label=f'{col:.1e} ions/cm$^2$')

ax1.set_xlabel('Depth ($\mu$m)')
ax1.axvline(x=2, color='grey', linestyle='--')
ax1.axvline(x=4.9, color='grey', linestyle='--')
# ax1.text(.8, 15, 'Silver', fontsize=11, ha='center', va='center')
# ax1.text(3.5, 15, 'REBCO', fontsize=11, ha='center', va='center')
ax1.set_ylabel('Damage (mdpa)')
ax1.set_title('Full Tape')

# Create the legend for subplot 1
legend1 = ax1.legend(loc='upper left', title='Irradiation Dose', facecolor='white')
legend1.get_frame().set_alpha(1)  # Set legend frame alpha to fully opaque

# Plot for sheet_name 3 (Silver and REBCO Layer)
for col in data_sheet3.columns[1:]:
    depth = data_sheet3['Depth (um)']
    dpa = data_sheet3[col]
    ax2.plot(depth, dpa, label=f'{col:.1e} ions/cm$^2$')

ax2.set_xlabel('Depth ($\mu$m)')
ax2.axvline(x=2, color='grey', linestyle='--')
ax2.axvline(x=4.9, color='grey', linestyle='--')
# ax2.text(.8, 18, 'Silver', fontsize=11, ha='center', va='center')
# ax2.text(3.5, 18, 'REBCO', fontsize=11, ha='center', va='center')
ax2.set_ylabel('Damage (mdpa)')
ax2.set_title('Silver and REBCO Layer')

# Adjust layout and display the plot
fig.suptitle(sample_name, fontsize=14)  # Overall title above subplots
plt.tight_layout()  # Increase padding if necessary
plt.show()
