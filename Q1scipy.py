from scipy.optimize import minimize
from math import sqrt
import pandas as pd


locations=[]

df = pd.read_excel('Q1.xlsx', header=0)
for row in df.itertuples():
    locations.append(tuple(row)[1:])

print(locations)

def objective(x):
    cost=[]
    for location in locations:
        cost.append(location[1]*abs(location[0]-x))
    return sum(cost)

# Choose the initial value
x0=[0]
Sol=minimize(objective, x0)
# Print the results
print(Sol)