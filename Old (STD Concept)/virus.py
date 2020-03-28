class Virus():
    def __init__(self, p_infect: float):
        '''
        Constructor for the Virus class.

        Arguments:
            p_infect: probability that an infected person will infect their
                partner during an encounter.
        Raises:
            ValueError: if p_infect is not in [0,1]
        '''
        if 0<=p_infect<=1:
            self.p_infect = p_infect
        else:
            raise ValueError('Invalid probability for p_infect.')
