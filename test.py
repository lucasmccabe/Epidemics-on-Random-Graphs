from experiment import Experiment
import matplotlib.pyplot as plt
import numpy as np

recovery_times_considered = 50
trials_per_recovery_time = 50

total_infected = []
for t in range(1,1+recovery_times_considered):
    total_infected_samples = []
    for trial in range(trials_per_recovery_time):
        test_experiment = Experiment(population = 1000,
                                    p_adjacent = 0.2,
                                    p_infect = 0.001,
                                    t_recover = t)

        test_experiment.run_experiment(show_progress = True)
        test_experiment.save_experiment_results()
        print(test_experiment.calculate_ever_infected())
        total_infected_samples.append(test_experiment.calculate_ever_infected())
    total_infected.append(np.mean(total_infected_samples))

plt.plot(range(1,1+recovery_times_considered), total_infected)
plt.xlabel('Viral Recovery Time')
plt.ylabel('Total Infected (out of 1000 nodes)')
plt.title('V(0.001, t) over G(1000, 0.2)')
plt.show()
