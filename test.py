from experiment import Experiment


test_experiment = Experiment(population = 1000,
                            p_adjacent = 0.2,
                            p_infect = 0.001,
                            t_recover = 14)

test_experiment.run_experiment(show_progress = True)
test_experiment.save_experiment_results()
