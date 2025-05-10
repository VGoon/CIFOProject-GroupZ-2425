import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from library.algorithms.hc_sa.hill_climbing import hill_climbing
from library.algorithms.hc_sa.simulated_annealing import simulated_annealing
from library.wedding_solution import Wedding_Solution
from library.algorithms.hc_sa.wedding_sa_hc_solutions import Wedding_HillClimbingSolution, Wedding_SimulatedAnnealingSolution

from library.algorithms.hc_sa.neighborhoods import random_swap_neighborhood, actual_greedy_swap_neighborhood

# Compute the average fitness across all trials at each iteration
def run_trials_avg_fitness_per_iteration(
        optimization_algo = "HC",
        neighborhood_function=random_swap_neighborhood, 
        trials=10, 
        max_iter=100,
        maximization=True,
        verbose=True,

        #Specific for SA
        C = 100,
        L = 10,
        H = 1.01
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

    if optimization_algo == "SA":
        for i in range(trials):
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
            print ("Number of iterations: ", iter)
            best_solutions.append(best_solution)
            all_fitness_histories.append(trial_fitness_history)
    

    else: #optimization_algo == "HC":
        for i in range(trials):
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
            print ("Number of iterations: ", iter)
            best_solutions.append(best_solution)
            all_fitness_histories.append(trial_fitness_history)


    # Compute the average fitness across all trials at each iteration
    # if we have a = [[1, 2, 3], [2, 3, 4], [3, 4, 5]] when we do averages = [sum(col) / len(col) for col in zip(*a)] 
    # we get this [2.0, 3.0, 4.0]


    """
    Notes
    When computing the average fitness per iteration across multiple trials, we may encounter
    fitness histories (lists) of different lengths. This happens when the optimization algorithm 
    (concretely Hill Climbing) converges early — i.e., stops before reaching the max number of iterations.

    If we don't handle this, using zip(*all_fitness_histories) will truncate to the shortest list,
    which would result in misleading averages and incomplete plots.

    Solution:
    To make all fitness histories the same length, we pad the shorter ones by repeating their final
    fitness value until they reach the length of the longest history. This ensures consistent averaging
    across all iterations.
    """
    # Pad shorter histories to match the longest one
    max_len = max(len(hist) for hist in all_fitness_histories)
    for hist in all_fitness_histories:
        if len(hist) < max_len:
            hist.extend([hist[-1]] * (max_len - len(hist)))


    avg_fitness_per_iteration = [round(sum(col) / len(col), 2) for col in zip(*all_fitness_histories)]

    # Plot the results
    plt.figure(figsize=(10, 5))
    plt.plot(avg_fitness_per_iteration, label='Average Fitness per Iteration')
    plt.xlabel('Iteration')
    plt.ylabel('Average Fitness')
    plt.title('Average Fitness per Iteration)')
    plt.legend()

    # Remove grid and set integer ticks on x-axis
    plt.grid(False)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()
    plt.show()


    return best_solutions, all_fitness_histories, avg_fitness_per_iteration
    # the best_solutions is a list of instances of best solutions and not the fitness of the best solutions
    # the all_fitness_histories is a list of lists of fitnesses