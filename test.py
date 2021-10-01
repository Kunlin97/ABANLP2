import pandas as pd
from pyomo.environ import *

# create a model instance
model = ConcreteModel()

# create x and y variables in the model
model.x = Var()

locations=[]

df = pd.read_excel('Q1.xlsx', header=0)
for row in df.itertuples():
    locations.append(tuple(row)[1:])

print(locations)

'''
def objective(x):
    cost=[]
    for location in locations:
        cost.append(location[1]*abs(location[0]-x))
    return sum(cost)
'''
# add a model objective
model.objective = Objective(expr = locations[0][1]*abs(locations[0][0]-model.x)+locations[1][1]*abs(locations[1][0]-model.x)+locations[2][1]*abs(locations[2][0]-model.x)+locations[3][1]*abs(locations[3][0]-model.x), sense=minimize)
results = SolverFactory('ipopt').solve(model)
model.pprint()