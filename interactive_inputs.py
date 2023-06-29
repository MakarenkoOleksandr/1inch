from wallet_balance.get_tokens_data import get_tokens_data


def interactive_inputs():

    while True:
        # Выводим меню действий
        print("Выберите действие:")
        print("1. Проверить баланс кошелька")
        print("2. Обмен монет")

        choice = input("Введите номер действия: ")

        if choice == "1":
            get_tokens_data()
            break

        elif choice == "2":
            print("Вы выбрали действие 2.")
            # Здесь можно добавить код для выполнения действия 2
            break

        elif choice == "3":
            print("До свидания!")
            break

        else:
            print("Неверный ввод. Попробуйте ещё раз.")

    return choice
