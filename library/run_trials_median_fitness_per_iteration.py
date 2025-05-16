import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd
import time
from datetime import datetime
import os
import numpy as np


from library.algorithms.hc_sa.hill_climbing import hill_climbing
from library.algorithms.hc_sa.simulated_annealing import simulated_annealing
from library.algorithms.genetic_algorithms.genetic_algorithm import genetic_algorithm
from library.algorithms.hc_sa.wedding_sa_hc_solutions import Wedding_HillClimbingSolution, Wedding_SimulatedAnnealingSolution
from library.wedding_ga_solution import WeddingGASolution
from library.wedding_solution import Wedding_Solution

from library.algorithms.hc_sa.neighborhoods import random_swap_neighborhood, greedy_swap_neighborhood
import pandas as pd
fitness_grid = pd.read_csv("library/wedding_seat_data.csv")

# Import required for the selection, crossover, and mutation functions going to be uses in the GAs algorithms
from library.algorithms.genetic_algorithms.selection import fitness_proportionate_selection, ranking_selection, tournament_selection
from library.algorithms.genetic_algorithms.crossover import cycle_crossover, order_crossover, modified_partially_matched_crossover
from library.algorithms.genetic_algorithms.mutation import greedy_swap_mutation, scramble_mutation, inversion_mutation, tableswap_mutation


