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
        print("\nAvtomobil raqamlari savdo tizimiga xush kelibsiz!")
        choice = input("""
1. Admin sifatida tizimga kirish
2. Foydalanuvchi sifatida tizimga kirish
3. Chiqish
Kerakli bo'limni tanlang: """)

        if choice == "1":
            admin_username = input("Admin login: ")
            admin_password = input("Admin parol: ")
            if admin_username == "admin" and admin_password == "admin123":
                print("Admin sifatida tizimga muvaffaqiyatli kirdingiz.")
                while True:
                    admin_choice = input("""
1. Yangi avtomobil raqami qo'shish
2. Avtomobil raqamlarini ko'rish
3. Sotuvlar tarixini ko'rish
4. Chiqish
Kerakli bo'limni tanlang: """)

                    if admin_choice == "1":
                        number = input("Avtomobil raqamini kiriting: ")
                        price = float(input("Narxni kiriting: "))
                        new_number = CarNumber(number, price)
                        car_numbers.append(new_number)
                        print(f"Avtomobil raqami {number} qo'shildi.")
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
                        print("Noto'g'ri tanlov!")
            else:
                print("Login yoki parol noto'g'ri.")

        elif choice == "2":
            user_action = input("""
1. Username orqali tizimga kirish
2. Yangi foydalanuvchi yaratish
Kerakli bo'limni tanlang: """)

            user = None
            if user_action == "1":
                username = input("Username-ni kiriting: ")
                user = next((u for u in users if u.username == username), None)
                if user:
                    print(f"Xush kelibsiz, {user.username}!")
                else:
                    print("Foydalanuvchi topilmadi.")
            elif user_action == "2":
                username = input("Yangi username kiriting: ")
                address = input("Manzilingizni kiriting: ")
                user = User(username, address)
                users.append(user)
                print(f"Yangi foydalanuvchi yaratildi: {user.username}")
                save_data(car_numbers, users, sales)
            else:
                print("Noto'g'ri tanlov!")

            if user:
                while True:
                    user_choice = input("""
1. Avtomobil raqamlarini ko'rish
2. Avtomobil raqamini sotib olish
3. Sotib olingan raqamlarni ko'rish
4. Chiqish
Kerakli bo'limni tanlang: """)

                    if user_choice == "1":
                        for number in car_numbers:
                            print(number)
                    elif user_choice == "2":
                        number_id = input("Sotib olish uchun avtomobil raqamini kiriting: ")
                        number = next((n for n in car_numbers if n.number == number_id and n.status == "Available"),
                                      None)
                        if number:
                            print(f"Avtomobil raqami {number.number} sotib olindi!")
                            number.status = "Sold"
                            user.purchased_numbers.append(number)
                            sales.append(Sale(number, user, "2025-01-09"))
                            save_data(car_numbers, users, sales)
                        else:
                            print("Avtomobil raqami mavjud emas.")
                    elif user_choice == "3":
                        for number in user.purchased_numbers:
                            print(number)
                    elif user_choice == "4":
                        break
                    else:
                        print("Noto'g'ri tanlov!")

        elif choice == "3":
            print("Tizimdan chiqildi.")
            break
        else:
            print("Noto'g'ri tanlov!")

if __name__ == "__main__":
    main()
