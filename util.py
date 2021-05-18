import pyomo.environ as pyEnv
import scipy.spatial
import numpy as np

def distance(loc1, loc2):
#     dist = np.linalg.norm(abs(loc1-loc2))
#     dist = math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))
    dist =scipy.spatial.distance.euclidean(loc1,loc2)
#     dist = (loc1[0]-loc2[0])**2 + (loc1[1]-loc2[1])**2
    return dist

def def_cost_matrix(locations):
    cost_matrix = np.zeros((len(locations), len(locations))) # creates matrix with all values zero
    for idx1, loc1 in enumerate(locations):
        for idx2, loc2 in enumerate(locations):
            cost_matrix[idx1, idx2] = distance(loc1, loc2)
#     np.fill_diagonal(cost_matrix,6E9)
    return cost_matrix

def obj_func(model):
    return sum(model.x[i,j] * model.c[i,j] for i in model.N for j in model.M)
def rule_const1(model,M):
    return sum(model.x[i,M] for i in model.N if i!=M ) == 1

def rule_const2(model,N):
    return sum(model.x[N,j] for j in model.M if j!=N) == 1

def rule_const3(model,i,j):

    #Acessing the lengtth of the Cost Matrix
    length_of_cost_matrix=max(model.M.ordered_data())

    if i!=j:
        return model.u[i] - model.u[j] + model.x[i,j] * length_of_cost_matrix <= length_of_cost_matrix-1
    else:
        #Yeah, this else doesn't say anything
        return model.u[i] - model.u[i] == 0


def solve_tsp(locations_tsp, cost_matrix):  # based on "http://www.opl.ufc.br/post/tsp/"
    # Model
    model = pyEnv.ConcreteModel()

    # Indexes for the cities
    model.M = pyEnv.RangeSet(len(locations_tsp))
    model.N = pyEnv.RangeSet(len(locations_tsp))

    # Index for the dummy variable u
    model.U = pyEnv.RangeSet(2, len(locations_tsp))

    # Decision variables xij
    model.x = pyEnv.Var(model.N, model.M, within=pyEnv.Binary)
    #     model.x = pyEnv.Var(model.N, within=pyEnv.Binary)

    # Dummy variable ui
    model.u = pyEnv.Var(model.N, within=pyEnv.NonNegativeIntegers, bounds=(0, len(cost_matrix) - 1))

    # Cost Matrix cij
    #     model.c = pyEnv.Param(model.N, model.M,initialize=lambda model, i, j: cost_matrix[i][j])
    model.c = pyEnv.Param(model.N, model.M, initialize=lambda model, i, j: cost_matrix[i - 1][j - 1])

    model.objective = pyEnv.Objective(rule=obj_func, sense=pyEnv.minimize)

    model.const1 = pyEnv.Constraint(model.M, rule=rule_const1)

    model.rest2 = pyEnv.Constraint(model.N, rule=rule_const2)

    model.rest3 = pyEnv.Constraint(model.U, model.N, rule=rule_const3)

    #     model.pprint()

    # Solves
    solver = pyEnv.SolverFactory('glpk')
    result = solver.solve(model, tee=False)
    #     solver = pyEnv.SolverFactory('cplex')
    #     result = solver.solve(model,tee = True)

    l = list(model.x.keys())
    sol = []
    for i in l:
        if model.x[i]() != 0:
            if model.x[i]() != None:
                sol.append(i)
    #     print(sol)
    print(sol)
    # sort the solution
    sorted_sol = [sol[0][0], sol[0][1]]  # list of visited location ids, always starting at the depot
    #     print(sorted_sol)
    for i in sol:
        #         print("i:"+ str(i))
        for ii in sol:
            #             print("ii:"+ str(ii))
            last_loc = sorted_sol[-1]  # sorted_sol[len(sorted_sol)-1]
            #             print("last loc:"+ str(last_loc))
            if ii[0] == last_loc:
                if ii[1] == 1:  # stop if we are back at the depot
                    break
                else:
                    sorted_sol.append(ii[1])

    sorted_sol.append(sol[0][0])  # we go back to the depot

    return sorted_sol, result