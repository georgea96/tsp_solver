import matplotlib.pyplot as plt
import numpy as np
import util

visualization = False


locations= np.array([(250, 250,250), # location 0 - the depot
                    (228, 0,0),    # location 1
                    (500, 0,2),    # location 2
                    (0, 80,5),     # location 3
                    (124, 101,6),   # location 4
                    (370, 160,12),  # location 5
                    (30, 360, 0)] ) # location 6

plt.figure(figsize=(8,5))
plt.scatter(locations[0,0],locations[0,1], color="red") # depot

res_out=[]
loc_out = []
loc_cluster_save = []

cost_matrix = util.def_cost_matrix(locations)
sol, result= util.solve_tsp(locations,cost_matrix)

print("Robot follows the route: {}".format(sol))



res_out.append(sol)
if visualization == True:
    for i in sol:
        loc_out.append(locations[i - 1])

    for i in range(len(locations)-1): # customers loc
        plt.scatter(locations[i+1,0],locations[i+1,1], color="blue")
    for index in range(len(loc_out)-1):
        x=[loc_out[index][0],loc_out[index+1][0]]
        y=[loc_out[index][1],loc_out[index+1][1]]
        plt.plot(x,y,'black')
    plt.show()
