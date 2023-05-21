import numpy as np
import matplotlib.pyplot as plt
import random
CrP = 0.8

def HolderTableFunction(x,y):
     return -1*abs(np.sin(x)*np.cos(y)*np.exp(abs(1-(np.sqrt(x*x+y*y)/np.pi))))

#Gives most minimum value of the function attained in given generation
def min_across_gens(Coordinates,population_size):
    min_value = HolderTableFunction(Coordinates[0][0],Coordinates[0][1])
    for i in range(population_size):
        value = HolderTableFunction(Coordinates[i][0],Coordinates[i][1])
        if value < min_value:
            min_value = value
    return min_value

#Gives mean value of the function attained in given generation
def mean_across_gens(Coordinates,population_size):
    mean_value = 0
    for i in range(population_size):
        mean_value += HolderTableFunction(Coordinates[i][0],Coordinates[i][1])
    
    mean_value/=population_size
    return mean_value

#Creates a mutant vector of given vector
def Generate_mutant(sel_cor,coordinates,F):
    r1 =int(random.uniform(0,population_size-1))
    r2 = int(random.uniform(0,population_size-1))
    r3 = int(random.uniform(0,population_size-1))
    x_mutant = sel_cor[0]
    y_mutant = sel_cor[1]
    x_mutant += 0.5*(coordinates[r1][0] - coordinates[j][0])+F*(coordinates[r2][0] - coordinates[r3][0])
    y_mutant += 0.5*(coordinates[r1][1] - coordinates[r2][1])+F*(coordinates[r2][1] - coordinates[r3][1])
    new_coordinates = [x_mutant,y_mutant]
    return new_coordinates

#Creates a trial vector of a given vector and its mutant vector
def Trial(x,y,x_mutant,y_mutant):
    probx = random.uniform(0,1)
    proby = random.uniform(0,1)
    if probx < CrP:
         x = x_mutant
    if proby < CrP:
         y = y_mutant
    return [x,y]

#To check if the new coordinates are within the constraints
def Evaluate_constraints(x,y):
    if x > 10 or x < -10:
         return False
    elif y > 10 or y < -10:
         return False
    
    return True

#Returns true if all the coordinates are the same
def converged_or_not(coordinates):
    for i in range(population_size):
        if coordinates[i][0] != coordinates[i][1]:
            return False
    return True

if __name__ == '__main__':
    generations = [50,100,200]
    population_sizes = [20,50,100,200]

    for generation in generations:
        for population_size in population_sizes:
            plt.clf()
            coordinates = []
            mean_across_generations = []
            min_across_generations = []
            for i in range(0,population_size):
                    #Candidate i is generated randomly
                    x = random.uniform(-10, 10)
                    y = random.uniform(-10, 10)
                    coordinates.append([x,y])
            for i in range(0,generation):
                F = random.uniform(-2,2)
                for j in range(population_size):
                    #Mutant j is generated randomly and then trial is done with the mutant and the candidate j.
                    mutant_coordinates = Generate_mutant(coordinates[j],coordinates,F)
                    trial_coordinates = Trial(x,y,mutant_coordinates[0],mutant_coordinates[1])
                    # If the trial is successful, then the mutant is replaced with the trial.
                    # If the trial is not successful, then the mutant is not replaced. 
                    if Evaluate_constraints(trial_coordinates[0],trial_coordinates[1]):
                        if(HolderTableFunction(trial_coordinates[0],trial_coordinates[1]) < HolderTableFunction(coordinates[j][0],coordinates[j][1])):
                            coordinates[j] = trial_coordinates
                    else:
                        j-=1
                #Breaks if all the coordinates are the same
                if(converged_or_not(coordinates)):
                    break
                min_across_generations.append(min_across_gens(coordinates,population_size))
                mean_across_generations.append(mean_across_gens(coordinates,population_size))
            plt.plot(min_across_generations)
            plt.plot(mean_across_generations)
            plt.xlabel("Generation")
            plt.ylabel("Fitness")
            plt.suptitle("HolderTable Function")
            plt.title("The population size is "+str(population_size)+" and the number of generations is "+str(generation))
            plt.legend(["Minimum","Mean"])
            print("The minimum value at generation "+str(generation)+" is "+str(min_across_generations[-1]))
            print("The mean value at generation "+str(generation)+" is "+str(mean_across_generations[-1]))
            plt.show()
            