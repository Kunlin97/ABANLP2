from scipy.optimize import minimize
from math import sqrt
import numpy as np
import pandas as pd


coefficients=[]

df = pd.read_excel('Q4.xlsx', header=0,)
for row in df.itertuples():
    coefficients.append(tuple(row)[2:])
#coefficients=np.array(df)
coefficientsT=np.transpose(coefficients)

costs=[2,2.2,2.3,2.4]
print(coefficientsT)

# Calculate the predicted demands for all types of lipsticks.
def objective(x):     
    demands=[]
    for coefficient in coefficientsT:
        a=coefficient[0]
        i=0
        while i<4:
            i+=1
            a+=coefficient[i]*x[i-1]
        demands.append(a)
    return np.dot(demands,costs-x)

def costraint_total_demand(x):
    capacity=10000
    for coefficient in coefficientsT:
        capacity=capacity-coefficient[0]
        i=0
        while i<4:
            i+=1
            capacity-=coefficient[i]*x[i-1]
    return capacity

def non_negative_demand(x):
    demands=[]
    for coefficient in coefficientsT:
        demands.append(coefficient[0]+coefficient[1]*x[0]+coefficient[2]*x[1]+coefficient[3]*x[2]+coefficient[4]*x[3])
    return demands    

x0=[3,3,3,3]
b=(2.4,20)
bnds=(b,b,b,b)

con0 = {'type': 'ineq', 'fun': costraint_total_demand}
con1 = {'type': 'ineq', 'fun': non_negative_demand}
cons=[con0,con1]

sol=minimize(objective,x0, bounds=bnds,constraints=cons)
# Print the solution regardless of integer constraints
print(sol.x)
print('maximum expected profit is', -objective(sol.x))