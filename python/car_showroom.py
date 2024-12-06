import random
import time

class Car:
    def __init__(self, brand, model, year, price, horsepower):
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price
        self.horsepower = horsepower
        self.color = "White"
        self.engine_status = False

    def customize(self, color):
        self.color = color
        print(f"The {self.brand} {self.model} has been painted {self.color}.")

    def toggle_engine(self):
        self.engine_status = not self.engine_status
        state = "ON" if self.engine_status else "OFF"
        print(f"The engine is now {state}.")

    def test_drive(self):
        if not self.engine_status:
            print("The engine is OFF! Start the engine to begin the test drive.")
            return

        print(f"Starting the test drive for {self.brand} {self.model}...")
        for _ in range(3):
            speed = random.randint(20, 120)
            print(f"Speed: {speed} km/h")
            time.sleep(1)
        print("Test drive complete. Hope you enjoyed the ride!")

    def __str__(self):
        return (f"{self.brand} {self.model} ({self.year})\n"
                f"Price: ${self.price}\n"
                f"Horsepower: {self.horsepower} HP\n"
                f"Color: {self.color}\n")

def main():
    cars = [
        Car("Tesla", "Model S", 2024, 79999, 670),
        Car("BMW", "M3", 2023, 69999, 503),
        Car("Toyota", "Supra", 2022, 51999, 382)
    ]

    print("Welcome to the Virtual Car Showroom!")
    while True:
        print("\nAvailable Cars:")
        for i, car in enumerate(cars, 1):
            print(f"{i}. {car.brand} {car.model}")

        choice = input("\nSelect a car by number (or type 'exit' to leave): ")
        if choice.lower() == 'exit':
            print("Thank you for visiting the showroom!")
            break

        if not choice.isdigit() or not (1 <= int(choice) <= len(cars)):
            print("Invalid choice. Try again.")
            continue

        selected_car = cars[int(choice) - 1]
        print(f"\nYou selected:\n{selected_car}")

        while True:
            print("\nOptions:")
            print("1. Customize Color")
            print("2. Start/Stop Engine")
            print("3. Test Drive")
            print("4. View Details")
            print("5. Go Back")

            option = input("Choose an option: ")
            match option:
                case "1":
                    color = input("Enter the desired color: ")
                    selected_car.customize(color)
                case "2":
                    selected_car.toggle_engine()
                case "3":
                    selected_car.test_drive()
                case "4":
                    print(selected_car)
                case "5":
                    print("Returning to car selection...")
                    break
                case _:
                    print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
