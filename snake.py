import numpy as np
import matplotlib.pyplot as plt
import random # random number generators

""" Parameters """ 

snake_step_score=1 #amount of reward for taking a step without collision
snake_food_score=200 #amount of reward for getting food

""" Move the snake to a new position """ 
def move_snake(Coordinates,New_Position):
    Coordinates[0:-1]=Coordinates[1:]
    Coordinates[-1]=New_Position
    
""" Check for collisions """ 
def collision_check(Coordinates,New_Position,size):
    #Check for collision with the wall first
    if( (New_Position[0]<=0) or (New_Position[1]<=0) or (New_Position[0]>=size) or (New_Position[1]>=size)):
        iscollision=True
    elif (np.any((Coordinates[:,1]==New_Position[1])*(Coordinates[:,0]==New_Position[0]))):
        iscollision=True
    else:
        iscollision=False #default
    
    return iscollision
 
""" Grow snake """ 
def grow_snake(Coordinates,New_Position):
    
    Coordinates=np.append(Coordinates,[New_Position],axis=0)
    return Coordinates
    

def snake_step(Coordinates,size,Foodcoordinates,plot_image,chosen_action):
    reward=0 #default

    
    #Find  the direction the snake is heading
    Direction=Coordinates[-1]-Coordinates[-2]
    
    #Decide what to do based on input
    if (chosen_action==0): #Player pressed LEFT
        NewDirection=[-1,0]
    elif (chosen_action==1): #Player pressed RIGHT
        NewDirection=[1,0]
    elif (chosen_action==2): #Player pressed UP
        NewDirection=[0,1]
    elif (chosen_action==3): #Player pressed DOWN
        NewDirection=[0,-1]
    
    #Check if the new direction is valid
    if (np.dot(Direction,NewDirection)!=0): #0 would mean perpendicular, this means invalid move
        NewDirection=Direction #revert to old direction
        
    #Find new coordinate
    New_Position=Coordinates[-1]+NewDirection
    
    #Check for collision
    iscollision=collision_check(Coordinates,New_Position,size)
    
    if(not iscollision): #no collision
        #Did it get the food?
        if (np.all(New_Position==Foodcoordinates)):
            Coordinates=grow_snake(Coordinates,New_Position) #yum-yum, grow snake
            reward=snake_food_score
            #Check if snake is too large
            if(len(Coordinates[:,0])>=(size-1)**2):
                iscollision=True #End the game
            else:
                #Set down new food
                empty=False
                while(empty==False):
                    #find coordinates that are not occupied by the snake
                    food_x=random.randint(1,size-1)
                    food_y=random.randint(1,size-1)
                    empty=(not np.any((Coordinates[:,1]==food_y)*(Coordinates[:,0]==food_x)))
                Foodcoordinates=np.array([food_x,food_y])
        else:
            move_snake(Coordinates,New_Position)
            reward=snake_step_score
     
    #Plot Image  
    if (plot_image):
        print ''
        #make coordinate arrays
        X_array=np.ndarray([size+1,size+1])
        Y_array=np.ndarray([size+1,size+1])
        for i in range(size+1):
            X_array[i,:]=i
            Y_array[:,i]=i
        X_array=X_array
        Y_array=Y_array
        #Find walls
        Walls=((X_array<=0)+(Y_array<=0)+(X_array>=size)+(Y_array>=size))
        #Find the body of the snake
        Snake_on_board=np.zeros([size+1,size+1],dtype=bool)
        for i in range(len(Coordinates[:,0])):
            Snake_on_board=Snake_on_board+( (X_array==Coordinates[i,0])*(Y_array==Coordinates[i,1]) )
        #Find food
        Food_on_board=(X_array==Foodcoordinates[0])*(Y_array==Foodcoordinates[1])
        #Create color array for plot, default white color
        Color_array=np.zeros([size+1,size+1])
        Color_array[Walls]=-1 #black walls
        Color_array[Snake_on_board]=-0.75 #bluish snake
        Color_array[Food_on_board]=-0.25 #orange food
        #plot
        fig=plt.figure()
        plt.axis('off')
        plt.imshow(Color_array,cmap='gnuplot2', interpolation='nearest')
        plt.show()
    
    if (plot_image):
        return (iscollision, reward, Coordinates, Foodcoordinates,fig) #return reward and collision state
    else:
        return (iscollision, reward, Coordinates, Foodcoordinates) #return reward and collision state
            
        
        
    
    