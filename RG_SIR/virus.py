#!/usr/bin/env python

class Virus():
    def __init__(self,
                p_infect: float = 0.1,
                t_recover: float = 1):
        '''
        Constructor for the Virus class.

        Arguments:
            p_infect: probability that an infected person will infect their
                partner during an encounter.
            t_recover: the average number of time steps it takes for an infected
                individual to recover from an infection.
        Raises:
            ValueError: if p_infect is not in [0,1]
            ValueError: if t_recover is not in [0,inf)
        '''
        if 0<=p_infect<=1:
            self.p_infect = p_infect
        else:
            raise ValueError('p_infect must be between 0 and 1.')

        if 0<=t_recover:
            self.t_recover = t_recover
        else:
            raise ValueError('t_recover must be at least 0.')

        #p_recover is the parameter estimate of a geometric random variable
        #with E[Geo(p)]=t_recover
        self.p_recover = 1.0/t_recover
