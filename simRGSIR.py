#!/usr/bin/env python

from RG_SIR.experiment import Experiment
from RG_SIR.virus import Virus
from RG_SIR.vaccine import Vaccine
import sys

if __name__ == "__main__":
    population = int(sys.argv[1])
    p_adjacent = float(sys.argv[2])
    p_infect = float(sys.argv[3])
    t_recover = int(sys.argv[4])
    rollout = str(sys.argv[5])
    effectiveness = float(sys.argv[6])

    if rollout == 'immediate':
        prevalence = float(sys.argv[7])

        experiment = Experiment(population = population,
                                p_adjacent = p_adjacent,
                                virus = Virus(p_infect=p_infect,
                                            t_recover = t_recover),
                                vaccine = Vaccine(effectiveness = effectiveness,
                                            rollout = rollout,
                                            prevalence = prevalence)
                                )
    else:
        delay = int(sys.argv[7])
        rate = float(sys.argv[8])

        experiment = Experiment(population = population,
                                p_adjacent = p_adjacent,
                                virus = Virus(p_infect=p_infect,
                                            t_recover = t_recover),
                                vaccine = Vaccine(effectiveness = effectiveness,
                                            rollout = rollout,
                                            delay = delay,
                                            rate = rate)
                                )

    experiment.run_experiment(show_progress = True)
