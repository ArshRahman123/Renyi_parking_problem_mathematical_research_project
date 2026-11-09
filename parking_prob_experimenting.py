import random
import matplotlib.pyplot as plt

def renyi_parking(L, distribution="uniform", alpha=5.0):
    """
    1D Renyi parking on interval [0, L] with fixed car length = 1.

    Adaptive stopping rule:
        Stop when failed_attempts > alpha * number_of_parked_cars

    Distributions are scale-adaptive.
    """

    car_length = 1
    usable_length = L - car_length

    parked = []
    failed_attempts = 0

    while True:

        if len(parked) > 0 and failed_attempts > alpha * len(parked):
            break

        if distribution == "uniform":
            start = random.uniform(0, usable_length)

        elif distribution == "normal":
            beta = 1  

            sigma = beta * usable_length

            while True:
                start = random.gauss(usable_length / 2, sigma)
                if 0 <= start <= usable_length:
                    break

        elif distribution == "exponential":
            beta = 0.25  

            lam = 1.0 / (beta * usable_length)

            while True:
                start = random.expovariate(lam)
                if 0 <= start <= usable_length:
                    break

        else:
            raise ValueError("Unknown distribution: choose 'uniform', 'normal', or 'exponential'")

        end = start + car_length

        overlap = False
        for s, e in parked:
            if not (end <= s or start >= e):
                overlap = True
                break

        if not overlap:
            parked.append((start, end))
            failed_attempts = 0
        else:
            failed_attempts += 1

    return sorted(parked)


def plot_parking(parked, L):
    plt.figure(figsize=(12, 2))

    plt.hlines(0, 0, L, color="black")

    for s, e in parked:
        plt.hlines(0, s, e, linewidth=10, color="blue")

    plt.xlim(0, L)
    plt.yticks([])
    plt.title("1D Renyi Parking (Adaptive Stop)")
    plt.xlabel("Position along line")
    plt.show()


if __name__ == "__main__":

    L = float(input("Enter total line length: "))
    distribution = input("Choose distribution (uniform/normal/exponential): ").strip().lower()

    parked = renyi_parking(
        L=L,
        distribution=distribution,
        alpha=0.5   
    )

    num_cars = len(parked)
    density = num_cars / L

    print("Number of parked cars:", num_cars)
    print("Density of cars: {:.4f}".format(density))

    plot_parking(parked, L=L)
