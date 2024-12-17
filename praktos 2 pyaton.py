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


        self.admin.add_item(Item("AK-47 | Redline", 15.99, "Rare"))
        self.admin.add_item(Item("AWP | Dragon Lore", 150.0, "Legendary"))
        self.admin.add_item(Item("AWP | Asiimov", 1000.0, "Rare"))
        self.admin.add_item(Item("AK-47 | Legion", 125.99, "Epic"))
        self.admin.add_item(Item("Desert Eagle | Crimson Web", 25.99, "Epic"))
        self.admin.add_item(Item("Desert Eagle | Blaze", 54.99, "Rare"))
        self.admin.add_item(Item("Karambit | Crimson Web", 200.0, "Legendary"))
        self.admin.add_item(Item("Karambit | Tiger Tooth", 125.0, "Legendary"))
        self.admin.add_item(Item("M4A1-S | Nightmare ", 99.99, "Epic"))
    def filter_items(self, rarity=None, name_contains=None, price_min=None, price_max=None):
        try:
            filtered_items = self.admin.items


            if rarity:
                filtered_items = list(filter(lambda item: item.rarity == rarity, filtered_items))


            if name_contains:
                filtered_items = list(filter(lambda item: name_contains.lower() in item.name.lower(), filtered_items))


            if price_min is not None or price_max is not None:
                filtered_items = list(filter(lambda item: (price_min is None or item.price >= price_min) and
                                                          (price_max is None or item.price <= price_max),
                                             filtered_items))

            print("Отфильтрованные товары:")
            if filtered_items:
                for item in filtered_items:
                    print(item)
            else:
                print("Товары не найдены.")
        except Exception as e:
            print(f"Произошла ошибка при фильтрации: {e}")

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
            print("Административное меню:")
            print("1. Добавить товар")
            print("2. Удалить товар")

            print("4. Показать товары")
            print("5. Фильтровать товары")
            print("0. Выйти")
            choice = input("Выберите опцию: ")

            if choice == '1':
                name = input("Введите имя товара: ")
                price = float(input("Введите цену товара: "))
                rarity = input("Введите редкость товара: ")
                self.admin.add_item(Item(name, price, rarity))
                print(f"Товар {name} добавлен.")
            elif choice == '2':
                name = input("Введите имя товара, который хотите удалить: ")
                item_to_remove = next((item for item in self.admin.items if item.name == name), None)
                if item_to_remove:
                    self.admin.remove_item(item_to_remove)
                    print(f"Товар {name} удалён.")
                else:
                    print("Товар не найден.")
            elif choice == '3':
                name = input("Введите имя товара, который хотите изменить: ")
                item_to_modify = next((item for item in self.admin.items if item.name == name), None)
                if item_to_modify:
                    new_name = input("Введите новое имя товара: ")
                    new_price = float(input("Введите новую цену товара: "))
                    new_rarity = input("Введите новую редкость товара: ")
                    new_item = Item(new_name, new_price, new_rarity)
                    self.admin.modify_item(item_to_modify, new_item)
                    print(f"Товар {item_to_modify.name} изменён на {new_item.name}.")
                else:
                    print("Товар не найден.")
            elif choice == '4':
                self.show_items()
            elif choice == '5':
                try:
                    rarity = input("Введите редкость для фильтрации (или оставьте пустым): ")
                    name_contains = input("Введите часть имени товара для фильтрации (или оставьте пустым): ")
                    price_min = input("Введите минимальную цену (или оставьте пустым): ")
                    price_max = input("Введите максимальную цену (или оставьте пустым): ")

                    price_min = float(price_min) if price_min else None
                    price_max = float(price_max) if price_max else None

                    self.filter_items(
                        rarity if rarity else None,
                        name_contains if name_contains else None,
                        price_min,
                        price_max
                    )
                except ValueError:
                    print("Ошибка: введены неверные данные для цены.")
            elif choice == '0':
                break

    def user_menu(self):
        while True:
            print("Пользовательское меню:")
            print("1. Показать все товары")
            print("2. Фильтровать товары")
            print("3. Купить товар")
            print("4. Посмотреть историю покупок")
            print("0. Выйти")
            choice = input("Выберите опцию: ")

            if choice == '1':
                self.show_items()
            elif choice == '2':
                try:
                    rarity = input("Введите редкость для фильтрации (или оставьте пустым): ")
                    name_contains = input("Введите часть имени товара для фильтрации (или оставьте пустым): ")
                    price_min = input("Введите минимальную цену (или оставьте пустым): ")
                    price_max = input("Введите максимальную цену (или оставьте пустым): ")

                    price_min = float(price_min) if price_min else None
                    price_max: Any | None = float(price_max) if price_max else None

                    self.filter_items(
                        rarity if rarity else None,
                        name_contains if name_contains else None,
                        price_min,
                        price_max)

                except ValueError:
                    print("Ошибка: введены неверные данные для цены.")
            elif choice == '3':
                item_name = input("Введите имя товара, который хотите купить: ")
                self.buy_item(item_name)
            elif choice == '4':
                print("Ваша история покупок:")
                if self.current_user.history:
                    for item in self.current_user.history:
                        print(item)
                else:
                    print("У вас нет купленных товаров.")
            elif choice == '0':
                break

def main():
    marketplace = Marketplace()

    while True:
        print("Главное меню:")
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
