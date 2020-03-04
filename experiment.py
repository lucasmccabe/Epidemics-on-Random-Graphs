import numpy as np
import random
from virus import Virus


class Experiment():
    '''
    Simulate an epidemic over a random graph.
    '''

    def __init__(self, population:int = 10, p_partner:float = 0.5, p_infect: float = 0.02):
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

    #def simulate_step(self):
