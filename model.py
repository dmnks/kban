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

    @property
    def cards(self):
        return self._cards

    def add(self, card):
        card.width = self.width
        self._cards.append(card)

    def paint(self, win, y, x):
        win.addstr(y, x, self.name.center(self.width))
        for i, card in enumerate(self.cards):
            card.paint(win, y + 2 + (i * card.height), x)


class Workflow(object):
    def __init__(self, name):
        self.name = name
        self.columns = []

    def paint(self, win, y, x):
        for i, column in enumerate(self.columns):
            column.paint(win, y, x + (i * (column.width + 2)))
