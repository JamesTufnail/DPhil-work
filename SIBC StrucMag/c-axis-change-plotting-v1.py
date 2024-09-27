import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks


data = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\SIBC StrucMag\XRD\Files for plotting\xrd-c-axis-change.txt",
                   sep='\t')

sample = data['Sample']

pristine, Ion1 = data['Pristine'], data['Ion1']
yerror_pristine, yerror_Ion1 = data[r'pristine error (95%)'], data[r'Ion1 error (95%)']
print(data)

colours = [
    ['#1f77b4', '#1f77b4', '#1f77b4'],  # Group 1: Shades of blue
    ['#ff7f0e', '#ff7f0e', '#ff7f0e'],  # Group 2: Shades of orange
    ['#2ca02c', '#2ca02c', '#2ca02c'],  # Group 3: Shades of green
]

colours = [colour for group in colours for colour in group]

for i in range(len(sample)):
    plt.errorbar(sample[i][-2:], pristine[i], yerr=yerror_pristine[i], fmt='o',
                 color=colours[i], capsize=3)
    plt.errorbar(sample[i][-2:], Ion1[i], yerr=yerror_Ion1[i], fmt='x', 
                 color=colours[i], capsize=3)

plt.text(0.95, 0.95, '\u2716 = 1.6 mdpa \n \u25CB = Pristine', 
         ha='right', va='top', transform=plt.gca().transAxes, bbox=dict(facecolor='white', edgecolor='black'))

plt.grid(True)
plt.xlabel('Sample')
plt.ylabel('C-axis Parameter (Å)')
plt.title(r'Change in c-axis parameter with 95% confidence intervals')

group_labels = ['Fujikura-2021Gd', 'SuNAM-2021Gd', 'SuperPower-2011Gd/Y']

# Add dummy lines for group labels in the legend
for i, label in enumerate(group_labels):
    plt.plot([], [], color=colours[:][3*i], label=label, linewidth=5)
plt.legend(loc='upper left')


plt.show()








# state = '0', '1.5'

# for i in range(len(sample)):
#     plt.errorbar(state[0], pristine[i], yerr=yerror_pristine[i], fmt='o',
#                  label=sample[i], color=colours[i], capsize=3)
#     plt.errorbar(state[1], Ion1[i], yerr=yerror_Ion1[i], fmt='x', 
#                 label=sample[i], color=colours[i], capsize=3)
    
# plt.show()