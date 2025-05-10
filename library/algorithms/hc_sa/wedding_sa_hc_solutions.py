from  library.wedding_solution import Wedding_Solution
import pandas as pd
import random
df = pd.read_csv("library/wedding_seat_data.csv")


class Wedding_HillClimbingSolution(Wedding_Solution):
    def __init__(self, repr=None, tables=8, attendees=64, values_grid=df, pretty_print_msg=None, neighborhood_function=None):
        if not pretty_print_msg:
            self.pretty_print_msg = "Initial Solution."
        else:
            self.pretty_print_msg = pretty_print_msg

        super().__init__(
            tables=tables,
            attendees=attendees,
            values_grid=values_grid,
            repr=repr
        )
        self.neighborhood_function = neighborhood_function

    
    def get_neighbors(self):

        # Receives the representation of the current solution and generates a list of the neighbors representations
        # Includes the get_valued_people parameter to get the valued people 
        repr_neighbors = self.neighborhood_function(self.repr, get_valued_people=self.get_valued_people)
        #repr_neighbors = self.neighborhood_function(self.repr)


        
        # For each neighbor representation, create a new Wedding_HillClimbingSolution object
        return [
            Wedding_HillClimbingSolution(
                repr=neighbor_repr,
                tables=self.tables,
                attendees=self.attendees,
                values_grid=self.values_grid,
                neighborhood_function=self.neighborhood_function,
                pretty_print_msg=debug_msg
            )
            for neighbor_repr, debug_msg in repr_neighbors
        ]

    def pretty_print(self):
        return "Final seating: " + str(self.repr) + "\nFitness: " + str(self.fitness())




class Wedding_SimulatedAnnealingSolution(Wedding_Solution):
    def __init__(self, repr=None, tables=8, attendees=64, values_grid=df, pretty_print_msg=None, neighborhood_function=None):
        if not pretty_print_msg:
            self.pretty_print_msg = "Initial Solution."
        else:
            self.pretty_print_msg = pretty_print_msg

        super().__init__(
            tables=tables,
            attendees=attendees,
            values_grid=values_grid,
            repr=repr
        )

        self.neighborhood_function = neighborhood_function

    def pretty_print(self):
        return self.pretty_print_msg + "\nFitness: " + str(self.fitness())

    def get_random_neighbor(self):
        """Get a random neighbor using the neighborhood function (returning representations), and wrap it as an instance."""
        # Get list of (repr, debug_msg) pairs
        neighbors = self.neighborhood_function(self.repr, get_valued_people=self.get_valued_people)

        if not neighbors:
            return self  # fallback: no neighbors, return self

        # Randomly choose one neighbor's representation and message
        neighbor_repr, debug_msg = random.choice(neighbors)

        # Wrap it as a new instance of this class
        return Wedding_SimulatedAnnealingSolution(
            repr=neighbor_repr,
            tables=self.tables,
            attendees=self.attendees,
            values_grid=self.values_grid,
            neighborhood_function=self.neighborhood_function,
            pretty_print_msg=debug_msg
        )
