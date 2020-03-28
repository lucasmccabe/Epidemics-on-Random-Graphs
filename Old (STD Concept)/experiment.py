import numpy as np
import random
from virus import Virus


class Experiment():
    '''
    Simulate an epidemic over a random graph.
    '''

    def __init__(self,
                population:int = 100,
                p_partner:float = 0.2,
                p_infect: float = 0.2):
        '''
        Constructor for the Experiment class.
        Initializes world for experimentation.

        Arguments:
            population: the number of people/nodes to simulate
            p_partner: the probability of two nodes being sexual partners
            p_infect: probability that an infected person will infect their
                partner during an encounter.
        Raises:
            ValueError: if population is not >0
            ValueError: if p_partner is not in [0,1]
        '''
        if population<=0:
            raise ValueError('Cannot have negative or zero population.')
        elif p_partner<0 or p_partner>1:
            raise ValueError('Invalid probability for p_partner.')
        else:
            self.population = population
            self.p_partner = p_partner

        self.partners = self.init_partners(population, p_partner)
        self.infected = self.init_infected(population)
        self.virus = Virus(p_infect)


    def init_partners(self, population:int, p_partner:float):
        '''
        Initializes sexual partners matrix.
        Creates a square matrix of size population whose lower triangular
        values are drawn from a binomial distribution with probability
        p_partner. Matrix is then made symmetric with a zero diagonal.

        Arguments:
            population: the number of people/nodes to simulate
            p_partner: the probability of two nodes being sexual partners
        Returns:
            partners
        '''
        partners = np.random.binomial(1, p_partner, (population,population))
        partners -= np.triu(partners) #makes upper triangle and diagonal zero
        partners += partners.T #makes upper triangle = lower triangle for symmetry
        return partners


    def init_infected(self, population:int):
        '''
        Initializes array of infected individuals.
        At initialization, this is a one-dimensional array of length
        population with zeros everywhere except at one node (one infected
        person in the population).


        Arguments:
            population: the number of people/nodes to simulate
        Returns:
            infected
        '''
        infected = np.zeros(population)
        infected[random.randint(0,population)] = 1
        return infected


    def count_infected(self):
        '''
        Counts the number of infected individuals.
        '''
        return np.sum(self.infected)


    def simulate_step(self):
        '''
        Simulates a single simulation time step.
        '''
        had_encounter = [] #track the indices of individuals who have an encounter,
            #so as not to repeat partners when iterating through partner matrix
        for i in range(len(self.partners)):
            if i in had_encounter:
                #catches case where person i already had an encounter
                continue
            if np.sum(self.partners[i][i+1:]) == 0:
                #catches case where person i has zero potential partners
                continue

            potential_partners = [j+i+1 for j, x in
                                    enumerate(self.partners[i][i+1:]) if x == 1]

            if not [partner for partner in potential_partners
                                            if partner not in had_encounter]:
                #catches case where all of person i's potential partners have
                #already had an encounter
                continue

            partner = random.choice(potential_partners) #randomly select a partner
            while partner in had_encounter:
                #if selected partner has already had an encounter, choose again
                partner = random.choice(potential_partners)
            had_encounter += [i, partner]

            if self.infected[i] == 0:
                #not infected, cannot infect partner
                continue
            else:
                #infected, can infect partner
                if random.random() <= self.virus.p_infect:
                    #print('%d infects %d' %(i, partner))
                    self.infected[partner] = 1
