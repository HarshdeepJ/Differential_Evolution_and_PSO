import numpy as np
import random
import matplotlib.pyplot as plt

def EggHolder(x,y):
    return -(y+47)*np.sin(np.sqrt(np.abs(x/2+y+47)))-x*np.sin(np.sqrt(np.abs(x-y-47)))

#To check if the new coordinates are within the constraints
def Evaluate_constraints(x,y):
    if x > 512 or x < -512:
         return False
    elif y > 512 or y < -512:
         return False
    
    return True

#To update the personal best coordinates of the candidates
def update_p_best(coordinates,personal_best_of_candidate):
    for i in range(len(coordinates)):
        if EggHolder(coordinates[i][0],coordinates[i][1]) < EggHolder(personal_best_of_candidate[i][0],personal_best_of_candidate[i][1]):
            personal_best_of_candidate[i] = [coordinates[i][0],coordinates[i][1]]

#To update the global best coordinates of all the candidates
def update_g_best(coordinates,global_best_across_generations):
    for i in range(len(coordinates)):
        if EggHolder(coordinates[i][0],coordinates[i][1]) < EggHolder(global_best_across_generations[0],global_best_across_generations[1]):
            global_best_across_generations = [coordinates[i][0],coordinates[i][1]]

#To give the minimum value of EggHolder for a given generation candidates
def min_across_gens(coordinates):
    min_value = EggHolder(coordinates[0][0],coordinates[0][1])
    for i in range(len(coordinates)):
        if EggHolder(coordinates[i][0],coordinates[i][1]) < min_value:
            min_value = EggHolder(coordinates[i][0],coordinates[i][1])
    return min_value

#To give the mean value of EggHolder for a given generation candidates
def mean_across_gens(coordinates):
    sum_value = 0
    for i in range(len(coordinates)):
        sum_value = sum_value + EggHolder(coordinates[i][0],coordinates[i][1])
    return sum_value/len(coordinates)

if __name__ == '__main__':
    generations = [50,100,200]
    population_sizes = [20,50,100,200]
    for population_size in population_sizes:
        for generation in generations:
            coordinates = []
            mean_across_generations = []
            min_across_generations = []
            personal_best_of_candidate = []
            global_best_across_generations = []
            velocity_of_candidate = []
            for i in range(population_size):
                #Random generation of coordinates for all candidates
                coordinates.append([random.uniform(-512,512),random.uniform(-512,512)])
                #Also assigning the personal best coordinates of all candidates
                personal_best_of_candidate.append([coordinates[i][0],coordinates[i][1]])
                #Initialization of velocity as 0 in both the axis
                velocity_of_candidate.append([0,0])
                if i == 0:
                    global_best_across_generations = [coordinates[i][0],coordinates[i][1]]
                else:
                    if(EggHolder(coordinates[i][0],coordinates[i][1]) < EggHolder(global_best_across_generations[0],global_best_across_generations[1])):#Updating the global best coordinates of all candidates
                        global_best_across_generations = [coordinates[i][0],coordinates[i][1]]

            c1 = random.uniform(0,4)
            c2 = 4-c1

            for i in range(generation):
                for j in range(population_size):
                    rand = random.uniform(0,1)
                    #Updating the velocity of candidate j
                    new_velocity_x = velocity_of_candidate[j][0]+c1*rand*(personal_best_of_candidate[j][0]-coordinates[j][0])+c2*rand*(global_best_across_generations[0]-coordinates[j][0])
                    new_velocity_y = velocity_of_candidate[j][1]+c1*rand*(personal_best_of_candidate[j][1]-coordinates[j][1])+c2*rand*(global_best_across_generations[1]-coordinates[j][1])
                    #Check if the new coordinates are within the constraints
                    if Evaluate_constraints(coordinates[j][0]+new_velocity_x,coordinates[j][1]+new_velocity_y):
                        coordinates[j][0] = coordinates[j][0]+new_velocity_x
                        coordinates[j][1] = coordinates[j][1]+new_velocity_y
                    else:
                        continue
                    
                    #Updating the personal best coordinates of candidate j
                    update_p_best(coordinates,personal_best_of_candidate)
                #Updating the global best coordinates of all the candidates
                update_g_best(coordinates,global_best_across_generations)
                min_across_generations.append(min_across_gens(coordinates))
                mean_across_generations.append(mean_across_gens(coordinates))
            
            plt.plot(min_across_generations)
            plt.plot(mean_across_generations)
            plt.xlabel("Generation")
            plt.ylabel("Fitness")
            plt.suptitle("EggHolder Function using PSO")
            plt.title("The population size is "+str(population_size)+" and the number of generations is "+str(generation))
            plt.legend(["Minimum","Mean"])
            print("The minimum value at generation "+str(generation)+" is "+str(min_across_generations[-1]))
            print("The mean value at generation "+str(generation)+" is "+str(mean_across_generations[-1]))
            plt.show()
            