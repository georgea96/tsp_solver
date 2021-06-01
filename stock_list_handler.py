
import pandas as pd
import numpy as np
#Creating the stock handler class
class stock_handler:
    def __init__(self):
        #Reading the existing stock_list file
        self.stock_list=pd.read_csv('stock_list.csv', delimiter=',')
        #Defining the cartesian coordinate variables for the product
        self.x=0
        self.y=0
        self.z=0
        #Defining the cartesian coordinate variables for the robot's base to grasp a product
        self.base_x=0
        self.base_y=0
        self.base_z=0
        #Class variable to hold the products name
        self.name=[]
        #Printing existing stock list
        print(self.stock_list)

    #Function to get the name of the new product
    def get_name(self):
        #Getting a valid input from the user for the name of the product
        while True:
            name=input("Please enter Product Name to be adedd in stock: ")
            #Check if the name of the prudct is only digits
            if (name.isdigit()==True):
                print("Please try a name which has at least one character")
            else:
                #if not dont get any other inputs
                break
        return name

    def is_it_number(self,number):
        try:
            temp=float(number)
            return True
        except ValueError:
            return False
    #Fucntion to get an x,y,z input from the user separated by commas
    #Used for both base xyz and product xyz
    def get_xyz(self,xyz_for):
        y=0
        x=0
        z=0
        #Getting a valid input from the user for the XYZ coordinates
        while True:
            xyz=input("Please enter the %s XYZ coordinate within the shop separated by commas: "%xyz_for)
            splited_xyz=xyz.split(',')
            print(self.is_it_number(-5))
            #Checking if the format entered by the user is correct (i.e. 3 numbers separated by comas)
            if   (len(splited_xyz)==3):
                #Checking if every split is a degit
                if(self.is_it_number(splited_xyz[0])==True)&(self.is_it_number(splited_xyz[1])==True)&(self.is_it_number(splited_xyz[2])==True):
                    #If it is then we have some xyz coordinates
                    x=splited_xyz[0]
                    y=splited_xyz[1]
                    z=splited_xyz[2]
                    break
                else:
                    print("Wrong Try again please")
            else:
                print("Wrong Try again please")
        return x,y,z

    #Wrapper for getting input from the suer
    def get_user_input(self):
        #Function call to get the name of the product
        self.name=self.get_name()
        #Function call to get the products xyz coordinates
        self.x,self.y,self.z=self.get_xyz(xyz_for="product's")
        #Function call to get the robot's base xyz coordinates
        self.base_x,self.base_y,self.base_z=self.get_xyz(xyz_for="robot's base")

    #Function for validating the input frrom the user
    def validate(self):
        xyz_flag=False
        name_flag=False

        #========================================================================#
        #                            Change Accordingly                          #
        #========================================================================#
        #Specify the distances products should have between them in XYZ direction
        x_thresh=5
        y_thresh=5
        z_thresh=2
        #=======================================================================#
        #=======================================================================#


        #Loading only the names of the products already in stock
        stock_names=self.stock_list.loc[:,'Name']

        #Loading the locations of the products in stock
        stock_locations=self.stock_list.loc[:,['X','Y','Z']]

        #Creating a series using the new products xyz coordinates
        sr = pd.to_numeric(pd.Series([self.x, self.y,self.z], index =['X','Y','Z']))
        #Subtracting the new products xyz coordinates with every product already in stock
        diff_with_existing_products=stock_locations.subtract(sr, axis = 1)


        #Checking if there is a product already in stock with the name of the new product
        if (any(stock_names.loc[:]==self.name)==True):
            print("Product already exist in the database")
            #If there is then we dont pass the validation check
            name_flag=False
        else:
            name_flag=True

        #Checking if the inputted xyz coordinates of the product are within the threshold requested.
        if ((   any(diff_with_existing_products['X']<=x_thresh) &   any(diff_with_existing_products['X']>=-x_thresh) )
         |  (   any(diff_with_existing_products['Y']<=y_thresh) &   any(diff_with_existing_products['Y']>=-y_thresh) )
         |  (   any(diff_with_existing_products['Z']<=z_thresh) &   any(diff_with_existing_products['Z']>=-z_thresh) ) ):
            #If the coordiantes requested are within the threshold then try again
            print("Product Coordinates of product are not available.. Try Again")
            xyz_flag=False
        else:
            xyz_flag=True

        #If either the name already exist in the database or the product is too close to another product
        if (xyz_flag==False)|(name_flag==False):
            #Validation failed return false
            return False
        else:
            #Validation succesful return true
            return True

    #Wrapper function to get user input and validate it
    def add_new_product(self):
        validation_flag = False
        while validation_flag!=True:
            #Getting input from the user (new product anme, xyz coordinates, base xyz coordinates)\
            self.get_user_input()

            #If the input has passed the vlaidation
            if self.validate() == True:
                validation_flag=True
                #Add the new product in stock list
                self.stock_list.loc[len(self.stock_list)] = [self.name,self.x,self.y,self.z,self.base_x,self.base_y,self.base_z]
                #Append to the csv file without row index
                self.stock_list.to_csv('stock_list.csv', index = False)
                #Let the user know
                print("Product Succesfully added in stock")
                break



if __name__ == '__main__':

    while True:
        stock=stock_handler()
        stock.add_new_product()
        user_input=input("Press any other key to continue \nPress 'q' to quit \n")
        if (user_input == 'q'):
            break
