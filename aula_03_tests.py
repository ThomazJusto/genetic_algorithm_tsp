import random as random
import bisect

def genetic_algorithm(population, fn_fitness, gene_pool, fn_thres=None, ngen=1000, pmut=0.1):

    # for each generation
    for i in range(ngen):

        # create a new population
        new_population = []

        # repeat to create len(population) individuals
        for i in range(len(population)):

          # select the parents
          p1, p2 = select(2, population, fn_fitness)

          # recombine the parents, thus producing the child
          child = recombine(p1, p2)

          # mutate the child
          child = mutate(child, gene_pool, pmut)

          # add the child to the new population
          new_population.append(child)

        # move to the new population
        population = new_population

        # check if one of the individuals achieved a fitness of fn_thres; if so, return it
        fittest_individual = fitness_threshold(fn_fitness, fn_thres, population)
        if fittest_individual:
            return fittest_individual

    # return the individual with highest fitness
    return max(population, key=fn_fitness)

# get the best individual of the received population and return it if its
# fitness is higher than the specified threshold fn_thres
def fitness_threshold(fn_fitness, fn_thres, population):
    if not fn_thres:
        return None

    fittest_individual = max(population, key=fn_fitness)
    if fn_fitness(fittest_individual) >= fn_thres:
        return fittest_individual

    return None


# genetic operator for selection of individuals;
# this function implements roulette wheel selection, where individuals with
# higher fitness are selected with higher probability
def select(r, population, fn_fitness):
    fitnesses = map(fn_fitness, population)
    sampler = weighted_sampler(population, fitnesses)
    return [sampler() for i in range(r)]

# return a single sample from seq; the probability of a sample being returned
# is proportional to its weight
def weighted_sampler(seq, weights):
    totals = []
    for w in weights:
        totals.append(w + totals[-1] if totals else w)
    return lambda: seq[bisect.bisect(totals, random.uniform(0, totals[-1]))]

# genetic operator for recombination (crossover) of individuals;
# this function implements single-point crossover, where the resulting individual
# carries a portion [0,c] from parent x and a portion [c,n] from parent y, with
# c selected at random
def recombine(x, y):
    n = len(x)
    c = random.randrange(0, n)
    return x[:c] + y[c:]

# genetic operator for mutation;
# this function implements uniform mutation, where a single element of the
# individual is selected at random and its value is changed by a randomly chosen
# value (out of the possible values in gene_pool)
def mutate(x, gene_pool, pmut):

    # if random >= pmut, then no mutation is performed
    if random.uniform(0, 1) >= pmut:
        return x

    n = len(x)
    g = len(gene_pool)
    c = random.randrange(0, n) # gene to be mutated
    r = random.randrange(0, g) # new value of the selected gene

    new_gene = gene_pool[r]
    return x[:c] + [new_gene] + x[c+1:]

def init_population(pop_number, gene_pool, state_length):
    g = len(gene_pool)
    population = []
    for i in range(pop_number):
        # each individual is represented as an array with size state_length,
        # where each position contains a value from gene_pool selected at random
        new_individual = [gene_pool[random.randrange(0, g)] for j in range(state_length)]
        population.append(new_individual)
        #print(new_individual)

    return population

# evaluation class for the n-Queens problem -> Classe que vai servir para o fitness function
class EvaluateNQueens:
    # during initialization, store the problem instance
    def __init__(self, n):
        self.n = n

    # compute the value of the received solution
    def __call__(self, solution):
        conflicts = 0

        # TO DO: count the number of conflicts
        

        # our genetic algorithm implementation maximises the value;
        # moreover, its selection operator does not handle negative values properly;
        # thus, we estimate the maximum possible number of conflicts (which is
        # given by n(n-1)/2) and subtract from it the number of conflicts of the
        # received solution; this allows our algorithm to maximize the fitness;
        # hence, our objective here is to get as close to n(n-1)/2 as possible
        return ((self.n * (self.n - 1)))/2 - conflicts


# TESTING WITH THE PROBLEM: Queens
problem_instance = [0, 0, 0, 0, 0, 0, 0, 0]
fn_fitness = EvaluateNQueens(problem_instance)
possible_values = [x for x in range(8)] #[0, 1, 2, 3, 4, 5, 6, 7]  

#quantidade
individual_length = 8

# population size
population_size = 5

# initial population
population = init_population(population_size, possible_values, individual_length)

# run the algoritm
solution = genetic_algorithm(population, fn_fitness, gene_pool=possible_values, fn_thres=10)

# print the results
print('Resulting solution: %s' % solution)
print('Value of resulting solution: %d' % fn_fitness(solution))