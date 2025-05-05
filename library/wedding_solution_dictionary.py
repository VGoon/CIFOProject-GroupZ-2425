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

        if repr:
            repr = self._validate_repr(repr)

        super().__init__(repr=repr)

    def _validate_repr(self, repr):
        # repr needs to be a dictionary
        if not isinstance(repr, dict):
            raise TypeError("Representation must be a dictionary.")
        
        # all the values in the repr need to be an int, if not - change to an int
        if not all(isinstance(person, int) for table in repr.values() for person in table):
            # repr = [int(person) for person in repr]
            repr = {tables: [int(person) for person in people] for tables, people in repr.items()}

        # the number of keys in repr need to be the same as the number of tables defined
        if len(repr.keys()) != self.tables:
            raise ValueError("The number of tables do not match the number of tables in the representation.")
        
        # there needs to be the same number of ppl at each table
        lengths = [len(lst) for lst in repr.values()]
        if not all(length == lengths[0] for length in lengths):
            raise ValueError("The number of people assigned to each table need to be the same.")
        
        # the length of all the attendees need to match the defined variable for attendees
        if len([val for sublist in repr.values() for val in sublist]) != self.attendees:
            raise ValueError("The total number of attendees in the representation need to match the defined number of attendees")
        
        # the number of unique values in the repr need to be the same number of attendees (for duplicates)
        if len(set([val for sublist in repr.values() for val in sublist])) != self.attendees:
            raise ValueError("There can be no duplicate attendees.")
        
        # there needs to be every value from 1 - the number of attendees (addressing the need for having the entire sequence)
        missing_attendees = set(range(1, self.attendees+1)) - set([val for sublist in repr.values() for val in sublist])
        if missing_attendees:
            raise ValueError("The representation is missing seating for the following people: ", missing_attendees)
        
        return repr

    # Override the superclass's methods
    def random_initial_representation(self):
        tables = {i: [] for i in range(1, self.tables + 1)}
        attendees_list = list(range(1, self.attendees+1))
        random.shuffle(attendees_list)

        table = 1
        while len(attendees_list) > 0:
            tables[table].append(attendees_list.pop())
            if len(tables[table]) == (self.attendees/self.tables):
                table += 1
                
        return tables


    def fitness(self):
        fitness = 0
        for i in range(1, self.tables+1): # loop through the tables
            table = self.repr[i]
            people_seen = []
            for personA in table: # loop through the people at the table 
                people_seen.append(personA) # make sure to skip personA's score with themself
                for personB in table: # compare person A with everyone else at the table
                    if personB not in people_seen: # skip the people that were already counted to not count them twice
                        fitness += self.values_grid[self.values_grid['idx'] == personA][str(personB)].values[0] 
        return fitness