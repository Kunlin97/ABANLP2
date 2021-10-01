from scipy.optimize import minimize
import numpy as np
import pandas as pd
from itertools import combinations

#input data
coefficients=[]

df = pd.read_excel('Q4.xlsx', header=0,)
for row in df.itertuples():
    coefficients.append(tuple(row)[2:])
#coefficients=np.array(df)
coefficientsT=np.transpose(coefficients)

costs=[2,2.2,2.3,2.4]
print(coefficientsT)


def objective(x):     
    demands=[]
    for coefficient in coefficientsT:
        demands.append(coefficient[0]+coefficient[1]*x[0]+coefficient[2]*x[1]+coefficient[3]*x[2]+coefficient[4]*x[3])
    return np.dot(demands,costs-np.array([x[0], x[1], x[2], x[3]]))+20000*x[4]
# The total predicted demands for all types of lipsticks is less than 10000+1000* extra capacity.
def total_demand(x):
    capacity=10000+1000*x[4]
    for coefficient in coefficientsT:
        capacity -= coefficient[0]+coefficient[1]*x[0]+coefficient[2]*x[1]+coefficient[3]*x[2]+coefficient[4]*x[3]
    return capacity
# The demands function for each type of lipsticks
def demands(x):
    demands=[]
    for coefficient in coefficientsT:
        demands.append(coefficient[0]+coefficient[1]*x[0]+coefficient[2]*x[1]+coefficient[3]*x[2]+coefficient[4]*x[3])
    return demands
#The predicted demand for SL
def constraint0(x):
    return demands(x)[0]
#The predicted demand for CB
def constraint1(x):
    return demands(x)[1]
#The predicted demand for AS
def constraint2(x):
    return demands(x)[2]
#The predicted demand for HB
def constraint3(x):
    return demands(x)[3]

#choose the initail values
x0=[3,3,3,3,0]
#define bounds
b=(0,20)
bnds=(b,b,b,b,b)

con0 = {'type': 'ineq', 'fun': total_demand}
con1 = {'type': 'ineq', 'fun': constraint0}
con2 = {'type': 'ineq', 'fun': constraint1}
con3 = {'type': 'ineq', 'fun': constraint2}
con4 = {'type': 'ineq', 'fun': constraint3}
cons=[con0,con1,con2,con3,con4]


sol=minimize(objective,x0, bounds=bnds,constraints=cons)
# Print the solution and the optimized profit
print(sol.x)
print(-objective(sol.x))

#see when extra capacity range from 0 to 10, where is the most profit.
combinations=[]
i=-1
while i<10:
    i+=1
    combinations.append([sol.x[0],sol.x[1],sol.x[2],sol.x[3],(int(sol.x[4])+i)])

##print(combinations)
#good combination should meet the constraints
good_combinations=[]
for combination in combinations:
    if total_demand(combination)>=min(0,total_demand([5.577870398282241, 6.0658776866581565, 5.754240645077893, 6.141134588445512, 0])): #this constraint should be bounding with the actual solution. However, because of limited decimals, the value of the constraint is less than 0.
        if all(demand>=0 for demand in demands(combination)):
           good_combinations.append(combination)

##print(good_combinations)
# Calculate the cost value for all valid combinations.
values=[]
for combination in good_combinations:
    values.append(-objective(combination))

# Find the max profit value
max_value = max(values)
# and the indices of these values
max_indices = [index for index, element in enumerate(values) if element == max_value]
# And print out all the combinations which will give this max profit value
for max_index in max_indices:
    print(good_combinations[max_index])
