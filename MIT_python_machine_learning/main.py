import pandas as pd

pd.set_option('display.max.columns', 500)
df = pd.read_csv(r"C:\Users\James\OneDrive\Documents\CVs and applications\Online Courses\AIMOOC\Modules\Module1\Data\temperature_boston_monthly_5years.csv")

####### Selecting data by column ##########
# print(df)
#
# print(df.loc[28])
#
# print(df.loc["Month"])
#
# columns = ["Month", "Year", "AvgTemperature"]
# print(df[columns])

############ Sorting data and resetting index #########
df_sorted = df.sort_values("AvgTemperature", ascending = False)
# print(df_sorted)
reset = df_sorted.reset_index(drop = True)
# print(reset)

######### Finding mean and filtering

mean_temp = df["AvgTemperature"].mean()
max_temp = df["AvgTemperature"].max()
min_temp = df["AvgTemperature"].min()
data_points = df["AvgTemperature"].count()

condition = df["AvgTemperature"] > 75
hot_days = df.loc[condition]
# print(hot_days)

##### Grouping data
# print(df)

# below will find maximum of each column grouped by rows, hence 12 is always highest month
allmeantemps = df.groupby("Year").mean()
print(allmeantemps)
allmaxtemps = df.groupby("Year").max()

temp2015 = allmaxtemps.loc[2015]["AvgTemperature"]

condition = (df["AvgTemperature"] > temp2015)
temp2015sametemp = df.loc[condition]
# print(temp2015sametemp)

####### Finding correlations

# print(df.corr())
