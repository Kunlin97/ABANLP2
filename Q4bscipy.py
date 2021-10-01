from scipy.optimize import minimize
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

# Define the objective
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
# Total demand is less than or equal to 10000
def costraint_total_demand(x):
    capacity=10000
    for coefficient in coefficientsT:
        capacity=capacity-coefficient[0]
        i=0
        while i<4:
            i+=1
            capacity-=coefficient[i]*x[i-1]
    return capacity
# The demands function for each type of lipsticks
def demands(x):
    demands=[]
    for coefficient in coefficientsT:
        a=coefficient[0]
        i=0
        while i<4:
            i+=1
            a+=coefficient[i]*x[i-1]
        demands.append(a)
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
x0=[3,3,3,3]
#define bounds
b=(2.4,20)
bnds=(b,b,b,b)

con0 = {'type': 'ineq', 'fun': costraint_total_demand}
con1 = {'type': 'ineq', 'fun': demands}
cons=[con0,con1]

sol=minimize(objective,x0, bounds=bnds,constraints=cons)

# Print the solution 
print(sol.x)
print(-objective(sol.x))