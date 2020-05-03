import numpy as np
import random
import datetime
import math
import copy
from virus import Virus
from vaccine import Vaccine

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
        -At each time step, each infected node recovers with probability
        self.virus.p_recover, which is set to the maximum likelihood estimate
        of a parameter p for a geometric random variable whereby
        E[Geo(p)] = self.t_recover.
    '''

    def __init__(self,
                population: int = 100,
                p_adjacent: float = 0.1,
                virus: object = Virus(p_infect = 0.1,
                                        t_recover = 1),
                vaccine: object = Vaccine(effectiveness = 0.5,
                                            rollout = 'immediate',
                                            prevalence = 0,
                                            delay = 0,
                                            rate = 0),
                max_threshold: float = 1.0
                ):
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
            max_threshold: the simulation halts if at least this fraction of
                the population becomes infected.
        Raises:
            ValueError: if population is not >0.
            ValueError: if p_adjacent is not in [0,1].
        '''
        if population <= 0:
            raise ValueError('Cannot have negative or zero population.')
        elif max_threshold < 0 or max_threshold > 1:
            raise ValueError('max_threshold must be between 0 and 1.')
        elif p_adjacent < 0 or p_adjacent > 1:
            raise ValueError('Invalid probability for p_adjacent.')
        else:
            self.population = population
            self.p_adjacent = p_adjacent
            self.virus = virus
            self.vaccine = vaccine
            self.adjacency = self.init_adjacency()
            self.infected = self.init_infected()
            self.immune = self.init_immune()
            self.vaccinated = self.init_vaccinated()
            self.time_step = 0
            self.newly_infected = 1
            self.max_threshold = max_threshold

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

        A value of zero indicates an uninfected node, and nonzero value
        indicates an infected node.
        '''
        infected = np.zeros(self.population)
        infected[random.randint(0, self.population-1)] = 1
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

    def init_vaccinated(self):
        '''
        Initializes array describing vaccinated nodes. This is used to track
        vaccine rollout.
        '''
        if self.vaccine.rollout == 'immediate':
            #a fraction self.vaccine.prevalence of all nodes are randomly
            #selected to receive the vaccine
            vaccinated = np.zeros(self.population)
            vaccinated[:int(self.vaccine.prevalence*self.population)] = 1
            np.random.shuffle(vaccinated)
        if self.vaccine.rollout == 'linear':
            #if the rollout is linear, the initial vaccine prevalence is zero
            vaccinated = np.zeros(self.population)

        return vaccinated

    def count_infected(self):
        '''
        Returns the number of infected individuals.
        '''
        return np.count_nonzero(self.infected)

    def count_immune(self):
        '''
        Returns the number of recovered/naturally immune individuals.
        '''
        return np.count_nonzero(self.immune)

    def count_vaccinated(self):
        '''
        Returns the number of vaccinated individuals.
        '''
        return np.count_nonzero(self.vaccinated)

    def propagate_virus(self):
        '''
        Each infected node spreads the virus to each
        of its connected nodes with probability p_infect. For clarity, the
        expected number of nodes and infected node v will infect in a given time
        step is given by p_infect*degree(v).
        '''
        updated_infected = copy.deepcopy(self.infected)
        #print('Infection count:', self.count_infected())
        #print(self.infected)
        for i in range(self.population):
            if self.infected[i] == 1:
                #virus can only be spread from infected node
                for j in range(self.population):
                    #iterates adjacency row for node i
                    if (self.adjacency[i][j] == 1 and
                        random.random()<=self.virus.p_infect and
                        self.infected[j] == 0 and
                        self.immune[j] == 0):
                        #contact with an infected node occurs, opening the
                        #POSSIBILITY of transmission
                        #transmission cannot occur when potential recipient is
                        #(naturally) immune (e.g. recovered)
                        if (self.vaccinated[j] == 1 and
                            random.random()<=self.vaccine.effectiveness):
                            #transmission is avoided with probability
                            #self.vaccine.effectiveness in the case of
                            #vaccinated recipient
                            continue
                        updated_infected[j] = 1
        self.newly_infected = np.sum(updated_infected - self.infected)
        self.infected = updated_infected
        #print('Newly infected: ', done_prop)
        #print(self.count_infected())
        return None

    def update_infected(self):
        '''
        Each infected node recovers with probability self.virus.p_recover.
        '''
        for i in np.where(self.infected == 1)[0]:
            if random.random() <= self.virus.p_recover:
                self.infected[i] = 0
                self.immune[i] = 1
        return None

    def update_vaccinated(self):
        '''

        Raises:
            NotImplementedError for unimplemented rollouts. Shouldn't really
                happen.
        '''
        if self.vaccine.rollout == 'immediate':
            return None
        if self.vaccine.rollout == 'linear':
            if self.time_step >= self.vaccine.delay:
                #self.vaccine.rate*self.population is the number of new nodes
                #that become vaccinated each time step.
                if len(np.where(self.vaccinated == 0)[0]) <= \
                                            self.vaccine.rate*self.population:
                    #If there are fewer than self.vaccine.rate*self.population
                    #unvaccinated nodes remaining, all nodes become vaccinated.
                    self.vaccinated = np.ones(self.population)
                else:
                    self.vaccinated[random.sample(
                                    list(np.where(self.vaccinated == 0)[0]),
                                    int(self.vaccine.rate*self.population))] = 1
        else:
            raise NotImplementedError

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
        1. Virus is propagated by infected nodes.
        2. Infected nodes become one step closer to recovery.
        3. Newly-recovered nodes become immune.

        If the vaccine rollout is not immediate, a fourth event occurs:
        4. The number of nodes vaccinated updates according to the defined
        rollout strategy.
        '''
        self.propagate_virus() #handles event 3
        if self.time_step != 0:
            self.update_infected() #handles events 2 and 3
        self.update_vaccinated() #handles event 4
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

    def print_progress(self):
        '''
        Prints interesting progress metrics for each time step.
        '''
        print('**********')
        print('Time step: %d:' %self.time_step)
        print('Newly Infected: %d' %self.newly_infected)
        print('Max Infected At Once: %d' %max(self.infected_history))
        print('Total Infected Now: %d' %self.count_infected())
        print('Total Vaccinated Now: %d' %self.count_vaccinated())
        print('Total Recovered/Immune Now: %d' %self.count_immune())

    def run_experiment(self, show_progress: bool = False):
        '''
        Runs an experiment. Experiment stops when either one of:
            1. The entire population is infected.
            2. The entire population has recovered.

        Arguments:
            show_progress: If True, prints some progress metrics.
        Returns:
            None
        '''
        while (0 < self.count_infected() < self.population*self.max_threshold):
            if show_progress:
                self.print_progress()
            self.simulate_step()
        if show_progress:
            self.print_progress()
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
