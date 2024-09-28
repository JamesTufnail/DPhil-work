import pandas as pd
import matplotlib.pyplot as plt

# def XAS_diff_plot(data, edge_start, offset):
#
#




fu21 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\FU21Y_10deg.nor",
                   skiprows=8,
                   delim_whitespace=' ')
fu21 = pd.DataFrame(fu21.values, columns= ["energy", "Fu21_10deg"])


sp11 = pd.read_csv(r"C:\Users\James\OneDrive - Nexus365\DPhil-general\XAS\Susie data\SP11_10deg.nor",
                   skiprows=8,
                   delim_whitespace=' ')
sp11 = pd.DataFrame(sp11.values, columns= ["energy", "SP11_10deg"])

shifts = [-0.3, -0.2, -0.1, 0, 0.1, 0.2]
# 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
sp11["energy"] = sp11["energy"] - 8979.3
fu21["energy"] = fu21["energy"] - 8979.3

# for shift in shifts:
#     sp11["energy"] = sp11["energy"] - shift
#
#     plt.title("10 Degrees XANES Spectra of Fu21 and SP11 ")
#     plt.plot(fu21["energy"], fu21["Fu21_10deg"], label = 'Fu21')
#     plt.plot(sp11["energy"], sp11["SP11_10deg"], label = 'SP11 with {} eV shift'.format(shift))
#     plt.xlim(0, 30)
#     plt.legend()
#     plt.show()

## TODO: Find differece plots between SP11 and FU21 and just plot with shifted energies (NOTE THIS MAY NOT BE PHYSICAL!)

sp11["diff"] = sp11["SP11_10deg"] - fu21["Fu21_10deg"]
print(sp11.head())

for shift in shifts:
    sp11["energy"] = sp11["energy"] - shift
    plt.plot(sp11["energy"], sp11["diff"], label = "Offset of {} eV".format(shift))

# title= ("Diff plot with different eV offset")
plt.axhline(y=0, color="black", linewidth=0.5, linestyle='--')
plt.xlim(0, 30)
plt.legend()
plt.title("XANES Diff plot with different eV offset (Fu21 reference)")
plt.show()
