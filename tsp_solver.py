import matplotlib.pyplot as plt
import numpy as np
import util
import csv
import os
import pandas as pd



def validate(stock_list,customer_entry):
    exists = any(stock_list.Name==customer_entry)
    return exists

def get_shopping_list(stock):
    shopping_list=[]
    print("Please enter an item to purchase...\n\nPress 'q' if you are done with your shopping list.\n")

    while True:
        customer_entry=input()
        if (customer_entry=='q'):
            break
        else:
            result=validate(stock,customer_entry)
            if result==True:
                shopping_list.append(customer_entry)
            else:
                print("Sorry this item is not in stock")

    # Displaying the Customer Shopping List
    print("\n\n----------------------")
    print("Your Shopping List is")
    print("----------------------")
    [print(x) for x in shopping_list]
    print("----------------------\n\n")

    return shopping_list

def sort_shopping_list(stock,shopping_list,visualization=False):
    #Filtering customer items from stock dataframe
    customer_items=stock[stock['Name'].isin(shopping_list)]
    # print(customer_items)

    # Adding two extra nodes which are fixed --> The entrance
    top_row = pd.DataFrame({'Name':['Entrance'],'Base_X':[-1.69],'Base_Y':[-1.79],'Base_Z':[0],'Roll':[0],'Pitch':[0],'Yaw':[2.5]})
    #Concatenating the customer items with the location of entrance
    customer_items = pd.concat([top_row,customer_items]).reset_index(drop = True)
    # Adding two extra nodes which are fixed --> the Till
    bottom_row = pd.DataFrame({'Name':['Till'],'Base_X':[-2.0],'Base_Y':[2.0],'Base_Z':[0],'Roll':[0],'Pitch':[0],'Yaw':[-0.785]})
    #Concatenating the customer items with the two fixed location of till
    customer_items = pd.concat([customer_items,bottom_row]).reset_index(drop = True)


    #Clamping of names keeping only base X and y coordinate for TSP
    locations_array=customer_items.loc[:,['Base_X','Base_Y']]

    # Converting the dataframe to a numpy array
    #Making everything float
    locations_array=(locations_array.to_numpy()).astype('float32')

    #Calculating the cost matrix
    cost_matrix = util.def_cost_matrix(locations_array[:,:2])

    #Hacking the cost matrix with a dummy node
    # The procedure followed is explained here:
    # https://stackoverflow.com/questions/14527815/how-to-fix-the-start-and-end-points-in-travelling-salesmen-problem
    dummy_node_column=10E5*np.ones((1,cost_matrix.shape[1]))
    dummy_node_row=10E5*np.ones((1+cost_matrix.shape[0],1))
    cost_matrix=np.vstack([cost_matrix,dummy_node_column])
    cost_matrix=np.hstack([cost_matrix,dummy_node_row])
    cost_matrix[-1,-1]=0
    cost_matrix[-1,0]=0

    #Temporarily removing till from cost matrix and using dummy node to find a solution
    cost_matrix=np.delete(cost_matrix,-2,0)

    #Solving the TSP problem
    sol, result= util.solve_tsp(locations_array,cost_matrix)

    #Reordering the dataframe to obtain ir in the order appearing in the solution
    customer_items=customer_items.reindex([x-1 for x in sol])

    # Outputting the solution
    print("The robot will follow the route:")
    print(customer_items.loc[:]['Name'])

    #List for vizualization purposes
    loc_out = []


    #Vizualization of the graph with its nodes if requested
    if visualization == True:
        plt.figure(figsize=(8, 5))

        #Populating list to be used for edges plotting
        for i in sol:
            loc_out.append(locations_array[i - 1])

        #plotting the nodes of the graph
        for i in range(len(locations_array)-2): # customers loc
            plt.scatter(locations_array[i+1,0],locations_array[i+1,1], color="blue")
            plt.text(locations_array[i+1,0]-0.02,locations_array[i+1,1]+0.2, customer_items.loc[i+1]['Name'])

        #Plotting the edges of the graph
        for index in range(len(loc_out)-1):
            x=[loc_out[index][0],loc_out[index+1][0]]
            y=[loc_out[index][1],loc_out[index+1][1]]
            plt.plot(x,y,'black')

        #Plotting till and entrance points with their corresponding text
        plt.scatter(locations_array[0, 0], locations_array[0, 1], color="red")
        plt.text(locations_array[0,0]-0.02,locations_array[0,1]+0.2, "Entrance")
        plt.text(locations_array[-1,0]-0.02,locations_array[-1,1]-0.4, "Till")
        plt.scatter(locations_array[-1, 0], locations_array[-1, 1], color="red")

        plt.title('TSP solution')
        plt.xlabel("Shop X-Coordinate")
        plt.ylabel("Shop Y-Coordinate")
        plt.savefig('TSP_solution_example.png')
        plt.show()
    return customer_items

if __name__ == "__main__":
    # Reading the stock which exist in the shop
    path=os.getcwd()
    stock=pd.read_csv(path+'/stock_list.csv', delimiter=',')

    #Displaying Stock to the customer
    print("Our stock is:\n================")
    print(stock.loc[:,'Name'])

    # Getting the shopping list input from the customer and validating it
    shopping_list=get_shopping_list(stock)

    #Solving the TSP problem returning poses to be visited
    sol=sort_shopping_list(stock,shopping_list,visualization=True)
