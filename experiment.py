import numpy as np
import random
from virus import Virus
import datetime


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
        Raises:
            ValueError: if population is not >0.
            ValueError: if p_adjacent is not in [0,1].
        '''
        if population<=0:
            raise ValueError('Cannot have negative or zero population.')
        elif p_adjacent<0 or p_adjacent>1:
            raise ValueError('Invalid probability for p_adjacent.')
        else:
            self.population = population
            self.p_adjacent = p_adjacent

        self.adjacency = self.init_adjacency(population, p_adjacent)
        self.virus = Virus(p_infect, t_recover)
        self.infected = self.init_infected(population)
        self.immune = self.init_immune(population)
        self.time_step = 0

        #experiment history:
        self.infected_history = [1]
        self.immune_history = [0]


    def init_adjacency(self, population:int, p_adjacent:float):
        '''
        Initializes adjacency matrix.

        Creates a square matrix of size population whose lower triangular
        values are drawn from a binomial distribution with probability
        p_adjacent. Matrix is then made symmetric with a zero diagonal.

        Arguments:
            population: the number of nodes to simulate.
            p_adjacent: the probability of two nodes being connected.
        Returns:
            partners
        '''
        adjacency = np.random.binomial(1, p_adjacent, (population,population))
        adjacency -= np.triu(adjacency) #makes upper triangle and diagonal zero
        adjacency += adjacency.T #makes upper triangle=lower triangle for symmetry
        return adjacency

    def init_infected(self, population:int):
        '''
        Initializes array describing infected nodes. At initialization, this is a
        one-dimensional array of length population with zeros everywhere except
        at one node (one infected node in the population).

        Of note is that this is not a binary matrix, as it is also used to track
        recovery times. As such, a value of zero indicates an uninfected node,
        and a (positive) nonzero value indicates an infected node with that
        many time steps left before recovery.

        Arguments:
            population: the number of people/nodes to simulate.
        Returns:
            infected
        '''
        infected = np.zeros(population)
        infected[random.randint(0,population)] = self.virus.t_recover
        return infected

    def init_immune(self, population:int):
        '''
        Initializes array describing immune nodes. At initialization, this is a
        one-dimensional array of length population with zeros everywhere (at
        first, zero nodes have immunity). After an infected node recovers, they
        are designated immune and can neither catch nor pass on the virus.

        Arguments:
            population: the number of people/nodes to simulate.
        Returns:
            None
        '''
        immune = np.zeros(population)
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
        return None

    def save_experiment_results(self):
        '''
        Saves experiment history/results to a text file. The file contains six
        lines, population as follows:
            -population
            -p_adjacent
            -p_infect
            -t_recover
            -max number infected in any time step
            -max number immune in any time step (number immune at end)
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
                        self.immune_history[-1]]:
                output.write('%s\n' %param)
            for i in range(self.time_step):
                output.write('%s ' %self.infected_history[i])
            output.write('\n')
            for i in range(self.time_step):
                output.write('%s ' %self.immune_history[i])

        output.close()
        return None
