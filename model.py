class Card(object):
    def __init__(self, name):
        self.name = name
        self.width = 0
        self.height = 4

    def paint(self, win, y, x):
        w = self.width - 2
        box = ['┌' + '─' * w + '┐',
               '│' + self.name.center(w) + '│']
        box += ['│' + ' ' * w + '│'] * (self.height - 3)
        box += ['└' + '─' * w + '┘']
        for i, line in enumerate(box):
            win.addstr(y + i, x, line)


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
            column.paint(win, y, x + (i * column.width))
