import random
import math

def colour_distance(c1, c2):
    rmean = (c1[0] + c2[0]) / 2
    r = c1[0] - c2[0]
    g = c1[1] - c2[1]
    b = c1[2] - c2[2]
    return np.sqrt(((2 + rmean/2356) * r * r) + 4 * g * g + ((2 + ((255 - rmean)/256)) * b * b) )

def read_books_list(file_path):
    book_list = {}
    with open(file_path, 'r') as file:
        for index, line in enumerate(file):
            if index == 0:
                continue  # Skip the first line as it is the header
            line = line.strip().split(',')
            book_list[line[0]] = [int(line[1]), int(line[2]), int(line[3])]
    return book_list

### useful for genetic algorithms
import numpy as np

# adjust fitness so it more likely that goood individual are selected
def population_fitness(population,book_list):
    td= [1/(total_distance(individual, book_list)/10000) for individual in population]
    fitness = np.exp(td)
    return fitness

def weighted_choice(population,fitness,num_choices):
    max = sum([c for c in fitness])
    selection_probs = [c/max for c in fitness]
    indices = np.random.choice(len(population), size=int(num_choices), replace=True, p=selection_probs)
    return indices

def reproduction(parent1, parent2):
    child = parent2.copy()  # Start with a copy of parent2
    i = random.randint(0,len(parent1))  # choosing crossover points
    j = random.randint(i,len(parent1))  # choosing crossover points
    child[0:i] = parent1[:i]
    child[j:len(parent1)] = parent1[j:len(parent1)]
    # check for duplacate
    element_count = {}
    for element in child:
        if element in element_count:
            element_count[element] += 1
        else:
            element_count[element] = 1
    # find missing elements from parent1 in child
    missing_elements = [element for element in parent1 if element not in element_count]
    # replace duplicates with missing 
    for idx, element in enumerate(child):
        if missing_elements and element_count[element] > 1:
            child[idx] = missing_elements.pop(0)
            element_count[element] -= 1
            element_count[child[idx]] = element_count.get(child[idx], 0) + 1
    return child
