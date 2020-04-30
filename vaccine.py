class Vaccine():
    def __init__(self,
                effectiveness: float = 0.5,
                rollout: str = 'immediate',
                prevalence: float = 0,
                delay: float = 0,
                rate: float = 0):
        '''
        Constructor for the Vaccine class.

        Arguments:
            effectiveness: Vaccine effectiveness. Describes fraction of
                potential transmissions that are avoided thanks to the vaccine.
            rollout: Describes rollout. Two varieties are currently supported:
                'immediate' - After delay, vaccine immediately has specified
                    prevalence.
                'linear' - Linear rollout occurs with specified rate.
            prevalence: Fraction of nodes who have the vaccine. If rollout is
                linear, this varies.
            delay: Number of time steps before rollout begins.
            rate: Rate parameter for linear rollout.
        Raises:
            many ValueError, should detail later
        '''
        if 0<=effectiveness<=1:
            self.effectiveness = effectiveness
        else:
            raise ValueError('effectiveness must be between 0 and 1.')

        if rollout.lower() in ['immediate', 'linear']:
            self.rollout = rollout.lower()
        else:
            raise ValueError('Invalid rollout provided.')

        if 0<=prevalence<=1:
            self.prevalence = prevalence
        else:
            raise ValueError('prevalence must be between 0 and 1.')

        if delay >= 0 and int(delay)==delay:
            self.delay = delay
        else:
            raise ValueError('delay must be an integer at least zero.')

        if 0<=rate<=1:
            self.rate = rate
        else:
            raise ValueError('rate must be between 0 and 1.')

        if rollout == 'linear' and prevalence != 0:
            raise ValueError('prevalence must start at 0 with variable rollout.')
