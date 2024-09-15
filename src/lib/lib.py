from random import randint, choice


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length
        self._tp = tp  # Ориенация корабля (1 - горизонтальная, 2 - вертикальная)
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = [1] * length  # Состояние клеток корабля (1 - целая, 0 - подбитая)

    def set_start_cords(self, x, y):
        self._x = x
        self._y = y

    def set_cells(self, i):
        self._cells[i] = 0

    def set_is_move(self):
        self._is_move = False

    def get_start_cords(self):
        return self._x, self._y

    def tp(self):
        return self._tp

    def cells(self):
        return self._cells

    @property
    def length(self):
        return self._length

    def move(self, go):
        if self._is_move:
            if self._tp == 1:
                self._x += go
            else:
                self._y += go

    def is_collide(self, pole):
        """проходится по полю вокруг корабля в поисках единицы"""
        for i in range(-1, self._length + 1):
            for j in range(-1, 2):
                if self._tp == 1:
                    tx, ty = self._x + i, self._y + j
                else:
                    tx, ty = self._x + j, self._y + i

                if 0 <= tx < len(pole) and 0 <= ty < len(pole) and pole[ty][tx] != 0:
                    return True
        return False

    def is_out_pole(self, size):
        if self._tp == 1:
            return not (0 <= self._x < size and 0 <= self._x + self._length - 1 < size)
        else:
            return not (0 <= self._y < size and 0 <= self._y + self._length - 1 < size)


class GamePole:
    def __init__(self, size=10):
        self._size = size  # Размер поля
        self._ships = [Ship(4, randint(1, 2)),
                       Ship(3, randint(1, 2)), Ship(3, randint(1, 2)),
                       Ship(2, randint(1, 2)), Ship(2, randint(1, 2)), Ship(2, randint(1, 2)),
                       Ship(1, randint(1, 2)), Ship(1, randint(1, 2)),
                       Ship(1, randint(1, 2)), Ship(1, randint(1, 2))]
        self._field = [[0] * self._size for _ in range(self._size)]
        self._count_ships = len(self._ships)
        self._opponent_field = [[0] * self._size for _ in range(self._size)]
        self.set_random_positions()

    @property
    def count_ships(self):
        return self._count_ships

    def set_random_positions(self):  # расставляет координаты сразу так, чтобы корабль не выходил за пределы поля
        for ship in self._ships:  # далее проверят на столкновения с другим кораблем, если тру - то выбор других х,у
            while True:  # добавляет корабль на поле
                if ship.tp() == 1:
                    x, y = randint(0, self._size - ship.length), randint(0, self._size - 1)
                else:
                    x, y = randint(0, self._size - 1), randint(0, self._size - ship.length)

                ship.set_start_cords(x, y)
                if not ship.is_collide(self._field):
                    break

            self.place_ship(ship)

    def place_ship(self, ship):
        # self._pole = [[0] * self._size for _ in range(self._size)]
        x, y = ship.get_start_cords()
        cells = ship.cells()
        for i in range(ship.length):
            if ship.tp() == 1:
                self._field[y][x + i] = cells[i]
            else:
                self._field[y + i][x] = cells[i]

    def zeroing_ship(self, ship):
        """зануление корабля при перемещении чтобы при проверке столкновения он не сталкивался сам с собой
         (после перемещения заново отрисовывается)"""

        x, y = ship.get_start_cords()
        for i in range(ship.length):
            if ship.tp() == 1:
                self._field[y][x + i] = 0
            else:
                self._field[y + i][x] = 0

    def move_ships(self):
        for ship in self._ships:
            go = choice([-1, 1])
            self.zeroing_ship(ship)
            ship.move(go)
            if ship.is_out_pole(self._size) or ship.is_collide(self._field):
                ship.move(-go)  # Возврат в исходное положение при столкновении или выходе за границы поля
            self.place_ship(ship)

    def attack_ship(self, ax, ay):
        if self._field[ay][ax] == 1:
            for ship in self._ships:
                sx, sy = ship.get_start_cords()
                for i in range(ship.length):
                    if (ax, ay) == (sx + i, sy) or (ax, ay) == (sx, sy + i):
                        ship.set_cells(i)
                        ship.set_is_move()
                        self._opponent_field[ay][ax] = 'x'
                        if not any(ship.cells()):
                            self.death_ship(ship, ax, ay)
                        return True
        else:
            self._opponent_field[ay][ax] = '*'

    def death_ship(self, ship, ax, ay):
        self._count_ships -= 1
        for i in range(-1, ship.length + 1):
            for j in range(-1, 2):
                if ship.tp() == 1:
                    tx, ty = ax + i - ship.length + 1, ay + j
                else:
                    tx, ty = ax + j, ay + i - ship.length + 1

                if 0 <= tx < self._size and 0 <= ty < self._size:
                    self._opponent_field[ty][tx] = '*'

    def show(self):
        print()
        for row in self._field:
            print('  '.join(map(str, row)))

    def opponent_field_show(self):
        print()
        for row in self._opponent_field:
            print('  '.join(map(str, row)))
