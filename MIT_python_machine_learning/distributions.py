import pandas as pd
import sklearn.linear_model as lm
import matplotlib.pyplot as plt

def count_data(data, low, high):
    count = 0
    for i in data:
        if low <= i <= high:
            count +=1
    return count




df = pd.read_csv(r"C:\Users\James\OneDrive\Documents\CVs and applications\Online Courses\AIMOOC\Modules\Module3\Data\distributions.csv")
#
# plt.scatter(df.index, df["Uniform"])
# print(df["Uniform"].mean())
# print(df["Uniform"].std())
#
# plt.figure()
# plt.scatter(df.index,df["Gaussian"])
# print(df["Gaussian"].mean())
# print(df["Gaussian"].std())
# plt.show()

height = df["Gaussian"]
plt.hist(height, bins=10)
plt.show()

mean = height.mean()
std = height.std()
print("Average Height is: ", mean)
print("Height std is:", std)

n_data = 200
count = count_data(height, mean-std, mean+std)
probability = (count/n_data) * 100
print(probability)



