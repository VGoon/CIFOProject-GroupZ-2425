import random
from copy import deepcopy
from random import randint
# from library.solution import Solution
import pandas as pd
fitness_grid = pd.read_csv("library/wedding_seat_data.csv")

# make it genuinly greedy by starting to make personB the max of the ppl with relationships (sort descending)
def greedy_swap_mutation(representation, mut_prob, fitness_grid):
    new_repr = deepcopy(representation)
    attendees_num = len(representation)

    # random chance to do the mutation
    if random.random() > mut_prob:
        print("Randomly chosen to not implement greedy_swap_mutation.")
        return new_repr

    # selects random different tables to swap from, 
    randomPersonA = randint(1, attendees_num)
    randomTableA = new_repr[randomPersonA-1]

    # get positivley valued neighbors
    filtered = fitness_grid[fitness_grid['idx'] == randomPersonA].iloc[0]
    filtered = filtered.drop('idx')
    peopleWithRelationship = [int(x) for x in filtered[filtered > 0].index] # only getting the attendees that are valued by randomPersonA
    peopleWithRelationship = sorted(peopleWithRelationship, reverse=True)

    # determine person B (don't choose someone from the same table)
    randomPersonB = None
    for personB in peopleWithRelationship:
        randomPersonB = personB
        randomTableB = new_repr[personB-1]
        if randomTableA == randomTableB:
            continue
        else:
            break

    # if there are no values people that don't share the same table as A, randomly choose B
    if randomPersonB == None:
        randomPersonB = randint(1, attendees_num)
        randomTableB = new_repr[randomPersonB-1]
        while randomTableB == randomTableA: # always choose a different table
            randomPersonB = randint(1, attendees_num)
            randomTableB = new_repr[randomPersonB-1]

    # select someone random from tableA thats not randomPersonA
    # get everyone from randomTableA
    tableA_seats = [i for i, x in enumerate(new_repr) if x == randomTableA]
    tableA_seats = [x + 1 for x in tableA_seats] # add 1 to everything to match the fitness grid
    tableA_seats.remove(randomPersonA) # remove personA from the list
    randomPersonC = random.choice(tableA_seats)

    # Swap the two people between the tables
    new_repr[randomPersonC-1] = randomTableB
    new_repr[randomPersonB-1] = randomTableA

    # print("Swapped personC #" + str(randomPersonC) + " at table " + str(randomTableA) + " with personB #" + str(personB) + " at table " + str(randomTableB) + " for personA #" + str(randomPersonA))
import random
from copy import deepcopy
from random import randint
# from library.solution import Solution
import pandas as pd
fitness_grid = pd.read_csv("library/wedding_seat_data.csv")

# make it genuinly greedy by starting to make personB the max of the ppl with relationships (sort descending)
def greedy_swap_mutation(representation, mut_prob, fitness_grid):
    new_repr = deepcopy(representation)
    attendees_num = len(representation)

    # random chance to do the mutation
    if random.random() > mut_prob:
        print("Randomly chosen to not implement greedy_swap_mutation.")
        return new_repr

    # selects random different tables to swap from, 
    randomPersonA = randint(1, attendees_num)
    randomTableA = new_repr[randomPersonA-1]

    # get positivley valued neighbors
    filtered = fitness_grid[fitness_grid['idx'] == randomPersonA].iloc[0]
    filtered = filtered.drop('idx')
    peopleWithRelationship = [int(x) for x in filtered[filtered > 0].index] # only getting the attendees that are valued by randomPersonA
    peopleWithRelationship = sorted(peopleWithRelationship, reverse=True)

    # determine person B (don't choose someone from the same table)
    randomPersonB = None
    for personB in peopleWithRelationship:
        randomPersonB = personB
        randomTableB = new_repr[personB-1]
        if randomTableA == randomTableB:
            continue
        else:
            break

    # if there are no values people that don't share the same table as A, randomly choose B
    if randomPersonB == None:
        randomPersonB = randint(1, attendees_num)
        randomTableB = new_repr[randomPersonB-1]
        while randomTableB == randomTableA: # always choose a different table
            randomPersonB = randint(1, attendees_num)
            randomTableB = new_repr[randomPersonB-1]

    # select someone random from tableA thats not randomPersonA
    # get everyone from randomTableA
    tableA_seats = [i for i, x in enumerate(new_repr) if x == randomTableA]
    tableA_seats = [x + 1 for x in tableA_seats] # add 1 to everything to match the fitness grid
    tableA_seats.remove(randomPersonA) # remove personA from the list
    randomPersonC = random.choice(tableA_seats)

    # Swap the two people between the tables
    new_repr[randomPersonC-1] = randomTableB
    new_repr[randomPersonB-1] = randomTableA

    # print("Swapped personC #" + str(randomPersonC) + " at table " + str(randomTableA) + " with personB #" + str(personB) + " at table " + str(randomTableB) + " for personA #" + str(randomPersonA))

    return new_repr

