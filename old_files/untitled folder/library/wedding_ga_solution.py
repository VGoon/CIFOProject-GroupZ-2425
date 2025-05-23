from library.wedding_solution import Wedding_Solution
import pandas as pd
fitness_grid = pd.read_csv("library/wedding_seat_data.csv")

class WeddingGASolution(Wedding_Solution):
    def __init__(
        self,
        mutation_function,
        crossover_function,
        repr=None, 
        tables=8, 
        attendees=64, 
        values_grid=fitness_grid
    ):
        # Save as attributes for access in methods
        self.mutation_function = mutation_function
        self.crossover_function = crossover_function

        super().__init__(
            repr=repr,
            tables=tables,
            attendees=attendees,
            values_grid=values_grid,
        )

    def mutation(self, mut_prob):
        # Apply mutation function to representation
        new_repr = self.mutation_function(self.repr, mut_prob)
        # Create and return individual with mutated representation
        return WeddingGASolution(
            mutation_function=self.mutation_function,
            crossover_function=self.crossover_function,
            repr=new_repr
        )

    def crossover(self, other_solution):
        # Apply crossover function to self representation and other solution representation
        offspring1_repr, offspring2_repr = self.crossover_function(self.repr, other_solution.repr)

        # Create and return offspring with new representations
        return (
            WeddingGASolution(
                mutation_function=self.mutation_function,
                crossover_function=self.crossover_function,
                repr=offspring1_repr
            ),
            WeddingGASolution(
                mutation_function=self.mutation_function,
                crossover_function=self.crossover_function,
                repr=offspring2_repr
            )
        )