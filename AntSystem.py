def VeryBadTour(costs, number_of_cities):
    t = list(range(number_of_cities))
    return SolutionValue(costs, t)


def PheromoneUpdate(v, s):
    global pheromones
    global evaporation_constant
    for ix, i in np.ndenumerate(pheromones):
        pheromones[ix[0]][ix[1]] = (1-evaporation_constant) * i
    for j in range(len(s)-1):
        pheromones[s[j]][s[j+1]] += (1 / v)
        pheromones[s[j+1]][s[j]] += (1 / v)


def SolutionValue(costs, s):
    v = 0
    for i in range(len(s)):
        if i == len(s)-1:
            v = v + costs[s[i]][s[0]]
        else:
            v = v + costs[s[i]][s[i+1]]
    return v

def SolutionConstruction(l = None):
    if type(l) == int:
        s = [l]
    else:
        s = []
    N = Determine(s)
    while len(N) > 0:
        c = ChooseFrom(N, s)
        s.append(c)
        N = Determine(s)
    return s

def Determine(s):
    global number_of_cities
    N = list(range(number_of_cities))
    if len(s) > 0:
        for i in s:
            N.remove(i)
    return N

def ChooseFrom(N, s):
    global pheromones
    global alpha
    global beta
    probabilities = []
    total_factor = 0
    if len(s) > 0:
        current_loc = s[-1]    
        for n in N:
            phe = pheromones[current_loc][n]
            dis = costs[current_loc][n]
            total_factor += (np.power(phe, alpha) * np.power(1/dis, beta))
        for n in N:
            phe = pheromones[current_loc][n]
            dis = costs[current_loc][n]
            decision_probability = (np.power(phe, alpha) * np.power(1/dis, beta)) / total_factor #pheromone model
            probabilities.append(decision_probability)
        c = np.random.choice(N, p=probabilities, size=1)[0] #probabilistic decision for next state
    else:
        c = np.random.choice(N) #random starting location if it is not set
    return c

import numpy as np

evaporation_constant = 0.5
number_of_cities = 2
pheromones = np.ones((number_of_cities, number_of_cities))
alpha = 1
beta = 2

def Initialization(costs, e, a, b):
    global evaporation_constant
    evaporation_constant = e
    global number_of_cities
    number_of_cities = len(costs)
    global alpha
    alpha = a
    global beta
    beta = b
    global pheromones
    D = VeryBadTour(costs, number_of_cities)
    initial_pheromone_value = number_of_cities / D
    initial_pheromones = np.ones((number_of_cities, number_of_cities))
    initial_pheromones.fill(initial_pheromone_value)
    pheromones = initial_pheromones

def AntSystem(costs, e = 0.5, n = 10, alpha = 1, beta = 5, starting_location = None):
    Initialization(costs, e, alpha, beta)
    best_solution = []
    best_value = VeryBadTour(costs, number_of_cities)
    while n > 0:
        s = SolutionConstruction(l = starting_location)
        v = SolutionValue(costs, s)
        if v < best_value or len(best_solution) == 0:
            s.append(s[0])
            best_solution = s
            best_value = v
        PheromoneUpdate(v, s)
        n = n - 1
    print(f'{best_solution} is the best tour and {best_value} is the best value')
