from library.wedding_solution import Wedding_Solution

class WeddingGASolution(Wedding_Solution):
    def __init__(
        self,
        mutation_function,
        crossover_function,
        tables,
        attendees,
        #values_grid,
        values_grid = None,
        repr = None
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

    def fitness(self):
        # Check if the fitness has already been computed and cached
        if hasattr(self, '_fitness'):
            return self._fitness
        
        # If not, compute the fitness using the superclass's method and store it
        self._fitness = super().fitness()
        return self._fitness

    """
    def mutation(self, mut_prob):
        # Apply mutation function to representation
        new_repr = self.mutation_function(self.repr, mut_prob)
        # Create and return individual with mutated representation
        return WeddingGASolution(
            selection_function = self.selection_function,
            mutation_function=self.mutation_function,
            crossover_function=self.crossover_function,
            repr=new_repr
            
        )
    """

    def mutation(self, mut_prob):
        # Apply mutation function to representation, including fitness_grid
        new_repr = self.mutation_function(self.repr, mut_prob, self.values_grid)
        
        # Create and return individual with mutated representation
        return WeddingGASolution(
            mutation_function=self.mutation_function,
            crossover_function=self.crossover_function,
            tables=self.tables,
            attendees=self.attendees,
            values_grid=self.values_grid,
            repr=new_repr
        )

    def crossover(self, other_solution):
         # Apply crossover function to self representation and other solution representation
        offspring1_repr, offspring2_repr = self.crossover_function(self.repr, other_solution.repr)

        return (
            WeddingGASolution(
                mutation_function=self.mutation_function,
                crossover_function=self.crossover_function,
                tables=self.tables,
                attendees=self.attendees,
                values_grid=self.values_grid,
                repr=offspring1_repr
            ),
            WeddingGASolution(
                mutation_function=self.mutation_function,
                crossover_function=self.crossover_function,
                tables=self.tables,
                attendees=self.attendees,
                values_grid=self.values_grid,
                repr=offspring2_repr
            )
)

        
    """
    def crossover(self, other_solution):
        # Apply crossover function to self representation and other solution representation
        offspring1_repr, offspring2_repr = self.crossover_function(self.repr, other_solution.repr)

        # Create and return offspring with new representations
        return (
            WeddingGASolution(
                selection_function = self.selection_function,
                mutation_function=self.mutation_function,
                crossover_function=self.crossover_function,
                repr=offspring1_repr
            ),
            WeddingGASolution(
                selection_function = self.selection_function,
                mutation_function=self.mutation_function,
                crossover_function=self.crossover_function,
                repr=offspring2_repr
            )
        )
        """