# Compute the median fitness across all trials at each iteration
def run_trials_median_fitness_per_iteration(
    
        optimization_algo = "HC",
        neighborhood_function=random_swap_neighborhood, 
        trials=10, 
        max_iter=100,
        maximization=True,
        verbose=True,
        folder_path=None,

        #Specific for SA
        C = 100,
        L = 10,
        H = 1.01,

        # Specific for GA
        mutation_function=greedy_swap_mutation,
        crossover_function=cycle_crossover,
        selection_algorithm=fitness_proportionate_selection,
        pop_size=50,
        xo_prob=0.8,
        mut_prob=0.2,
        elitism=True
        ):
    
        

    """
    Run multiple trials of the simulated annealing algorithm with different initial solutions.

    Parameters:
        neighborhood_function (function): The neighborhood function to use.
        trials (int): The number of trials to run.

    Returns:
        list: A list of best solutions from each trial.
    """
    all_fitness_histories = []
    best_solutions = []
    trial_durations = []
    # Defining the mutation function name
    if mutation_function == greedy_swap_mutation:
        mutation_function_name = "greedy_swap_mutation"
    elif mutation_function == scramble_mutation:
        mutation_function_name = "scramble_mutation"
    elif mutation_function == inversion_mutation:
        mutation_function_name = "inversion_mutation"
    elif mutation_function == tableswap_mutation:
        mutation_function_name = "tableswap_mutation"

    # Defining the crossover function name
    if crossover_function == cycle_crossover:
        crossover_function_name = "cycle_crossover"
    elif crossover_function == modified_partially_matched_crossover:
        crossover_function_name = "modified_partially_matched_crossover"
    elif crossover_function == order_crossover:
        crossover_function_name = "order_crossover"

    # Defining the selection function name
    if selection_algorithm == fitness_proportionate_selection:
        selection_algorithm_name = "fitness_proportionate_selection"
    elif selection_algorithm == ranking_selection:
        selection_algorithm_name = "ranking_selection"
    elif selection_algorithm == tournament_selection:
        selection_algorithm_name = "tournament_selection"

    # Defining the neighborhood function name
    if neighborhood_function == random_swap_neighborhood:
        neighborhood_function_name = "random_swap_neighborhood"
    elif neighborhood_function == greedy_swap_neighborhood:
        neighborhood_function_name = "greedy_swap_neighborhood"

    # Generate a new folder to store the results obtained from the trials
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if folder_path is None:
        if optimization_algo == "GA":
            folder_path = f"ModelResults/{optimization_algo}/Trial_results_{mutation_function_name}_{crossover_function_name}_{selection_algorithm_name}"

        else:
            folder_path = f"ModelResults/{optimization_algo}/Trial_results_{neighborhood_function_name}"


    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    if optimization_algo == "SA":
        for i in range(trials):
            start_time = time.time()
            print(f"Trial {i + 1}/{trials}")
            sa_solution = Wedding_SimulatedAnnealingSolution(
                neighborhood_function=neighborhood_function,
                pretty_print_msg=f"Trial {i + 1} random swap SA solution"
            )

            best_solution, trial_fitness_history,iter = simulated_annealing(
                initial_solution=sa_solution,
                maximization=maximization,
                verbose=verbose,
                max_iter=max_iter,
                C= C,
                L=L,
                H=H
            )
            end_time = time.time()
            trial_durations.append(round(end_time - start_time, 2))  # seconds
            print(f"Trial duration: {trial_durations[-1]} seconds")
            print ("Number of iterations: ", iter)
            print(f"Neighborhood: {neighborhood_function.__name__}")
            print(f"Best solution fitness: {best_solution.fitness()}")
            best_solutions.append(best_solution)
            all_fitness_histories.append(trial_fitness_history)
    

    elif optimization_algo == "HC": 
        for i in range(trials):
            start_time = time.time()
            print(f"Trial {i + 1}/{trials}")
            hc_solution = Wedding_HillClimbingSolution(
                neighborhood_function=neighborhood_function,
                pretty_print_msg=f"Trial {i + 1} random swap HC solution"
            )

            best_solution, trial_fitness_history, iter = hill_climbing(
                initial_solution=hc_solution,
                maximization=maximization,
                verbose=verbose,
                max_iter=max_iter
            )
            end_time = time.time()
            trial_durations.append(round(end_time - start_time, 2)) 
            print(f"Trial duration: {trial_durations[-1]} seconds")

            print ("Number of iterations: ", iter)
            print(f"Neighborhood: {neighborhood_function.__name__}")
            print(f"Best solution fitness: {best_solution.fitness()}")
            best_solutions.append(best_solution)
            all_fitness_histories.append(trial_fitness_history)


    elif optimization_algo == "GA":
        for i in range(trials):
            start_time = time.time()
            print(f"Trial {i + 1}/{trials}")
            ga_initial_population = [WeddingGASolution(
            mutation_function=mutation_function,
            crossover_function=crossover_function,
            tables=8,  
            attendees=64,  
            values_grid=fitness_grid  
        ) for _ in range(pop_size)]

            best_solution, trial_fitness_history, gen = genetic_algorithm(
                initial_population=ga_initial_population,
                maximization=maximization,
                verbose=verbose,
                max_gen=max_iter,
                selection_algorithm=selection_algorithm,
                xo_prob=xo_prob,
                mut_prob=mut_prob,
                elitism=elitism,
            )
            end_time = time.time()
            trial_durations.append(round(end_time - start_time, 2))
            print(f"Trial duration: {trial_durations[-1]} seconds")
            print ("Number of generations: ", gen)
            print(f"Mutation: {mutation_function.__name__}, Crossover: {crossover_function.__name__}, Selection: {selection_algorithm.__name__}")
            print(f"Best solution fitness: {best_solution.fitness()}")
            best_solutions.append(best_solution)
            all_fitness_histories.append(trial_fitness_history)



    else:
        raise ValueError("Invalid optimization algorithm. Choose 'SA', 'HC', or 'GA'.")



    # Compute the median fitness across all trials at each iteration
    # if we have a = [[1, 2, 3], [2, 3, 4], [3, 4, 5]] when we do medians = [sum(col) / len(col) for col in zip(*a)] 
    # [round(np.median(col), 2) for col in zip(*all_fitness_histories)
    # we get this [2.0, 3.0, 4.0]


    """
    Notes
    When computing the median fitness per iteration across multiple trials, we may encounter
    fitness histories (lists) of different lengths. This happens when the optimization algorithm 
    (concretely Hill Climbing) converges early — i.e., stops before reaching the max number of iterations.

    If we don't handle this, using zip(*all_fitness_histories) will truncate to the shortest list,
    which would result in misleading medians and incomplete plots.

    Solution:
    To make all fitness histories the same length, we pad the shorter ones by repeating their final
    fitness value until they reach the length of the longest history. This ensures consistent averaging
    across all iterations.
    """
    # Please note that the median_fitness_per_iteration is only used for plotting the results
    # Since we will no longer plot the results for SA and HC we will just pad the fitness histories to not get an error
    # But variable won't be used
    if optimization_algo in ["SA", "HC"]:
        # Pad shorter histories to match the longest one
        max_len = max(len(hist) for hist in all_fitness_histories)
        for hist in all_fitness_histories:
            if len(hist) < max_len:
                hist.extend([hist[-1]] * (max_len - len(hist)))


    median_fitness_per_iteration = [round(np.median(col), 2) for col in zip(*all_fitness_histories)]


    if optimization_algo == "GA":
        # Plot the results
        plt.figure(figsize=(10, 5))
        plt.plot(median_fitness_per_iteration, label='Median Best Fitness per Generation')
        plt.xlabel('Generation')
        plt.ylabel('Median Best Fitness')
        plt.title('Median Best Fitness per Generation)')
        plt.legend()

        # Remove grid and set integer ticks on x-axis
        plt.grid(False)
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.tight_layout()
        plt.show()


    # Save the results to a CSV file
    # Save best solutions to a CSV file
    best_fitness_values = [sol.fitness() for sol in best_solutions]
    pd.DataFrame(best_fitness_values, columns=["Fitness"]).to_csv(os.path.join(folder_path, f"best_solutions_{timestamp}.csv"), index=False)

    # Save all fitness histories to a CSV file
    all_fitness_histories_df = pd.DataFrame(all_fitness_histories)
    all_fitness_histories_df.to_csv(os.path.join(folder_path, f"all_fitness_histories_{timestamp}.csv"), index=False)

    # Save median fitness per iteration to a CSV file
    pd.DataFrame(median_fitness_per_iteration, columns=["MedianFitness"]).to_csv(os.path.join(folder_path, f"median_fitness_per_iteration_{timestamp}.csv"), index=False)

    # Save the trial durations to a CSV file
    pd.DataFrame(trial_durations, columns=["TrialDurations"]).to_csv(os.path.join(folder_path, f"trial_durations_{timestamp}.csv"), index=False)


    return best_solutions, all_fitness_histories, median_fitness_per_iteration, trial_durations
    # the best_solutions is a list of instances of best solutions and not the fitness of the best solutions
    # the all_fitness_histories is a list of lists of fitnesses