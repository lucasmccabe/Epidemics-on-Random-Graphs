# Epidemics on Random Graphs

## Introduction
The code here aims at simulating an [SIR](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model/) disease outbreak over a [classical random graph](https://en.wikipedia.org/wiki/Random_graph). Included is functionality to incorporate interventions via a vaccine with a modifiable rollout.

## Table of Contents
* [Introduction](#introduction)
* [Table of Contents](#table-of-contents)
* [General Info](#general-info)
* [Usage](#usage)
* [Requirements](#requirements)
* [License](#license)

## General Info
We model a simple social network with a classical random graph G(n, p_adj), consisting of n nodes, whereby any two nodes are connected with probability p_adj. One randomly-selected node is infected with a virus V(p_inf, tau), becoming Patient Zero. During a time step, each infected node spreads the virus to each of its connected nodes with probability p_inf.  The expected number of time steps for a node to recover from infection is tau. For mathematical convenience, we ignore vital dynamics and assume that there are no births or deaths in the network.

## Usage

Most of the core functionality can be run using simRGSIR with command line arguments.

The first six command line arguments are:

1. **population**: the number of nodes to simulate.
2. **p_adjacent**: the probability of two nodes being connected.
3. **p_infect**: probability that an infected person will infect each of their connections during a time step.
4. **t_recover**: the average number of time steps it takes for an infected individual to recover from an infection.
5. **rollout**: describes rollout strategy. Two varieties are currently supported:

    - 'immediate' - after delay, vaccine immediately has specified prevalence.

    - 'linear' - linear rollout occurs with specified rate.

6. **effectiveness**: vaccine effectiveness. Describes fraction of potential transmissions that are avoided thanks to the vaccine.

If ` rollout=='immediate'`, then the seventh command line argument is:

7. **prevalence**: fraction of nodes who have the vaccine at the onset of the outbreak.

For example, to simulate an outbreak of V(0.15, 5) on G(1000, 0.1), with a uniform 40% of the population having a vaccine that is 70% effective against transmission, we can run:

```python
>>> python simRGSIR.py 1000 0.1 0.15 5 immediate 0.7 0.4
```

If ` rollout=='linear'`, then the seventh and eight command line arguments are:

7. **delay**: number of time steps before rollout begins.

8. **rate**: Rate parameter for linear rollout.


To simulate an outbreak of V(0.15, 5) on G(1000, 0.1), with a vaccine that is 70% effective against transmission being linearly rolled out with a rate parameter of 0.6 after a delay of 3 time steps, we can run:

```python
>>> python simRGSIR.py 1000 0.1 0.15 5 linear 0.7 3 0.6
```


For scripting and other uses, one can import the three main classes and run an experiment. For instance:

```python
from RG_SIR.experiment import Experiment
from RG_SIR.virus import Virus
from RG_SIR.vaccine import Vaccine

experiment = Experiment(population = 1000,
                        p_adjacent = 0.1,
                        virus = Virus(p_infect=0.15,
                                      t_recover = 5),
                        vaccine = Vaccine(effectiveness = 0.7,
                                          rollout = 'immediate',
                                          prevalence = 0.4)
                        )
experiment.run_experiment(show_progress = True)
```

## Requirements

This project was created with:
- `numpy==1.17.3`

## License
[MIT](https://choosealicense.com/licenses/mit/)
