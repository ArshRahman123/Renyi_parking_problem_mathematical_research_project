import random
import math
import matplotlib.pyplot as plt

def renyi_parking(line_length=100, car_length=1):
    num_attempts = int(input("Enter the number of cars to attempt: "))
    print("Choose a distribution for car placement:")
    print("1. Uniform")
    print("2. Normal")
    print("3. Exponential")
    choice = input("Enter 1, 2, or 3: ").strip()

    parked_cars = []
    successful_placements = 0

    for _ in range(num_attempts):
        if choice == "1": 
            start = random.uniform(0, line_length - car_length)
        elif choice == "2":  
            mean = line_length / 2
            std = line_length / 6  
            start = random.gauss(mean, std)
            start = max(0, min(start, line_length - car_length))
        elif choice == "3":  
            lam = 1 / (line_length / 2)  
            u = random.random()
            x = -math.log(1 - u) / lam
            start = min(x, line_length - car_length)
        else:
            print("Invalid choice. Defaulting to uniform.")
            start = random.uniform(0, line_length - car_length)

        end = start + car_length

        overlap = False
        for car_start in parked_cars:
            car_end = car_start + car_length
            if not (end <= car_start or start >= car_end):
                overlap = True
                break

        if not overlap:
            parked_cars.append(start)
            successful_placements += 1

    
    total_cars_on_line = len(parked_cars)
    density = total_cars_on_line * car_length / line_length
    success_percentage = (successful_placements / num_attempts) * 100


    print("\nResults:")
    print(f"Number of cars on the line: {total_cars_on_line}")
    print(f"Density of cars on the line: {density:.3f}")
    print(f"Number of successful placements: {successful_placements}")
    print(f"Percentage of successful placements: {success_percentage:.2f}%")

    
    plt.figure(figsize=(12, 2))
    for start in parked_cars:
        plt.plot([start, start + car_length], [0, 0], color='blue', linewidth=6)  # car as a thick line
    plt.xlim(0, line_length)
    plt.ylim(-1, 1)
    plt.xlabel("Line Position")
    plt.title("Renyi's Parking Simulation")
    plt.yticks([])
    plt.show()


renyi_parking()