import random
from copy import deepcopy
from random import randint
# from library.solution import Solution


def cycle_crossover(parent1_repr, parent2_repr):
    start_idx = randint(0, len(parent1_repr)-1)
    # print("Start idx: " + str(start_idx))

    # Initialize the cycle with the starting index
    cycle_idxs = [start_idx]
    current_cycle_idx = start_idx

    tables1_dict = {}
    tables2_dict = {}
    for idx in range(0, len(parent1_repr)):

        # fill the tables per index for repr2
        if parent2_repr[idx] not in tables2_dict.keys():
            tables2_dict[parent2_repr[idx]] = [idx]
        else:
            tables2_dict[parent2_repr[idx]].append(idx)

        # fill the tables per index for repr1
        if parent1_repr[idx] not in tables1_dict.keys():
            tables1_dict[parent1_repr[idx]] = [idx]
        else:
            tables1_dict[parent1_repr[idx]].append(idx)

    # Traverse the cycle by following the mapping from parent2 to parent1
    while True:
        table_parent2 = parent2_repr[current_cycle_idx] #

        # Find where this value is in parent1 to get the next index in the cycle
        next_cycle_idx = random.choice(tables1_dict[table_parent2])
        # print("Chose idx #" + str(next_cycle_idx) + " from parent 2.")
        tables1_dict[table_parent2].remove(next_cycle_idx)

        # Closed the cycle -> Break
        if next_cycle_idx == start_idx:
            break

        cycle_idxs.append(next_cycle_idx)
        current_cycle_idx = next_cycle_idx

    offspring1_repr = []
    offspring2_repr = []
    for idx in range(len(parent1_repr)):
        if idx in cycle_idxs:
            # Keep values from parent1 in offspring1 in the cycle indexes
            offspring1_repr.append(parent1_repr[idx])
            # Keep values from parent2 in offspring2 in the cycle indexes
            offspring2_repr.append(parent2_repr[idx])
        else:
            # Swap elements from parents in non-cycle indexes
            offspring1_repr.append(parent2_repr[idx])
            offspring2_repr.append(parent1_repr[idx])

    # To keep the same type as the parents representation
    if isinstance(parent1_repr, str) and isinstance(parent2_repr, str):
        offspring1_repr = "".join(offspring1_repr)
        offspring2_repr = "".join(offspring2_repr)

    return offspring1_repr, offspring2_repr

def order_crossover(parent1_repr, parent2_repr):
    # seats_per_table = parent1_repr.count(1)
    attendee_length = len(parent1_repr)

    # limit the number of people that can be shuffled to at max 10
    if attendee_length < 10:
        limit = int(attendee_length / 2)
    else:
        limit = 10

    # choose a random number of people to get a subset
    numOfPeople = randint(2, limit) # cant invert 1 person, nothing would change - limiting to 10 indivs for less disruption

    startPerson = randint(0, attendee_length-numOfPeople) # set the biggest number it can randomly choose as the total - the number aimed to shuffle
    stopPerson = startPerson + numOfPeople

    # print("Number to keep: ", numOfPeople)
    # print("Range to keep: " + str(startPerson) + " - " + str(stopPerson))
    # print("------------")
    parent1_repr_substring = parent1_repr[startPerson:stopPerson]
    parent2_repr_substring = parent2_repr[startPerson:stopPerson]
    # print("Substring 1: " + str(parent1_repr_substring))
    # print("Substring 2: " + str(parent2_repr_substring))
    # print("------------")
    offspring1_repr, offspring2_repr = [-1] * attendee_length, [-1] * attendee_length
    offspring1_repr[startPerson:stopPerson] = parent1_repr_substring
    offspring2_repr[startPerson:stopPerson] = parent2_repr_substring

    parent1_remaining = deepcopy(parent1_repr)
    parent2_remaining = deepcopy(parent2_repr)

    parent1_remaining.reverse()
    for value in parent2_repr_substring:
        parent1_remaining.remove(value)
    parent1_remaining.reverse()

    parent2_remaining.reverse()
    for value in parent1_repr_substring:
        parent2_remaining.remove(value)
    parent2_remaining.reverse()

    # print("Remaining 1: " + str(parent1_remaining))
    # print("Remaining 2: " + str(parent2_remaining))

    # print("------------")
    offspring_idx = 0
    substring_idx = 0
    while offspring_idx < attendee_length:
        if offspring_idx == startPerson:
            offspring_idx += len(parent1_repr_substring)

        if offspring_idx >= attendee_length:
            continue

        offspring1_repr[offspring_idx] = parent2_remaining[substring_idx]
        offspring2_repr[offspring_idx] = parent1_remaining[substring_idx]
        # print("IDX: [" + str(offspring_idx) + "] - " + str(offspring1_repr))

        offspring_idx += 1
        substring_idx += 1

    return offspring1_repr, offspring2_repr

