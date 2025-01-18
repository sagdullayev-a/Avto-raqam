import json
import os

class CarNumber:
    def __init__(self, number, price, status="Available"):
        self.number = number
        self.price = price
        self.status = status

    def __str__(self):
        return f"Number: {self.number}, Price: {self.price}, Status: {self.status}"

    def to_dict(self):
        return {
            "number": self.number,
            "price": self.price,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return CarNumber(data["number"], data["price"], data["status"])


class User:
    def __init__(self, username, address):
        self.username = username
        self.address = address
        self.purchased_numbers = []

    def __str__(self):
        return f"User: {self.username}, Address: {self.address}"

    def to_dict(self):
        return {
            "username": self.username,
            "address": self.address,
            "purchased_numbers": [number.to_dict() for number in self.purchased_numbers]
        }

    @staticmethod
    def from_dict(data):
        user = User(data["username"], data["address"])
        user.purchased_numbers = [CarNumber.from_dict(n) for n in data["purchased_numbers"]]
        return user


class Sale:
    def __init__(self, car_number, user, date):
        self.car_number = car_number
        self.user = user
        self.date = date

    def __str__(self):
        return f"Car: {self.car_number.number}, Buyer: {self.user.username}, Date: {self.date}"

    def to_dict(self):
        return {
            "car_number": self.car_number.to_dict(),
            "user": self.user.to_dict(),
            "date": self.date
        }

    @staticmethod
    def from_dict(data):
        return Sale(
            CarNumber.from_dict(data["car_number"]),
            User.from_dict(data["user"]),
            data["date"]
        )


def save_data(car_numbers, users, sales):
    with open("data.json", "w") as file:
        json.dump({
            "car_numbers": [number.to_dict() for number in car_numbers],
            "users": [user.to_dict() for user in users],
            "sales": [sale.to_dict() for sale in sales]
        }, file, indent=4)


def load_data():
    if not os.path.exists("data.json"):
        with open("data.json", "w") as file:
            json.dump({"car_numbers": [], "users": [], "sales": []}, file, indent=4)

    with open("data.json", "r") as file:
        data = json.load(file)
        car_numbers = [CarNumber.from_dict(n) for n in data["car_numbers"]]
        users = [User.from_dict(u) for u in data["users"]]
        sales = [Sale.from_dict(s) for s in data["sales"]]
        return car_numbers, users, sales


def main():
    car_numbers, users, sales = load_data()

    while True:
        print("\nWelcome to the Car Number Trading System!")
        choice = input("""
1. Login as Admin
2. Login as User
3. Exit
Select an option: """)

        if choice == "1":
            admin_username = input("Admin username: ")
            admin_password = input("Admin password: ")
            if admin_username == "admin" and admin_password == "admin123":
                print("Successfully logged in as Admin.")
                while True:
                    admin_choice = input("""
1. Add a new car number
2. View car numbers
3. View sales history
4. Exit
Select an option: """)

                    if admin_choice == "1":
                        number = input("Enter the car number: ")
                        price = float(input("Enter the price: "))
                        new_number = CarNumber(number, price)
                        car_numbers.append(new_number)
                        print(f"Car number {number} has been added.")
                        save_data(car_numbers, users, sales)
                    elif admin_choice == "2":
                        for number in car_numbers:
                            print(number)
                    elif admin_choice == "3":
                        for sale in sales:
                            print(sale)
                    elif admin_choice == "4":
                        break
                    else:
                        print("Invalid choice!")
            else:
                print("Incorrect username or password.")

        elif choice == "2":
            user_action = input("""
1. Login with username
2. Create a new user
Select an option: """)

            user = None
            if user_action == "1":
                username = input("Enter your username: ")
                user = next((u for u in users if u.username == username), None)
                if user:
                    print(f"Welcome back, {user.username}!")
                else:
                    print("User not found.")
            elif user_action == "2":
                username = input("Enter a new username: ")
                address = input("Enter your address: ")
                user = User(username, address)
                users.append(user)
                print(f"New user created: {user.username}")
                save_data(car_numbers, users, sales)
            else:
                print("Invalid choice!")

            if user:
                while True:
                    user_choice = input("""
1. View car numbers
2. Purchase a car number
3. View purchased car numbers
4. Exit
Select an option: """)

                    if user_choice == "1":
                        for number in car_numbers:
                            print(number)
                    elif user_choice == "2":
                        number_id = input("Enter the car number to purchase: ")
                        number = next((n for n in car_numbers if n.number == number_id and n.status == "Available"),
                                      None)
                        if number:
                            print(f"Car number {number.number} has been purchased!")
                            number.status = "Sold"
                            user.purchased_numbers.append(number)
                            sales.append(Sale(number, user, "2025-01-09"))
                            save_data(car_numbers, users, sales)
                        else:
                            print("Car number is not available.")
                    elif user_choice == "3":
                        for number in user.purchased_numbers:
                            print(number)
                    elif user_choice == "4":
                        break
                    else:
                        print("Invalid choice!")

        elif choice == "3":
            print("Exiting the system.")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
