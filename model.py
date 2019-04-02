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
            win.addstr(y, x, '▄' * self.width)
        win.addstr(y + 1, x, self.name.center(self.width), reverse)
        for i in range(self.height - 3):
            win.addstr(y + 2 + i, x, ' ' * self.width, reverse)
        if reverse:
            win.addstr(y + (self.height - 1), x, '▀' * self.width)


class Column(object):
    def __init__(self, name, width):
        self.name = name
        self.width = width
        self._cards = []
        self._cursor = 0

    @property
    def cards(self):
        return self._cards

    def add(self, card):
        card.width = self.width
        self._cards.append(card)

    def _select(self, down):
        delta = 1 if down else -1
        self._cards[self._cursor].selected = False
        self._cursor += delta
        self._cursor %= len(self._cards)
        self._cards[self._cursor].selected = True

    def down(self):
        self._select(True)

    def up(self):
        self._select(False)

    def paint(self, win, y, x):
        win.addstr(y, x, self.name.center(self.width))
        for i, card in enumerate(self.cards):
            card.paint(win, y + 2 + (i * card.height), x)


class Workflow(object):
    def __init__(self, name, win, y, x):
        self.name = name
        self.columns = []

        self.win = win
        self.y = y
        self.x = x

    def paint(self):
        self.win.clear()
        for i, column in enumerate(self.columns):
            column.paint(self.win, self.y, self.x + (i * (column.width + 2)))
