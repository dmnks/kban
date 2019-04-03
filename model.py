import curses


class Card(object):
    def __init__(self, name):
        self.name = name
        self.width = 0
        self.height = 4
        self.selected = False

    def paint(self, win, y, x):
        reverse = curses.A_REVERSE if self.selected else 0
        if reverse:
            win.addstr(y, x, '▇' * self.width)
        win.addstr(y + 1, x, self.name.center(self.width), reverse)
        for i in range(self.height - 3):
            win.addstr(y + 2 + i, x, ' ' * self.width, reverse)
        if reverse:
            win.addstr(y + (self.height - 1), x, '▁' * self.width,
                       curses.A_REVERSE)


class Column(object):
    def __init__(self, name, width):
        self.name = name
        self.cursor = 0
        self.selected = False
        self.width = width
        self.viewport = (0, 5)
        self._cards = []

    @property
    def cards(self):
        return self._cards

    def add(self, card):
        card.width = self.width
        self._cards.append(card)

    def _select(self, down):
        cursor = self.cursor
        delta = 1 if down else -1
        vdelta = 0

        cursor += delta
        if cursor == -1 or cursor == len(self._cards):
            return False
        if cursor == self.viewport[0] - 1:
            vdelta = -1
        if cursor == self.viewport[1]:
            vdelta = 1
        if vdelta != 0:
            self.viewport = tuple(map(lambda x: x + vdelta, self.viewport))

        self.cursor = cursor
        return True

    def down(self):
        return self._select(True)

    def up(self):
        return self._select(False)

    def paint(self, win, y, x):
        cur = y
        start, end = self.viewport
        win.addstr(cur, x, self.name.center(self.width))
        cur += 1
        if start > 0:
            win.addstr(cur, x, '▲'.center(self.width))
        cur += 1
        for i, card in enumerate(self._cards[start:end]):
            card.selected = self.selected and (i + start) == self.cursor
            card.paint(win, cur, x)
            cur += card.height
        if end < len(self._cards):
            win.addstr(cur, x, '▼'.center(self.width))


class Workflow(object):
    def __init__(self, name, win, y, x):
        self.name = name
        self.columns = []
        self.cursor = -1

        self.win = win
        self.y = y
        self.x = x

    def _select(self, right):
        cursor = self.cursor
        delta = 1 if right else -1
        # vdelta = 0

        cursor += delta
        if cursor == -1 or cursor == len(self.columns):
            return False
        # if cursor == self.viewport[0] - 1:
        #     vdelta = -1
        # if cursor == self.viewport[1]:
        #     vdelta = 1
        # if vdelta != 0:
        #     self.viewport = tuple(map(lambda x: x + vdelta, self.viewport))

        self.cursor = cursor
        return True

    def right(self):
        return self._select(True)

    def left(self):
        return self._select(False)

    def down(self):
        return self.columns[self.cursor].down()

    def up(self):
        return self.columns[self.cursor].up()

    def paint(self):
        start = 0
        self.win.clear()
        for i, column in enumerate(self.columns):
            column.selected = (i + start) == self.cursor
            column.paint(self.win, self.y, self.x + (i * (column.width + 2)))
