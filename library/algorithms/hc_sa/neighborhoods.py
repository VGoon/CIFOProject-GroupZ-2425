from random import randint, choice
from copy import deepcopy
from library.wedding_solution import Wedding_Solution


def random_swap_neighborhood(repr, get_valued_people=None, num_of_neighbors=64, attendees=64):
    neighbors = []
    attendees = len(repr)

    # loop through all the attendees and swap them at least once
    for personA in range(1, attendees+1):
        tableA = repr[personA - 1]

        randomPersonB = randint(1, attendees)

        randomTableB = repr[randomPersonB - 1]

        # find a random person to swap with that doesnt sit at the same table
        while randomTableB == tableA:
            randomPersonB = randint(1, attendees)
            randomTableB = repr[randomPersonB - 1]

        # swap personA and personB
        new_repr = deepcopy(repr)
        new_repr[personA - 1] = randomTableB
        new_repr[randomPersonB - 1] = tableA

        debug_print = "Swapped person #" + str(personA) + " at table " + str(tableA) + " with person #" + str(randomPersonB) + " at table " + str(randomTableB)

        # Validation step
        try:
            _ = Wedding_Solution(repr=new_repr, values_grid=None)
        except Exception as e:
            raise ValueError(f"random_swap_neighborhood - Invalid representation in mutation: {e}")

        # add to the list of neighbors
        neighbors.append((new_repr,debug_print))

    # Returns list of representations of neighbors
    return neighbors

def greedy_swap_neighborhood(repr, get_valued_people, attendees=64):

    """
    Generates neighbors by greedily swapping a random person with others they have relationships with.

    Parameters:
        repr (list): The current representation of seating.
        get_valued_people (function): A function that returns a list of people with valued relationships to a given person.
        attendees (int): Total number of attendees.

    Returns:
        list of tuples: Each tuple contains (new_repr, debug_msg).
    """
    neighbors = []

    # Select a random person A
    randomPersonA = randint(1, attendees)
    randomTableA = repr[randomPersonA - 1]

    # Get people who have a relationship with A
    peopleWithRelationship = get_valued_people(randomPersonA)

    for personB in peopleWithRelationship:
        tableB = repr[personB - 1]
        while tableB == randomTableA:
            personB = randint(1, attendees)
            tableB = repr[personB - 1]

        new_repr = deepcopy(repr)
        new_repr[randomPersonA - 1] = tableB
        new_repr[personB - 1] = randomTableA

        debug_msg = f"Swapped person #{randomPersonA} at table {randomTableA} with person #{personB} at table {tableB}"
        neighbors.append((new_repr, debug_msg))

    # Fallback: if no neighbors were created
    if not neighbors:
        randomPersonA = randint(1, attendees)
        randomTableA = repr[randomPersonA - 1]

        randomPersonB = randint(1, attendees)
        randomTableB = repr[randomPersonB - 1]
        while randomTableB == randomTableA:
            randomPersonB = randint(1, attendees)
            randomTableB = repr[randomPersonB - 1]

        new_repr = deepcopy(repr)
        new_repr[randomPersonA - 1] = randomTableB
        new_repr[randomPersonB - 1] = randomTableA

        debug_msg = f"Swapped person #{randomPersonA} at table {randomTableA} with person #{randomPersonB} at table {randomTableB}"
        # Validation step
        try:
            _ = Wedding_Solution(repr=new_repr, values_grid=None)
        except Exception as e:
            raise ValueError(f"random_swap_neighborhood - Invalid representation in mutation: {e}")
        
        neighbors.append((new_repr, debug_msg))

    return neighbors



def greedy_swap_neighborhood(repr, get_valued_people, attendees=64):
    neighbors = []

    # Select random person A and their table
    randomPersonA = randint(1, attendees)
    randomTableA = repr[randomPersonA - 1]

    # Get people person A has a relationship with
    peopleWithRelationship = get_valued_people(randomPersonA)

    for personB in peopleWithRelationship:
        tableB = repr[personB - 1]

        # Make sure personB is from a different table
        while tableB == randomTableA:
            personB = randint(1, attendees)
            tableB = repr[personB - 1]

        # Get everyone from randomTableA, except randomPersonA
        table_seats = [i + 1 for i, x in enumerate(repr) if x == randomTableA]
        if randomPersonA in table_seats:
            table_seats.remove(randomPersonA)

        # If table_seats is empty (very rare), skip this iteration
        if not table_seats:
            continue

        # Pick personC from the same table as personA (not personA)
        randomPersonC = choice(table_seats)

        # Perform the swap
        new_repr = deepcopy(repr)
        new_repr[randomPersonC - 1] = tableB
        new_repr[personB - 1] = randomTableA

        debug_msg = (
            f"Swapped personC #{randomPersonC} at table {randomTableA} with "
            f"personB #{personB} at table {tableB} for personA #{randomPersonA}"
        )

        neighbors.append((new_repr, debug_msg))

    # Fallback: if no neighbors were created
    if not neighbors:
        A = randint(1, attendees)
        tableA = repr[A - 1]

        B = randint(1, attendees)
        tableB = repr[B - 1]
        while tableB == tableA:
            B = randint(1, attendees)
            tableB = repr[B - 1]

        new_repr = deepcopy(repr)
        new_repr[A - 1] = tableB
        new_repr[B - 1] = tableA

        debug_msg = f"Random swapped person #{A} at table {tableA} with person #{B} at table {tableB}"
        neighbors.append((new_repr, debug_msg))

    return neighbors
