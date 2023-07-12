while True:
    user_input = input("Введите число: ")
    try:
        number = float(user_input)  # преобразуем введенную строку в число с плавающей точкой
        break  # если преобразование прошло успешно, выходим из цикла
    except ValueError:
        print("Ошибка: введено некорректное число. Попробуйте снова.")

print("Вы ввели число:", number)