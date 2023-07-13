import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\James\OneDrive\Documents\CVs and applications\Online Courses\AIMOOC\Modules\Module1\Data\city_temperature.csv",
                 low_memory=False)

print(df.head())
paris_df = df.loc[(df["City"] == 'Paris')]


#### Can' figure out how to get mean() to work for df (there's non-numeric values)
# non_numeric_columns = ["Region", "City"]
# numeric_df = df[pd.to_numeric(df[non_numeric_columns], errors='coerce').notna()]
# paris_mean = paris_df.groupby("AvgTemperature").mean()

paris_max = paris_df.groupby("Year").max()
# print(paris_max)

paristemp1998 = paris_max.loc[1998]["AvgTemperature"]
# print(paristemp1998)

hightemp = df.loc[(df["AvgTemperature"] > 80)]
cities = hightemp.groupby("City").count()
# print(cities.loc["Milan"]["AvgTemperature"])

plt.plot(df["Year"], color = 'green')
plt.show()




