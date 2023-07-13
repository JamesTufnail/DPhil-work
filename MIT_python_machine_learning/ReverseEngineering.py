import matplotlib.pyplot as plt
import pandas as pd
import sklearn.linear_model as lm
from sklearn.preprocessing import PolynomialFeatures

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

def multiple_linear_regression(x, y):
    """ JT - Determines coefficients and R^2 for mutliple independent variables

    :param x: x values (as list [[]]) - independent variable(s)
    :param y: y values - dependent variable
    :return: Coefficients, intercept, R^2 value (close to 1 is best)
    """
    lin_reg = lm.LinearRegression()
    lin_reg.fit(x, y)

    print("Coefficient:", lin_reg.coef_)
    print("Intercept:", lin_reg.intercept_)
    print("R$^2$ value:", lin_reg.score(x, y))

def polynomial_regression(x, y, degree):
    """ JT - Plots a polynomial fit of the input variables

    :param x: x values - independent variable(s)
    :param y: y values - dependent variable
    :return:
    """
    x_trans = PolynomialFeatures(degree=degree)
    x_trans = x_trans.fit_transform(x)

    lin_reg = lm.LinearRegression()
    lin_reg.fit(x_trans, y)
    y_pred = lin_reg.predict(x_trans)

    plt.scatter(x, y)
    plt.plot(x, y_pred)
    plt.show()

    # print("Coefficients:", lin_reg.coef_)
    # print("Intercept:", lin_reg.intercept_)
    # print("R$^2$ value:", lin_reg.score(x, y))


# df = pd.read_csv(r"C:\Users\James\OneDrive\Documents\CVs and applications\Online Courses\AIMOOC\Modules\Module2\Data\car_toyota_corolla.csv")
#
# x = df[["Gallons"]]  # x values have two square brackets
# y = df["Miles"]
#
# lin_reg = lm.LinearRegression()
# lin_reg.fit(x, y)
# ypred = lin_reg.predict(x)
#
# print('Coefficient:', lin_reg.coef_)
# print('Intercept:', lin_reg.intercept_)
#
# plt.scatter( x, y)
# plt.plot(x, ypred)
#
# # Can define best fit line manually using intercept and coeff too
# # y2 = lin_reg.coef_ * x + lin_reg.intercept_
# # plt.plot(x, y2, color='orange')
# plt.show()

### Multiple Datasets ####

# df2 = pd.read_csv(r"C:\Users\James\OneDrive\Documents\CVs and applications\Online Courses\AIMOOC\Modules\Module2\Data\multicar.csv")
#
# x2 = df2[["Gallons"]]
# y2 = df2["Miles"]
#
# lin_reg2 = lm.LinearRegression()
# lin_reg2.fit(x2,y2)
# y2pred = lin_reg2.predict(x2)
#
# plt.scatter(x2,y2)
# plt.plot(x2, y2pred)
# plt.show()


##### Prediction

# df = pd.read_csv(R"C:\Users\James\OneDrive\Documents\CVs and applications\Online Courses\AIMOOC\Modules\Module2\Data\avg_h_w.csv")
#
# x = df[["Height"]]
# y = df["Weight"]
#
# lin_reg = lm.LinearRegression()
# lin_reg.fit(x, y)
# ypred = lin_reg.predict(x)
#
#
# plt.scatter(x, y)
# plt.plot(x, ypred)
# plt.show()
#
# pred_weight = lin_reg.predict([[1.61]])
# print(pred_weight)

####

df_water = pd.read_csv(r"C:\Users\James\OneDrive\Documents\CVs and applications\Online Courses\AIMOOC\Modules\Module2\Data\water_potability.csv")
df_water = df_water.dropna()

x = df_water[["ph"]]
y = df_water["Hardness"]

# multiple_linear_regression(x, y)

############## Multiple linear regression

df_salary = pd.read_csv(r"C:\Users\James\OneDrive\Documents\CVs and applications\Online Courses\AIMOOC\Modules\Module2\Data\salary.csv")

y = df_salary["salary"] # dependent variable
# x1 = df_salary[["years_education"]]
# x2 = df_salary[["net_worth"]]
# x3 = df_salary[["work_experience"]]
# x4 = df_salary[["home_cost"]]
# x5 = df_salary[["height"]]
#
# single_linear_regression(x1, y)
# single_linear_regression(x2, y)
# single_linear_regression(x3, y)
# single_linear_regression(x4, y)
# single_linear_regression(x5, y)

# x_variables = df_salary[["years_education", "net_worth", "work_experience"]]
#
# multiple_linear_regression(x_variables, y) # my defined function - note removed plot


######## Polynomial Relationships #####

df_quad = pd.read_csv(r"C:\Users\James\OneDrive\Documents\CVs and applications\Online Courses\AIMOOC\Modules\Module2\Data\quadratic.csv")

x_quad = df_quad[["x"]]
y_quad = df_quad["y"]

polynomial_regression(x_quad, y_quad, 2)