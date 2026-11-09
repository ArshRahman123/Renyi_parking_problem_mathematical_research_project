import random
import math
import matplotlib.pyplot as plt
import numpy as np

def simulate_parking(line_length=100, car_length=1, max_cars=100, instances=1000, distribution='uniform'):
    # Storage for results
    num_cars_list = []
    density_list = []
    successful_placements_list = []
    success_percentage_list = []

    for num_attempts in range(1, max_cars + 1):
        total_cars_on_line = 0
        total_density = 0
        total_successful_placements = 0
        total_success_percentage = 0

        for _ in range(instances):
            parked_cars = []
            successful_placements = 0

            for _ in range(num_attempts):
                # Generate starting position
                if distribution == 'uniform':
                    start = random.uniform(0, line_length - car_length)
                elif distribution == 'normal':
                    mean = line_length / 2
                    std = line_length / 6                    # 50/3 =16.7
                    start = random.gauss(mean, std)
                    start = max(0, min(start, line_length - car_length))
                elif distribution == 'exponential':
                    lam = 1 / (line_length / 2) #lamda 1/50
                    u = random.random()
                    x = -math.log(1 - u) / lam        #ln(1-u)/lamda = x     start from cdf  F(x) = 1-e^(x (-lamda))
                    start = min(x, line_length - car_length)
                

                end = start + car_length

                # Check overlap
                overlap = False
                for car_start in parked_cars:
                    car_end = car_start + car_length
                    if not (end <= car_start or start >= car_end):
                        overlap = True
                        break

                if not overlap:
                    parked_cars.append(start)
                    successful_placements += 1

            total_cars_on_line += len(parked_cars)
            total_density += len(parked_cars) * car_length / line_length
            total_successful_placements += successful_placements
            total_success_percentage += successful_placements / num_attempts

        # Average results over instances
        num_cars_list.append(total_cars_on_line / instances)
        density_list.append(total_density / instances)
        successful_placements_list.append(total_successful_placements / instances)
        success_percentage_list.append((total_success_percentage / instances) * 100)

    return num_cars_list, density_list, successful_placements_list, success_percentage_list

def plot_results(max_cars=100, instances=1000):
    distributions = ['uniform', 'normal', 'exponential']
    metrics = ['Number of cars', 'Density','Success percentage']

    fig, axes = plt.subplots(3, 1, figsize=(12, 18))
    
    for distribution in distributions:
        num_cars_list, density_list, successful_placements_list, success_percentage_list = simulate_parking(
            max_cars=max_cars, instances=instances, distribution=distribution
        )

        axes[0].plot(range(1, max_cars + 1), num_cars_list, label=f'{distribution}')
        axes[1].plot(range(1, max_cars + 1), density_list, label=f'{distribution}')
        axes[2].plot(range(1, max_cars + 1), success_percentage_list, label=f'{distribution}')

    for i, ax in enumerate(axes):
        ax.set_xlabel("Number of attempted cars")
        ax.set_ylabel(metrics[i])
        ax.set_title(f"{metrics[i]}")
        ax.legend()
        ax.grid(True)

    plt.tight_layout()
    fig.subplots_adjust(hspace=0.4)
    plt.show()

# Run the simulation and plot
plot_results()