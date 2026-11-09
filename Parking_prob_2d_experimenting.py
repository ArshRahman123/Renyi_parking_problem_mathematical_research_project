import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def renyi_parking_2d_fixed_size(lot_width, lot_height, car_length, car_width,
                                distribution="uniform", alpha=5.0):
    """
    2D Renyi parking with adaptive stopping rule:
    Stop when failed_attempts > alpha * number_of_parked_cars
    Normal and Exponential distributions are adaptive to lot size.
    """

    parked = []
    failed_attempts = 0

    usable_width = lot_width - car_length
    usable_height = lot_height - car_width

    while True:

        # Adaptive stopping condition
        if len(parked) > 0 and failed_attempts > alpha * len(parked):
            break

        # -----------------------------
        # Generate position
        # -----------------------------

        if distribution == "uniform":
            x_start = random.uniform(0, usable_width)
            y_start = random.uniform(0, usable_height)

        elif distribution == "normal":
            beta = 0.2  # controls center clustering (smaller = tighter)

            sigma_x = beta * usable_width
            sigma_y = beta * usable_height

            while True:
                x_start = random.gauss(usable_width / 2, sigma_x)
                if 0 <= x_start <= usable_width:
                    break

            while True:
                y_start = random.gauss(usable_height / 2, sigma_y)
                if 0 <= y_start <= usable_height:
                    break

        elif distribution == "exponential":
            beta = 0.1  # controls corner clustering (smaller = stronger bias)

            lam_x = 1.0 / (beta * usable_width)
            lam_y = 1.0 / (beta * usable_height)

            while True:
                x_start = random.expovariate(lam_x)
                if 0 <= x_start <= usable_width:
                    break

            while True:
                y_start = random.expovariate(lam_y)
                if 0 <= y_start <= usable_height:
                    break

        else:
            raise ValueError("Distribution must be 'uniform', 'normal', or 'exponential'")

        new_car = (x_start, y_start, car_length, car_width)

        # -----------------------------
        # Overlap check
        # -----------------------------

        overlap = False
        for px, py, pl, pw in parked:
            if not (x_start + car_length <= px or x_start >= px + pl or
                    y_start + car_width <= py or y_start >= py + pw):
                overlap = True
                break

        if not overlap:
            parked.append(new_car)
            failed_attempts = 0
        else:
            failed_attempts += 1

    return parked


def plot_parking_2d(parked, lot_width, lot_height):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, lot_width)
    ax.set_ylim(0, lot_height)
    ax.set_aspect('equal')

    ax.add_patch(
        patches.Rectangle((0, 0), lot_width, lot_height,
                          linewidth=2, edgecolor='black', facecolor='none')
    )

    for x, y, length, width in parked:
        ax.add_patch(
            patches.Rectangle((x, y), length, width,
                              facecolor='blue', edgecolor='black', alpha=0.7)
        )

    plt.title("2D Renyi Parking Simulation (Adaptive Stop)")
    plt.xlabel("X (width)")
    plt.ylabel("Y (height)")
    plt.show()


if __name__ == "__main__":

    lot_width = float(input("Enter parking lot width (x-direction): "))
    lot_height = float(input("Enter parking lot height (y-direction): "))
    car_length = float(input("Enter car length: "))
    car_width = float(input("Enter car width: "))
    distribution = input("Choose distribution (uniform/normal/exponential): ").strip().lower()

    if car_length > lot_width or car_width > lot_height:
        print("Error: Car dimensions exceed parking lot dimensions!")
    else:
        parked = renyi_parking_2d_fixed_size(
            lot_width=lot_width,
            lot_height=lot_height,
            car_length=car_length,
            car_width=car_width,
            distribution=distribution,
            alpha=0.5
        )

        total_car_area = len(parked) * car_length * car_width
        lot_area = lot_width * lot_height
        density = total_car_area / lot_area

        print(f"\nNumber of parked cars: {len(parked)}")
        print(f"Density of parked cars: {density:.4f}")

        plot_parking_2d(parked, lot_width, lot_height)
