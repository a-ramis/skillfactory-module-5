def greet():  # Функция приветствия
    print("---------------------")
    print("   Приветсвуем вас   ")
    print("       в игре        ")
    print("   крестики-нолики   ")
    print("---------------------")
    print("    формат ввода:    ")
    print("номер строки -> Enter")
    print("номер столбца-> Enter")


def print_field():  # Функция печати поля
    for i in field:
        print(*i, sep='\t')


def one_move(t):  # Функция ввода
    x = input(f'Введите координаты {t} по вертикали: ')
    y = input(f'Введите координаты {t} по горизонтали: ')
    if not (x.isdigit()) or not (y.isdigit()):
        print('Вводите натуральные числа, по одному за раз!')
        return one_move(t)
    x, y = int(x), int(y)
    if 0 < x < 4 and 0 < y < 4:
        if field[x][y] == '-':
            field[x][y] = t
        else:
            print('Эта клетка занята! Введите другие координаты!')
            return one_move(t)
    else:
        print('Координаты вне диапазона игрового поля! Введите другие координаты!')
        return one_move(t)


def check_win():  # Функция проверки на победу
    win_cord = (((1, 1), (1, 2), (1, 3)), ((2, 1), (2, 2), (2, 3)), ((3, 1), (3, 2), (3, 3)),
                ((1, 1), (2, 1), (3, 1)), ((1, 2), (2, 2), (3, 2)), ((1, 3), (2, 3), (3, 3)),
                ((1, 1), (2, 2), (3, 3)), ((1, 3), (2, 2), (3, 1)))
    for cord in win_cord:
        symbols = []
        for c in cord:
            symbols.append(field[c[0]][c[1]])
        if symbols == ["X", "X", "X"]:
            print("Выиграл X!!!")
            return True
        if symbols == ["0", "0", "0"]:
            print("Выиграл 0!!!")
            return True
    return False

greet()
field = [
    [' ', 1, 2, 3],
    [1, '-', '-', '-'],
    [2, '-', '-', '-'],
    [3, '-', '-', '-']
]
print_field()
count = 0
while True:
    count += 1
    if count % 2 == 1:
        one_move('X')
    if count % 2 == 0:
        one_move('0')
    print_field()
    if check_win():
        break
    if count == 9:
        print('Игра закончилась ничьей!')
        break