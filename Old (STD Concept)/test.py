from experiment import Experiment

test_exp = Experiment()

print(test_exp.partners)
print('\n')

for step in range(1000):
    test_exp.simulate_step()
    print(test_exp.count_infected())
