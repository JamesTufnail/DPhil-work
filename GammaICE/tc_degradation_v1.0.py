import matplotlib.pyplot as plt
import pandas as pd

# Load the data
data = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\Experiments\Gamma Experiments\Data\tc_90_vals.txt", sep="\t")

print(data.head())


      
# Plot the data
fig = plt.figure(figsize=(8, 4))
plt.scatter(data['Sample'], 100*data['Pristine (jc0)'], label='Pristine')
plt.scatter(data['Sample'], 100*data['Ion (jc/jc0)'], label = 'Ion Irradiated', marker='x')
plt.scatter(data['Sample'], 100*data['Gamma (jc/jc0)'], label = 'Post Gamma', marker='^')

plt.xlabel('Sample and Damage (mdpa)')
plt.ylabel(r'Percentage Change in Tc $\left( \frac{Tc}{Tc_0} \right)$')
plt.legend()
plt.axhline(y=100, color='grey', linestyle='--')

plt.title('Critical Temperature following Ion and Gamma Irradiations')
plt.show()
