import numpy as np
import random
from virus import Virus
import datetime
import math


class Experiment():
    '''
    Simulates a virus spreading over a classical random graph.

    General framework:
        -Begin with a classical random graph G(population, p_adjacent), with one
        node having a Virus(p_infect, t_recover).
        -During a time step, each infected node spreads the virus to each
        of its connected nodes with probability p_infect. For clarity, the
        expected number of nodes and infected node v will infect in a given time
        step is given by p_infect*degree(v).
        -After a certain number of time steps, an infected node recovers and
        is then immune to the virus.
    '''

    def __init__(self,
                population:int = 100,
                p_adjacent:float = 0.1,
                p_infect: float = 0.1,
                t_recover: float = 1):
        '''
        Constructor for the Experiment class. Initializes world for
        experimentation.

        Arguments:
            population: the number of nodes to simulate.
                Corresponds to the n in G(n,p).
            p_adjacent: the probability of two nodes being connected.
                Corresponds to the p in G(n,p).
            p_infect: probability that an infected person will infect each of
                their connections during a time step.
                For clarity, the expected number of nodes and infected node v
                will infect in a given time step is given by p_infect*degree(v).
            t_recover: the number of time steps it takes for an infected
                individual to recover from an infection.
                *Note: to consider the simlified scenario with no recovery or
                    immunity, use t_recover = math.inf
        Raises:
            ValueError: if population is not >0.
            ValueError: if p_adjacent is not in [0,1].
            ValueError: if p_infect is not in [0,1].
            ValueError: if t_recover is not >=0.
        '''
        if population <= 0:
            raise ValueError('Cannot have negative or zero population.')
        elif p_adjacent < 0 or p_adjacent > 1:
            raise ValueError('Invalid probability for p_adjacent.')
        elif p_infect < 0 or p_infect > 1:
            raise ValueError('Invalid probability for p_infect.')
        elif t_recover < 0:
            raise ValueError('Cannot have negative t_recover.')
        else:
            self.population = population
            self.p_adjacent = p_adjacent

            self.adjacency = self.init_adjacency()
            self.virus = Virus(p_infect, t_recover)
            self.infected = self.init_infected()
            self.immune = self.init_immune()
            self.time_step = 0

            #experiment history:
            self.infected_history = [1]
            self.immune_history = [0]


    def init_adjacency(self):
        '''
        Initializes adjacency matrix.

        Creates a square matrix of size population whose lower triangular
        values are drawn from a binomial distribution with probability
        p_adjacent. Matrix is then made symmetric with a zero diagonal.
        '''
        adjacency = np.random.binomial(1,
                                    self.p_adjacent,
                                    (self.population, self.population)
                                    )
        adjacency -= np.triu(adjacency) #makes upper triangle and diagonal zero
        adjacency += adjacency.T #makes upper triangle=lower triangle for symmetry
        return adjacency

    def init_infected(self):
        '''
        Initializes array describing infected nodes. At initialization, this is a
        one-dimensional array of length population with zeros everywhere except
        at one node (one infected node in the population).

        Of note is that this is not a binary matrix, as it is also used to track
        recovery times. As such, a value of zero indicates an uninfected node,
        and a (positive) nonzero value indicates an infected node with that
        many time steps left before recovery.
        '''
        infected = np.zeros(self.population)
        infected[random.randint(0, self.population)] = self.virus.t_recover
        return infected

    def init_immune(self):
        '''
        Initializes array describing immune nodes. At initialization, this is a
        one-dimensional array of length population with zeros everywhere (at
        first, zero nodes have immunity). After an infected node recovers, they
        are designated immune and can neither catch nor pass on the virus.
        '''
        immune = np.zeros(self.population)
        return immune

    def count_infected(self):
        '''
        Returns the number of infected individuals.
        '''
        return np.count_nonzero(self.infected)

    def count_immune(self):
        '''
        Returns the number of immune individuals.
        '''
        return np.count_nonzero(self.immune)

    def propagate_virus(self):
        '''
        Each infected node spreads the virus to each
        of its connected nodes with probability p_infect. For clarity, the
        expected number of nodes and infected node v will infect in a given time
        step is given by p_infect*degree(v).
        '''
        for i in range(self.population):
            if self.infected[i] == 0:
                #virus cannot be spread from a node without the virus
                continue
            if np.sum(self.adjacency[i]) == 0:
                #catches case where node i has zero connections
                continue
            for j in range(self.population): #iterates adjacency row for node i
                if (self.adjacency[i][j] == 1 and
                    random.random()<=self.virus.p_infect and
                    self.infected[j] == 0 and
                    self.immune[j] != 1):
                    #if node j is not already infected and node j is
                    #not immune, the virus spreads from node i to node j
                    self.infected[j] = self.virus.t_recover
        return None

    def update_immune(self):
        '''
        Newly-recovered nodes become immune.
        '''
        for i in np.where(np.array(self.infected)==1)[0]:
            self.immune[i] = 1
        return None

    def update_infected(self):
        '''
        Infected nodes become one step closer to recovery.
        '''
        for i in np.where(np.array(self.infected)>0)[0]:
            self.infected[i] -= 1
        return None

    def update_history(self):
        '''
        Updates experiment history for tracking.
        '''
        self.infected_history.append(self.count_infected())
        self.immune_history.append(self.count_immune())
        return None

    def simulate_step(self):
        '''
        Simulates a single simulation time step. Three events occur:

        1. Infected nodes become one step closer to recovery.
        2. Newly-recovered nodes become immune.
        3. Virus is propagated by infected nodes.
        '''
        if self.time_step != 0:
            self.update_immune() #handles event 1
            self.update_infected() #handles event 2
        self.propagate_virus() #handles event 3

        self.update_history() #updates history for tracking experiment
        self.time_step += 1
        return None

    def calculate_ever_infected(self):
        '''
        Returns the total number of nodes have ever had the virus. This is
        the sum of count(nodes who currently have the virus) and
        count(nodes who are now immune).
        '''
        ever_infected = np.add(self.infected, self.immune)
        np.place(ever_infected, ever_infected>0, 1)
        return np.sum(ever_infected)

    def run_experiment(self, show_progress: bool = False):
        '''
        Runs an experiment. Experiment stops when either one of:
            1. The entire population is infected.
            2. The entire population has recovered.

        Arguments:
            show_progress: If True, prints:
                -current time step
                -total number infected
                -total number immune
        Returns:
            None
        '''
        while (0 < self.count_infected() < self.population):
            self.simulate_step()

            if show_progress:
                print('**********')
                print('Time step: %d:' %self.time_step)
                print('Infected: %d' %self.count_infected())
                print('Immune: %d' %self.count_immune())
        print('**********')
        return None

    def save_experiment_results(self):
        '''
        Saves experiment history/results to a text file. The file contains six
        lines, population as follows:
            -population
            -p_adjacent
            -p_infect
            -t_recover
            -max number infected in any single time step
            -total number infected across the experiment
            -R_0
            -infected_history
            -immune_history
        '''
        experiment_id = str(datetime.datetime.now()).replace(' ','_')
        for ch in ['-', ':', '.']:
            experiment_id = experiment_id.replace(ch, '')

        with open('Trials/Trial_' + experiment_id + '.txt', 'w') as output:
            for param in [self.population,
                        self.p_adjacent,
                        self.virus.p_infect,
                        self.virus.t_recover,
                        max(self.infected_history),
                        self.calculate_ever_infected()]:
                output.write('%s\n' %param)
            for i in range(self.time_step):
                output.write('%s ' %self.infected_history[i])
            output.write('\n')
            for i in range(self.time_step):
                output.write('%s ' %self.immune_history[i])

        output.close()
        return None
