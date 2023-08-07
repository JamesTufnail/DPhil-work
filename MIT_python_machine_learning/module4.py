import pandas as pd
import matplotlib.pyplot as plt
import sklearn.linear_model as lm
import sklearn.svm as svm

def single_linear_regression(x, y):
    """ JT - Plots linear regression for x and y values.

    :param x: x values
    :param y: y values
    :return: Coefficients, intercept, R^2 value (close to 1 is best)
    """
    lin_reg = lm.LinearRegression()
    lin_reg.fit(x, y)
    ypred = lin_reg.predict(x)

    plt.scatter(x, y)
    plt.plot(x, ypred, color='orange')
    plt.show()

    print("Coefficient:", lin_reg.coef_)
    print("Intercept:", lin_reg.intercept_)
    print("R$^2$ value:", lin_reg.score(x, y))

# df = pd.read_csv(r"C:\Users\James\OneDrive\Documents\CVs and applications\Online Courses\AIMOOC\Modules\Module4\Data\temperatures.csv")
#
# print(df.head())
#
# plt.hist(df["Y1961"], bins=20, color="blue")
# plt.hist(df["Y1990"], bins=20, color="orange")
# plt.hist(df["Y2019"], bins=20, color="green")
# # plt.show()
#
# world = df.loc[(df["Area"] == "World")]
# print(world)
#
# world = world.drop('Area', axis=1)
# world = world.drop('Months', axis=1)
#
# world_avg = world.mean()
# plt.figure(figsize=(15,5))
# plt.plot(world_avg)
# plt.show()

# df = pd.read_csv(r"C:\Users\James\OneDrive\Documents\CVs and applications\Online Courses\AIMOOC\Modules\Module4\Data\students.csv")
#
# print(df.head())
# x = df[["math score"]]
# y = df["reading score"]
#
# plt.scatter(x,y)
#
# lin_reg = lm.LinearRegression()
# lin_reg.fit(x,y)
# ypred = lin_reg.predict(x)
#
# plt.plot(x, ypred, color = "orange")
# plt.show()
# r2 = ypred.score(x,y)
# print(r2)


# df = pd.read_csv(r"C:\Users\James\OneDrive\Documents\CVs and applications\Online Courses\AIMOOC\Modules\Module4\Data\menu.csv")
#
# x=df[["Sugars", "Sodium"]]
# y=df["Label"]
# #
# clf = svm.SVC(kernel='linear')
# clf.fit(x, y)
# # score = clf.score(x, y)
# # print("R^2 value:", score)
#
# def draw_svc_line():
#     w = clf.coef_[0]
#     slope = -w[0]/w[1]
#     b = -clf.intercept_[0] / w[1]
#     xx = range(0, 130)
#     yy = slope * xx + b
#     line = plt.plot(xx, yy, color="magenta")
#
#     plt.scatter(df[df["Label"] == 1]["Sugars"], df[df["Label"] == 1]["Sodium"], color="blue")
#     plt.scatter(df[df["Label"] == 0]["Sugars"], df[df["Label"] == 0]["Sodium"], color="orange")
#     plt.xlabel("Sugar Level")
#     plt.ylabel("Sodium Level")
#     plt.title("Sugar vs Sodium level")
#     plt.show()
#
# draw_svc_line()
#
#

df = pd.read_csv(r"C:\Users\James\OneDrive\Documents\CVs and applications\Online Courses\AIMOOC\Modules\Module4\Data\menu.csv")

x=df[["Sugars", "Sodium"]]
y=df["Label"]

clf = lm.LogisticRegression()
clf.fit(x, y)
score = clf.score(x, y)
pred = clf.predict_proba([[60, 400]])
print(pred)