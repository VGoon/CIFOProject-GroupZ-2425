from library.solution import Solution
import pandas as pd
from random import randint
import random
fitness_grid = pd.read_csv("library/wedding_seat_data.csv")

class Wedding_Solution(Solution):
    def __init__(self, repr=None, tables=8, attendees=64, values_grid=fitness_grid):
        self.tables = tables
        self.attendees = attendees
        self.values_grid = values_grid
        self.seats_per_table = int(attendees / tables)

        if repr:
            repr = self._validate_repr(repr)

        super().__init__(repr=repr)

    # only used to validate the given representation (random initialization already follows these rules)
    def _validate_repr(self, repr):
        # repr needs to be a dictionary
        if not isinstance(repr, list):
            raise TypeError("Representation must be a list.")
        
        # this ensures that the partitions are always even and the same amounts
        if not (self.attendees / self.tables).is_integer():
            raise ValueError("The number of attendees and tables for this solution must divide evenly into each other.")
        
        # all the values in the repr need to be an int, if not - change to an int
        if not all([isinstance(table_num, int) for table_num in repr]):
            repr = [int(table) for table in repr]

        # the number of unique numbers in repr need to be the same as the number of tables defined
        if len(set(repr)) != self.tables:
            raise ValueError("Missing a table number from representation assignment: Table(s)", set(range(1,self.tables+1)) - set(repr))
        
        # there needs to be the same number of ppl at each table
        if not all(repr.count(x) == self.seats_per_table for x in range(1,self.tables)):
            raise ValueError("The number of people assigned to each table need to be the same.")
        
        # the length of all the attendees need to match the defined variable for attendees
        if len(repr) != self.attendees:
            raise ValueError("The total number of attendees in the representation need to match the defined number of attendees")
        
        return repr

    # Override the superclass's methods
    def random_initial_representation(self):
        seats = []
        for i in range(1,self.tables+1): # generates the same number of numbers in a row ([1] * 5 = [1,1,1,1,1])
            seats = seats + [i] * self.seats_per_table
        random.shuffle(seats) # randomly assign tables to participants
        return seats

    # returns the fitness of the representation / solution
    def fitness(self):
        fitness = 0
        for table_num in range(1, self.tables+1): # loop through the tables
            fitness += self.table_fitness(table_num)

        return fitness
    
    # checks the fitness of a specific table instead of all the tables
    def table_fitness(self, table):
        fitness = 0
        table_seats = [i for i, x in enumerate(self.repr) if x == table]
        table_seats = [x + 1 for x in table_seats] # add 1 to everything to match the fitness grid
        people_seen = []
        for personA in table_seats: # loop through the people at the table 
            people_seen.append(personA) # make sure to skip personA's score with themself
            for personB in table_seats: # compare person A with everyone else (personB) at the table
                if personB not in people_seen: # skip the people that were already counted to not count them twice
                    fitness += self.values_grid[self.values_grid['idx'] == personA][str(personB)].values[0]
        return fitness
    
    def get_valued_people(self, person):
        filtered = fitness_grid[fitness_grid['idx'] == person].iloc[0]
        filtered = filtered.drop('idx')
        peopleWithRelationship = [int(x) for x in filtered[filtered > 0].index] # only getting the attendees that are valued by randomPersonA
        return peopleWithRelationship
        
    # clearly shows which person sits at which table for debugging purposes
    def pretty_print(self):
        tables = {i: [] for i in range(1, self.tables+1)}  # Tables 1 through 8

        for idx, table in enumerate(self.repr):
            tables[table].append(idx)

        print("----------SEATING ARRANGEMENTS----------")
        for table_num in range(1, self.tables+1): 
            # checks to see if its single digit - if so, add a space for cleaner reading
            # also adds 1 so that it is clear which person is being referred to
            indices = [f"{i+1:2}" for i in tables[table_num]]
            print(f"Table {table_num}: [{', '.join(indices)}]")
        print("----------------------------------------")