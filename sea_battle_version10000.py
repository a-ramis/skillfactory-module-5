import random


class BoardOutException(Exception): # ошибка выбора клетки за пределами поля
    pass


class BoardUsedException(Exception): # ошибка выбора использованной клетки
    pass


class Dot: # класс точек на поле
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship: # класс кораблей
    def __init__(self, bow, length, orientation):
        self.bow = bow
        self.length = length
        self.orientation = orientation
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            dot_x = self.bow.x + i * self.orientation[0]
            dot_y = self.bow.y + i * self.orientation[1]
            ship_dots.append(Dot(dot_x, dot_y))
        return ship_dots


class Board: # класс игрового поля
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.board = [["O"] * size for _ in range(size)]
        self.ships = []
        self.busy = []
        self.lives = 0

    def add_ship(self, ship):

        for dot in ship.dots:
            if self.out(dot) or dot in self.busy:
                raise BoardOutException()
        for dot in ship.dots:
            self.board[dot.x][dot.y] = "■"
            self.busy.append(dot)

        self.ships.append(ship)
        self.contour(ship)
        self.lives += ship.length

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dot in ship.dots:
            for dx, dy in near:
                cur = Dot(dot.x + dx, dot.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.board[cur.x][cur.y] = "T"
                    self.busy.append(cur)

    def out(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()

        if dot in self.busy:
            raise BoardUsedException()

        self.busy.append(dot)

        for ship in self.ships:
            if dot in ship.dots:
                ship.lives -= 1
                self.board[dot.x][dot.y] = "X"
                if ship.lives == 0:
                    self.lives -= ship.length
                    self.contour(ship, verb=True)
                    return False, "Корабль уничтожен"
                else:
                    return True, "Корабль ранен"

        self.board[dot.x][dot.y] = "T"
        return False, "Мимо"

    def __str__(self):
        board_view = "   | " + " | ".join(str(i) for i in range(1, self.size + 1)) + " |"
        for i in range(self.size):
            row = " | ".join(self.board[i])
            board_view += f"\n {chr(ord('A') + i)} | {row} |"
        return board_view





class Player: # класс игрока
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat_move, message = self.enemy_board.shot(target)
                print(message)
                return repeat_move
            except BoardOutException:
                print("Выстрел за пределы поля")
            except BoardUsedException:
                print("Эта клетка уже была использована")


class AI(Player): # класс игрока-компьютера
    def ask(self):
        x = random.randint(0, self.board.size - 1)
        y = random.randint(0, self.board.size - 1)
        return Dot(x, y)


class User(Player): # класс игрока-пользователя
    def ask(self):
        while True:
            coordinates = input("Введите координаты выстрела: ")
            try:
                x = int(coordinates[1]) - 1
                y = ord(coordinates[0].upper()) - ord("A")
                return Dot(x, y)
            except (ValueError, IndexError):
                print("Неверный формат ввода координат")


class Game: # класс самой игры
    def __init__(self, size=6):
        self.size = size
        self.enemy_board = Board(hid=True, size=size)
        self.player_board = Board(size=size)
        self.enemy = AI(self.enemy_board, self.player_board)
        self.player = User(self.player_board, self.enemy_board)

    def random_board(self):
        ships = [3, 2, 2, 1, 1, 1, 1]
        while True:
            self.player_board = Board(size=self.size)
            try:
                for length in ships:
                    while True:
                        bow = Dot(random.randint(0, self.size - 1),
                                  random.randint(0, self.size - 1))
                        orientation = random.choice([(1, 0), (0, 1)])
                        ship = Ship(bow, length, orientation)
                        try:
                            self.player_board.add_ship(ship)
                            break
                        except BoardOutException:
                            continue
                break
            except BoardUsedException:
                continue
        while True:
            self.enemy_board = Board(hid=True, size=self.size)
            try:
                for length in ships:
                    while True:
                        bow = Dot(random.randint(0, self.size - 1),
                                  random.randint(0, self.size - 1))
                        orientation = random.choice([(1, 0), (0, 1)])
                        ship = Ship(bow, length, orientation)
                        try:
                            self.enemy_board.add_ship(ship)
                            break
                        except BoardOutException:
                            continue
                break
            except BoardUsedException:
                continue

    def greet(self):
        print("-------------------")
        print("  Морской бой")
        print("-------------------")
        print("Формат ввода координат: A1, B2, C3...")
        print("Количество жизней кораблей игрока:", self.player_board.lives)
        print("Количество жизней кораблей противника:", self.enemy_board.lives)
        print()

    def loop(self):
        num_moves = 0
        while True:
            print("Доска игрока:")
            print(self.player_board)
            print("Доска противника:")
            print(self.enemy_board)
            repeat_move = self.player.move()
            if self.enemy_board.lives == 0:
                print("Вы победили")
                break
            if self.player_board.lives == 0:
                print("Вы проиграли")
                break
            if not repeat_move:
                num_moves += 1
                self.enemy.move()
                print(f"Ход {num_moves}\n")

    def start(self):
        self.random_board()
        self.greet()
        self.loop()


g = Game()
g.start()