class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
        self.history = []

    def buy_item(self, item):
        self.history.append(item)

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, role='admin')
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def modify_item(self, item, new_item):
        index = self.items.index(item)
        self.items[index] = new_item

class Item:
    def __init__(self, name, price, rarity):
        self.name = name
        self.price = price
        self.rarity = rarity

    def __str__(self):
        return f"{self.name} (Price: {self.price}, Rarity: {self.rarity})"

class Marketplace:
    def __init__(self):
        self.users = []
        self.admin = Admin("admin", "admin123")
        self.current_user = None

        # Default admin items
        self.admin.add_item(Item("AK-47 | Redline", 15.99, "Rare"))
        self.admin.add_item(Item("AWP | Dragon Lore", 150.0, "Legendary"))

    def register_user(self, username, password):
        if any(user.username == username for user in self.users):
            print("Пользователь с таким именем уже существует!")
        else:
            self.users.append(User(username, password, role='user'))
            print(f"Пользователь {username} успешно зарегистрирован!")

    def login(self, username, password):
        if username == self.admin.username and password == self.admin.password:
            self.current_user = self.admin
            print("Вход выполнен как администратор.")
            return True

        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                print(f"Вход выполнен как пользователь {username}.")
                return True

        print("Неправильное имя пользователя или пароль.")
        return False

    def show_items(self):
        print("Доступные товары:")
        for item in self.admin.items:
            print(item)

    def buy_item(self, item_name):
        for item in self.admin.items:
            if item.name == item_name:
                self.current_user.buy_item(item)
                print(f"Вы купили: {item}")
                return
        print("Товар не найден!")

    def admin_menu(self):
        while True:
            print("\nАдминистративное меню:")
            print("1. Добавить товар")
            print("2. Удалить товар")
            print("3. Изменить товар")
            print("4. Показать товары")
            print("0. Выйти")
            choice = input("Выберите опцию: ")

            if choice == '1':
                name = input("Введите имя товара: ")
                price = float(input("Введите цену товара: "))
                rarity = input("Введите редкость товара: ")
                self.admin.add_item(Item(name, price, rarity))
            elif choice == '2':
                name = input("Введите имя товара, который хотите удалить: ")
                item_to_remove = next((item for item in self.admin.items if item.name == name), None)
                if item_to_remove:
                    self.admin.remove_item(item_to_remove)
                    print(f"Товар {name} удален.")
                else:
                    print("Товар не найден.")
            elif choice == '3':
                name = input("Введите имя товара, который хотите изменить: ")
                item_to_modify = next((item for item in self.admin.items if item.name == name), None)
                if item_to_modify:
                    new_name = input("Введите новое имя товара: ")
                    new_price = float(input("Введите новую цену товара: "))
                    new_rarity = input("Введите новую редкость товара: ")
                    self.admin.modify_item(item_to_modify, Item(new_name, new_price, new_rarity))
                    print(f"Товар {name} изменен.")
                else:
                    print("Товар не найден.")
            elif choice == '4':
                self.show_items()
            elif choice == '0':
                break

    def user_menu(self):
        while True:
            print("\nПользовательское меню:")
            print("1. Показать товары")
            print("2. Купить товар")
            print("3. Посмотреть историю покупок")
            print("0. Выйти")
            choice = input("Выберите опцию: ")

            if choice == '1':
                self.show_items()
            elif choice == '2':
                item_name = input("Введите имя товара, который хотите купить: ")
                self.buy_item(item_name)
            elif choice == '3':
                print("Ваша история покупок:")
                for item in self.current_user.history:
                    print(item)
            elif choice == '0':
                break

def main():
    marketplace = Marketplace()

    while True:
        print("\nГлавное меню:")
        print("1. Регистрация")
        print("2. Вход")
        print("0. Выход")
        choice = input("Выберите опцию: ")

        if choice == '1':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            marketplace.register_user(username, password)
        elif choice == '2':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            if marketplace.login(username, password):
                if marketplace.current_user.role == 'admin':
                    marketplace.admin_menu()
                else:
                    marketplace.user_menu()
        elif choice == '0':
            break

if __name__ == "__main__":
    main()