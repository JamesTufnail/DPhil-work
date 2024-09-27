import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\SRIM\Planned fluence-based He irradiations\NRT_Vacancy_comparison.txt",
                    delimiter='\t')

data_df = pd.DataFrame(data)
print(data_df)

plt.plot(data_df['Depth (um)'], data_df['FC 2 MeV He - NRT'], label='FC 2 MeV He - NRT')
plt.plot(data_df['Depth (um)'], data_df['QS 2 MeV He - NRT'], label='QS 2 MeV He - NRT', linestyle='--')
plt.plot(data_df['Depth (um)'], data_df['FC 2 MeV He - vacancy.txt'], label='FC 2 MeV He - Vacancy')
plt.plot(data_df['Depth (um)'], data_df['QS 2 MeV He - vacancy.txt'], label='QS 2 MeV He - Vacancy', linestyle='--')

plt.xlabel('Depth (um)')
plt.ylabel('Vacancy Concentration')
plt.title('NRT vs vacancy.txt method for Quick SRIM and Full Cascade SRIM')
plt.legend()
plt.show()

# fig, axs = plt.subplots(1, 2, figsize=(12, 6))


# axs[0].plot(data_df['Depth (um)'], data_df['QS 2 MeV'], label='QS 2 MeV', linestyle='--')
# axs[0].plot(data_df['Depth (um)'], data_df['FC 2 MeV'], label='FC 2 MeV')
# axs[0].set_title('2 MeV He')

# # Plot on the second subplot (axs[1])
# axs[1].plot(data_df['Depth (um)'], data_df['QS 1 MeV'], label='QS 1 MeV', linestyle='--')
# axs[1].plot(data_df['Depth (um)'], data_df['FC 1 MeV'], label='FC 1 MeV')
# axs[1].set_title('1 MeV He')

# # Set common labels and title
# for ax in axs:
#     ax.set_xlabel('Depth (um)')
#     ax.set_ylabel('Vacancy Concentration')

# # Set a common title
# plt.suptitle('Vacancy Concentration from vacancy.txt method for Quick SRIM and Full Cascade SRIM')

# # Add a legend to both subplots
# for ax in axs:
#     ax.legend()
# plt.show()


