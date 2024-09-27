import numpy as np 
import matplotlib.pyplot as plt

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Sample data~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# A=0, B=1, D=3, E=4
#pristine, pre irrad, 3x during irrad, post 24 hr gamma irrad
Ic_Sample_A = [14.23, 14.27, 14.2, 14.24, 14.17, 14.40] # [14.27,14.20,14.40] # 
RMS_Ic_Sample_A =  [0.04, 0.03, 0.03, 0.03, 0.03, 0.02] # [0.03,0.03,0.02] #

Ic_Sample_B = [13.38, 13.43, 13.22, 13.2, 13.28, 13.45]
RMS_Ic_Sample_B = [0.04, 0.03,0.03,0.03,0.03,0.01]

Ic_Sample_D = [14.67, 14.42, 14.32, 14.32, 14.37, 14.58]
RMS_Ic_Sample_D = [0.04, 0.02,0.02,0.02,0.02,0.01]

Ic_Sample_E = [14.1, 12.63, 12.52, 12.59, 12.53, 12.79]
RMS_Ic_Sample_E = [0.04, 0.03,0.03,0.03,0.03,0.02]

# C=2 in the list which is damaged
Ic_Sample_C = [14.2, 8.59, 8.44, 8.54, 8.54, 9.15]
RMS_Ic_Sample_C = [0.04, 0.05, 0.05, 0.05, 0.05, 0.02]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Raw Figure~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# fig = plt.figure()
# ax = fig.add_subplot(111)
# colours = plt.cm.viridis(np.linspace(0,1,6))

# ax.scatter([1,2,3,4,5,6,7,8,9],Ic_Sample_A, marker = 'x', color = colours[0])
# ax.plot([0,10],[Ic_Sample_A[0],Ic_Sample_A[0]],"--", color = colours[0])

# ax.scatter([1,2,3,4,5,6,7,8,9],Ic_Sample_B, marker = 's', color = colours[1],facecolors='none')
# ax.plot([0,10],[Ic_Sample_B[0],Ic_Sample_B[0]],"--", color = colours[1])

# ax.scatter([1,2,3,4,5],Ic_Sample_C, marker = 'v', color = colours[2],facecolors='none')
# ax.plot([0,10],[Ic_Sample_C[0],Ic_Sample_C[0]],"--", color = colours[2])

# ax.scatter([1,2,3,4,5],Ic_Sample_D, marker = 'o', color = colours[3],facecolors='none')
# ax.plot([0,10],[Ic_Sample_D[0],Ic_Sample_D[0]],"--", color = colours[3])

# ax.scatter([1,2,3,4,5],Ic_Sample_E, marker = '^', color = colours[4],facecolors='none')
# ax.plot([0,10],[Ic_Sample_E[0],Ic_Sample_E[0]],"--", color = colours[4])

# ax.scatter([1,2,3,4,5],Ic_Sample_F, marker = '*', color = colours[5],facecolors='none')
# ax.plot([0,10],[Ic_Sample_F[0],Ic_Sample_F[0]],"--", color = colours[5])


# ax.set_ylim(5,25)
# ax.set_xlim(0,10)
# plt.xticks([1,2,3,4,5,6,7,8,9],["Before \n irradiation", "In-situ \n test 1","In-situ \n test 2", "In-situ \n test 3","After \n irradiation", "Post 208 kGy \n In-situ test 1", "Post 208 kGy \n In-situ test 2", "Post 208 kGy \n In-situ test 3", "Post 208 kGy \n after irradiation"])
# # plt.yticks([0.1,0.05,0,-0.05,-0.1])
# plt.tight_layout()

# plt.show()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Normalised Figure~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


# fig = plt.figure()
# ax = fig.add_subplot(111)
# colours = plt.cm.viridis(np.linspace(0,1,6))

# ax.scatter([1,2,3,4,5,6,7,8],Ic_Sample_A[1:]/(np.ones(8)*Ic_Sample_A[0]), marker = 'x', color = colours[0],s = 60, label = "Sample A")

# ax.scatter([1,2,3,4,5,6,7,8],Ic_Sample_B[1:]/(np.ones(8)*Ic_Sample_B[0]), marker = 's', color = colours[1],facecolors='none',s = 60, label = "Sample B")

# ax.scatter([1,2,3,4],Ic_Sample_C[1:]/(np.ones(4)*Ic_Sample_C[0]), marker = 'v', color = colours[2],facecolors='none',s = 60, label = "Sample C")

# ax.scatter([1,2,3,4],Ic_Sample_D[1:]/(np.ones(4)*Ic_Sample_D[0]), marker = 'o', color = colours[3],facecolors='none',s = 60, label = "Sample D")

# ax.scatter([1,2,3,4],Ic_Sample_E[1:]/(np.ones(4)*Ic_Sample_E[0]), marker = '^', color = colours[4],facecolors='none',s = 60, label = "Sample E")

# ax.scatter([1,2,3,4],Ic_Sample_F[1:]/(np.ones(4)*Ic_Sample_F[0]), marker = '*', color = colours[5],facecolors='none',s = 120, label = "Sample F")


