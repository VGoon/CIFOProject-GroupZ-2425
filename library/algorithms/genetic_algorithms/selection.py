import random
from copy import deepcopy
from random import randint
from library.solution import Solution
import numpy as np

"""
def fitness_proportionate_selection(population: list[Solution], maximization: bool):
    if maximization:
        fitness_values = []
        for ind in population:
            if ind.fitness() < 0:
                # If fitness is negative (invalid solution like in Knapsack)
                # Set fitness to very small positive value
                # Probability of selecting this individual is nearly 0.
                fitness_values.append(0.0000001)
            else:
                fitness_values.append(ind.fitness())
    else:
        # Minimization: Use the inverse of the fitness value
        # Lower fitness should have higher probability of being selected
        fitness_values = [1 / ind.fitness() for ind in population]

    total_fitness = sum(fitness_values)
    # Generate random number between 0 and total
    random_nr = random.uniform(0, total_fitness)
    # For each individual, check if random number is inside the individual's "box"
    box_boundary = 0
    for ind_idx, ind in enumerate(population):
        box_boundary += fitness_values[ind_idx]
        if random_nr <= box_boundary:
            return deepcopy(ind)
"""


def fitness_proportionate_selection(population: list, maximization: bool):
    fitness_values = []

    for ind in population:
        # Use internal validator
        ind._validate_repr(ind.repr)

        fit = ind.fitness()

        # Reject invalid fitness values
        if fit < 0:
            raise ValueError(f"fitness_proportionate_selection- Invalid individual: negative fitness ({fit}) detected.")

        if maximization:
            fitness_values.append(fit) #if fit > 0 else 1e-7)
        else:
            fitness_values.append(1 / fit )#if fit > 0 else 1e-7)

    fitness_array = np.array(fitness_values)
    total_fitness = fitness_array.sum()

    selection_probs = fitness_array / total_fitness
    selected_index = np.random.choice(len(population), p=selection_probs)
    return deepcopy(population[selected_index])






def ranking_selection(population: list[Solution], maximization):
    # evalutate the fitness and get the total fitness
    total_fitness = 0
    fitness_list = [] # list of tuples (ind, fitness)
    for indiv in population:
        # Use internal validator
        indiv._validate_repr(indiv.repr)

        fitness = indiv.fitness()
        # Reject invalid fitness values
        if fitness < 0:
            raise ValueError(f"ranking selection - Invalid individual: negative fitness ({fitness}) detected.")
        
        fitness_list.append((indiv, fitness))
        total_fitness += fitness

    # sort by fitness (if max, sort in desc, otherwise, asc)
    if maximization:
        sorted(fitness_list, key=lambda x: x[1], reverse=True)
    else:   
        sorted(fitness_list, key=lambda x: x[1])
            
    # ranks will the the index in the list so index 0 will have rank 1
    # converting ranks to probabilities - the index of the rank list will match the index of the fitness_list
    rank_prob_list = []
    rank_summation = sum(list(range(1,65)))
    for index, indiv in enumerate(fitness_list):
        rank = index+1
        rank_prob = rank / rank_summation
        rank_prob_list.append(rank_prob)

    # select indiv
    selection = random.choices(fitness_list, weights=rank_prob_list)
    
    # print("Selected individual " + str(selection))
    selection[0][0].pretty_print()

    #return selection
    return deepcopy(selection[0][0])




def tournament_selection(population: list[Solution], maximization: bool, k: int = 3):
    # Ensure k is within bounds
    if k < 2:
        k = 2
    elif k > len(population):
        k = len(population)

    # Select k individuals using slicing logic like original version
    start_idx = randint(0, len(population) - k)
    end_idx = start_idx + k
    tourney_indivs = population[start_idx:end_idx]

    # Get fitness for selected individuals
    #fitness_list = [(ind, ind.fitness()) for ind in tourney_indivs]
    fitness_list = []
    for indiv in tourney_indivs:
        indiv._validate_repr(indiv.repr)  # Raise error if invalid
        fit = indiv.fitness()
        if fit < 0:
            raise ValueError(f"tornamente_selection - Invalid individual: negative fitness ({fit}) detected.")
        fitness_list.append((indiv, fit))

    # Select best (or worst) individual
    if maximization:
        selection = max(fitness_list, key=lambda x: x[1])
    else:
        selection = min(fitness_list, key=lambda x: x[1])

    # Uncomment for debugging
    # print(f"Tournament range: {start_idx}-{end_idx}")
    # selection[0].pretty_print()

    return selection[0]



"""
def tournament_selection(population: list[Solution], maximization):
    # randomly select the number of indivs to compare
    tourney_indivs_num = randint(2, int(len(population)/2)) # limiting range to half the population size
    tourney_indivs_start_idx = randint(0, len(population)-tourney_indivs_num)
    tourney_indivs_end_idx = tourney_indivs_start_idx + tourney_indivs_num
    tourney_indivs = population[tourney_indivs_start_idx:tourney_indivs_end_idx]

    # print("Range: " + str(tourney_indivs_start_idx) + " - " + str(tourney_indivs_end_idx))

    # get the subset's fitnesses
    fitness_list = [(ind, ind.fitness()) for ind in tourney_indivs]

    # select the best individual (if max, get the max(), otherwise, get the min())
    if maximization:
        selection = max(fitness_list, key=lambda x: x[1])
    else:
        selection = min(fitness_list, key=lambda x: x[1])

    # print("Selected individual " + str(selection))
    selection[0].pretty_print()
    
    return selection

"""