import pandas as pd
import matplotlib.pyplot as plt

"""
Script to plot each individual YBCO peak (Cu, in-phase O, out of phase O, O4)
"""

peaks = ['Cu', 'Out-of-phase', 'In-phase', 'O4']
x_lims = [
    [120, 180],
    [300, 390],
    [420, 480],
    [400, 600],
]

y_lims = [
    [0, 1.5],
    [0, 0.8],
    [0, 1],
    [0, 2],
]

colours = ['#1f77b4', '#ff7f0e', '#2ca02c']

cascade_shifts = [
    0.4,
    0.2,
    0.3,
    0.5,
]

# Create a 2x2 grid of subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Flatten the axs array to make it easier to iterate through
axs = axs.flatten()

raw_data = pd.read_excel(r"C:\Users\James\Desktop\810YBCO-cumulative-fits-raw.xlsx")


for i, (peak, shift, limits, ylim) in enumerate(zip(peaks, cascade_shifts, x_lims, y_lims)):
    # Reading and setting title
    df = pd.read_excel(r"C:\Users\James\Desktop\810YBCO-cumulative-fits.xlsx", sheet_name=peak)
    title = '{} Peak'.format(peak)
    print(df.head())

    wavenumbers = [
        df["s64 p w"],
        df["s10 300kev w"],
        df['s32 ann w'],
    ]

    counts = [
        df["s64 p c"],
        df["s10 300kev c"],
        df['s32 ann c'],
    ]

    labels = [
        'Pri',
        'Irr.',
        'Ann.',
    ]


    raw_cascade = 0
    cascade = 0
    for wvnmbrs, cnts, label, color in zip(wavenumbers, counts, labels, colours):
        axs[i].plot(wvnmbrs, cnts + cascade, label=label, color = color)
        axs[i].scatter(raw_data['w p'], raw_data['c p'], s=2.5, marker='o', color = '#1f77b4')
        axs[i].scatter(raw_data['w irr'], raw_data['c irr'] + shift, s=2.5, marker='o', color = '#ff7f0e')
        axs[i].scatter(raw_data['w ann'], raw_data['c ann'] +2*shift, s=2.5, marker='o', color = '#2ca02c')
        cascade += shift

    # Set the title for each subplot
    axs[i].set_title(title)

    # Set specific x-axis limits for each subplot
    axs[i].set_xlim(limits[0], limits[1])
    axs[i].set_ylim(ylim[0], ylim[1])

    # Turning on grid
    axs[i].grid(True)

# Add an overall title to the plot
fig.suptitle('Peak Shifts in 810YBCO Thin Film', fontsize=16)

# Set common x-axis and y-axis labels for the entire figure
fig.text(0.5, 0.06, 'Wavenumber (cm$^{-1}$)', ha='center', va='center', fontsize=12)
fig.text(0.06, 0.5, 'Intensity (arb. units)', ha='center', va='center', rotation='vertical', fontsize=12)

# Set common legend for all subplots
handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right')

# Adjust spacing between subplots
# plt.tight_layout()

# Show the plot
plt.show()