def scramble_mutation(representation, mut_prob):
    new_repr = deepcopy(representation)
    attendees_num = len(representation)

    # random chance to do the mutation
    if random.random() > mut_prob:
        print("Randomly chosen to not implement scramble_mutation.")
        return new_repr

    # limit the number of people that can be shuffled to at max 10
    if attendees_num < 10:
        limit = int(attendees_num / 2)
    else:
        limit = 10

    # choose a random number of people to get a subset
    numOfPeopleToShuffle = randint(2, limit) # cant shuffle 1 person, nothing would change

    startPerson = randint(0, attendees_num-numOfPeopleToShuffle) # set the biggest number it can randomly choose as the total - the number aimed to shuffle
    stopPerson = startPerson + numOfPeopleToShuffle
    
    # print("Number to shuffle: ", numOfPeopleToShuffle)
    # print("Range to shuffle: " + str(startPerson) + " - " + str(stopPerson))

    # shuffle the subset
    peopleToShuffle = new_repr[startPerson:stopPerson]
    random.shuffle(peopleToShuffle)
    new_repr[startPerson:stopPerson] = peopleToShuffle

    return new_repr

def inversion_mutation(representation, mut_prob):
    new_repr = deepcopy(representation)
    attendees_num = len(representation)
    
    # random chance to do the mutation
    if random.random() >= mut_prob:
        print("Randomly chosen to not implement inversion_mutation.")
        return new_repr
    
    # limit the number of people that can be shuffled to at max 10
    if attendees_num < 10:
        limit = int(attendees_num / 2)
    else:
        limit = 10

    # choose a random number of people to get a subset
    numOfPeopleToInvert = randint(2, limit) # cant invert 1 person, nothing would change - limiting to 10 indivs for less disruption

    startPerson = randint(0, attendees_num-numOfPeopleToInvert) # set the biggest number it can randomly choose as the total - the number aimed to shuffle
    stopPerson = startPerson + numOfPeopleToInvert

    # print("Number to invert: ", numOfPeopleToInvert)
    # print("Range to invert: " + str(startPerson) + " - " + str(stopPerson))

    # shuffle the subset
    peopleToInvert = new_repr[startPerson:stopPerson]
    # print(peopleToInvert)
    peopleToInvert.reverse()
    # print(peopleToInvert)
    # print("---------")
    new_repr[startPerson:stopPerson] = peopleToInvert
    
    return new_repr

def tableswap_mutation(representation, mut_prob):
    new_repr = deepcopy(representation)

    table_count = max(set(representation))

    # random chance to do the mutation
    if random.random() >= mut_prob:
        print("Randomly chosen to not implement tableswap_mutation.")
        return new_repr
    
    # get one individual from each table
    peopleToSwap = []
    for table_num in range(1, table_count+1):
        table_seats = [i+1 for i, val in enumerate(new_repr) if val == table_num]
        peopleToSwap.append(random.choice(table_seats))

    # shuffle the chosen people
    print(peopleToSwap)
    swap_copy = deepcopy(peopleToSwap)
    while swap_copy == peopleToSwap:
        random.shuffle(peopleToSwap)
    print(peopleToSwap)

    for idx in range(0, len(peopleToSwap)):
        table_num = idx + 1
        new_repr[peopleToSwap[idx]-1] = table_num

    return new_repr