def partially_matched_crossover(parent1_repr, parent2_repr):
    size = len(parent1_repr)
    
    # Make sure both parents are valid permutations (no repeated elements)
    # assert len(set(parent1_repr)) == len(parent1_repr), "parent1 is not a valid permutation"
    # assert len(set(parent2_repr)) == len(parent2_repr), "parent2 is not a valid permutation"

    # Randomly choose two crossover points that define the window to be swapped
    # cx1 is the starting index, cx2 is the ending index (inclusive)
    cx1 = random.randint(0, size - 2)
    cx2 = random.randint(cx1 + 1, size - 1)
    # print(f"Crossover points: {cx1} to {cx2}")

    # Initialize offspring as empty lists (filled with None), same size as parents(by definition)    
    offspring1 = [None] * size
    offspring2 = [None] * size

    # Copy the segment (crossover window) from the opposite parent into each offspring
    # So offspring1 gets the window from parent2, and vice versa
    offspring1[cx1:cx2+1] = parent2_repr[cx1:cx2+1]
    offspring2[cx1:cx2+1] = parent1_repr[cx1:cx2+1]

    # These mappings are used to resolve conflicts when filling in the rest of the offspring
    # They link the values that were swapped between the parents in the crossover window
    # For example, if parent1 had 5 in the window and parent2 had 2 in the same position,
    # the mapping would record 2 → 5 and 5 → 2
    # This is important because when we try to fill a position in the offspring with a value
    # from the other parent, we might hit a conflict (i.e., the value is already present
    # in the copied window). If that happens, we follow this mapping to find an alternative
    # value that maintains the permutation without introducing duplicates
    mapping1 = {
        parent2_repr[i]: parent1_repr[i]
        for i in range(cx1, cx2 + 1)
    }
    mapping2 = {
        parent1_repr[i]: parent2_repr[i]
        for i in range(cx1, cx2 + 1)
    }

    # window1 keeps track of which values were already placed in the window copied into offspring1
    window1 = parent2_repr[cx1:cx2+1]
    
    # Fill in the rest of offspring1 with values from parent1 (outside the crossover window)
    for i in range(size):
        if cx1 <= i <= cx2:
            continue # Skip the window, if i is within the window range since it's already filled

        # Start by taking the value from parent1 at the current position, this is the 
        # value we want to place in offspring1 unless it causes a conflict with what's already in the
        # crossover window
        val = parent1_repr[i]
       
        # If the value is already in the copied window, follow the mapping to resolve conflict
        while val in window1:
            val = mapping1[val]
        # Otherwise, just copy the value from parent1 (val = parent1_repr[i])
        offspring1[i] = val

    # Do the same for offspring2, but using parent2 as the source and parent1's window (same logic as the previous chunk of code)
    window2 = parent1_repr[cx1:cx2+1]
    for i in range(size):
        if cx1 <= i <= cx2:
            continue
        val = parent2_repr[i]
        
        while val in window2:
            val = mapping2[val]
        offspring2[i] = val

    return offspring1, offspring2