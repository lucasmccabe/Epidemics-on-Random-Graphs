#!/usr/bin/env python

r"""
Sample script exhibiting a binary search and simulation for estimating the
endemic steady state-inducing lower bound for alpha (rollout rate).

Intended for demonstration purposes only. Simply run the script directly from
the command line.

Example Usage:
>>> python estimate_alpha.py
**********
Simulated outbreak with alpha = 0.500000
**********
Simulated outbreak with alpha = 0.750000
**********
Simulated outbreak with alpha = 0.625000
**********
Simulated outbreak with alpha = 0.562500
**********
Simulated outbreak with alpha = 0.531250
**********
Simulated outbreak with alpha = 0.546875
**********
Simulated outbreak with alpha = 0.554688
Estimated endemic steady state lower bound for alpha: 0.554688.
"""

from RG_SIR.experiment import Experiment
from RG_SIR.virus import Virus
from RG_SIR.vaccine import Vaccine

#ADJUST PARAMS HERE-----
population = 1000
p_adjacent = 0.1
p_infect = 0.35
t_recover = 4
effectiveness = 0.65
rollout = 'linear'
prevalence = 0
delay = 1

stop_within = 0.01
#-------

alpha_high = 1.0
alpha_low = 0.0

while (abs(alpha_high-alpha_low) >= stop_within):
    alpha = (alpha_high+alpha_low)/2

    experiment = Experiment(population = population,
                            p_adjacent = p_adjacent,
                            virus = Virus(p_infect=p_infect,
                                        t_recover = t_recover),
                            vaccine = Vaccine(effectiveness = effectiveness,
                                        rollout = rollout,
                                        prevalence = prevalence,
                                        delay = delay,
                                        rate = alpha)
                            )

    experiment.run_experiment(show_progress = False)

    print('Simulated outbreak with alpha = %f' %alpha)
    #print(max(experiment.infected_history))

    if max(experiment.infected_history) < (1 - (1/t_recover))*0.925*population:
        alpha_high = alpha
    else:
        alpha_low = alpha


print('Estimated endemic steady state lower bound for alpha: %f.' %alpha)
