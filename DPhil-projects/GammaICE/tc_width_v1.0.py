import matplotlib.pyplot as plt
import pandas as pd

# Load the data
data = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\tc_transition_vals.txt", sep="\t")

print(data.head())


      
# Plot the data
fig = plt.figure(figsize=(8, 4))
plt.scatter(data['Sample'], data['Pristine (jc0)'], label='Pristine')
plt.scatter(data['Sample'], data['Ion (jc/jc0)'], label = 'Ion Irradiated', marker='x')
plt.scatter(data['Sample'], data['Gamma (jc/jc0)'], label = 'Post Gamma', marker='^')

plt.xlabel('Sample and Damage (mdpa)')
plt.ylabel(r'Normalised Change in $\Delta$ Tc $\left( \frac{\Delta Tc}{\Delta Tc_0} \right)$')
plt.legend()
plt.axhline(y=1, color='grey', linestyle='--')

plt.title(r'$\Delta$ Tc Change following Ion and Gamma Irradiations')
plt.show()