# ax.plot([0,10],[1,1],"--", color = 'black')


# ax.set_ylim(0.99,1.01)
# ax.set_xlim(0,9)
# plt.xticks([1,2,3,4,5,6,7,8],["In-situ \n test 1","In-situ \n test 2", "In-situ \n test 3","After \n irradiation", "Post \n 208 kGy \n in-situ \n test 1", "Post \n 208 kGy \n in-situ \n test 2", "Post \n 208 kGy \n in-situ \n test 3", "Post \n 208 kGy \n after \n irradiation"])
# plt.yticks([0.99,0.995,1,1.005,1.01])
# ax.set_ylabel("Critical current normalised against \n pre irradiation critical current ")
# plt.legend(frameon=False)
# plt.tight_layout()
# plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
colours = plt.cm.viridis(np.linspace(0,1,5))

ax.errorbar([1,2,3,4,5,6],Ic_Sample_A, yerr = RMS_Ic_Sample_A, marker = 'none', color = colours[0],markersize = 10, label = "Sample Ic#1",  capsize=10)
ax.errorbar([1,2,3,4,5,6],Ic_Sample_B, yerr = RMS_Ic_Sample_B, marker = 'none', color = colours[1],markersize = 10, label = "Sample Ic#2",  capsize=10)
ax.errorbar([1,2,3,4,5,6],Ic_Sample_D, yerr = RMS_Ic_Sample_D, marker = 'none', color = colours[2],markersize = 10, label = "Sample Ic#3",  capsize=10)
# ax.errorbar([1,2,3,4,5,6],Ic_Sample_E, yerr = RMS_Ic_Sample_E, marker = 'none', color = colours[3],markersize = 10, label = "Sample Ic#4",  capsize=10)

# ax.errorbar([1,2,3,4,5,6],Ic_Sample_C, yerr = RMS_Ic_Sample_C, marker = 'none', color = colours[4],markersize = 10, label = "Sample Ic#5",  capsize=10)

# ax.set_ylim(12,15)
plt.xticks([1,2,3,4,5,6],["pre \n ion \n irradiation", "post \n ion \n irradiation", "in-situ \n gamma \n test #1", "in-situ \n gamma \n test #2", "in-situ \n gamma \n test #3", "post \n gamma \n long-irradiation"])
ax.set_ylabel("Critical current [A]")
plt.legend(frameon=False, ncol=2)
ax.tick_params(top = True, right = True, direction = 'in', which = 'both')
plt.tight_layout()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
colours = plt.cm.viridis(np.linspace(0,1,5))

# ax.errorbar([1,2,3,4,5,6],Ic_Sample_A/(np.ones(6)*Ic_Sample_A[0]), yerr = RMS_Ic_Sample_A/(np.ones(6)*Ic_Sample_A[0]), marker = 'none', color = colours[0],markersize = 10, label = "Sample Ic#1", capsize=10)
# ax.errorbar([1,2,3,4,5,6],Ic_Sample_B/(np.ones(6)*Ic_Sample_B[0]), yerr = RMS_Ic_Sample_A/(np.ones(6)*Ic_Sample_B[0]), marker = 'none', color = colours[1],markersize = 10, label = "Sample Ic#2",  capsize=10)
# ax.errorbar([1,2,3,4,5,6],Ic_Sample_D/(np.ones(6)*Ic_Sample_D[0]), yerr = RMS_Ic_Sample_D/(np.ones(6)*Ic_Sample_D[0]), marker = 'none', color = colours[2],markersize = 10, label = "Sample Ic#3",  capsize=10)
ax.errorbar([1,2,3,4,5,6],Ic_Sample_E/(np.ones(6)*Ic_Sample_E[0]), yerr = RMS_Ic_Sample_E/(np.ones(6)*Ic_Sample_E[0]), marker = 'none', color = colours[3],markersize = 10, label = "Sample Ic#4",  capsize=10)
ax.errorbar([1,2,3,4,5,6],Ic_Sample_C/(np.ones(6)*Ic_Sample_C[0]), yerr = RMS_Ic_Sample_C/(np.ones(6)*Ic_Sample_C[0]), marker = 'none', color = colours[4],markersize = 10, label = "Sample Ic#5",  capsize=10)

# ax.set_ylim(0.97,1.03)
plt.xticks([1,2,3,4,5,6],["pre \n ion \n irradiation", "post \n ion \n irradiation", "in-situ \n gamma \n test #1", "in-situ \n gamma \n test #2", "in-situ \n gamma \n test #3", "post \n gamma \n long-irradiation"])
ax.set_ylabel("Critical current normalised against \n pre irradiation critical current ")
plt.axhline(y=1, color='grey', linestyle='--')
plt.axhline(y=0.9, color='grey', linestyle='--')
plt.legend(frameon=False)
ax.tick_params(top = True, right = True, direction = 'in', which = 'both')
plt.tight_layout()
plt.show()