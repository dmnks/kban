import curses


class List(object):
    SCROLLABLE_LEFT = 1
    SCROLLABLE_RIGHT = 2

    def __init__(self, items=None, size=5):
        if items is None:
            items = []
        self._items = items
        self.size = size
        self.cursor = 0
        self.selected = False

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        self._size = val
        self._viewport = (0, val)

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, val):
        val = max(0, min(val, len(self) - 1))
        self._cursor = val
        delta = val - self._viewport[0]
        if delta >= self.size:
            self._viewport = (val - self.size + 1, val + 1)
        elif delta < 0:
            self._viewport = (val, val + self.size)

    @property
    def selected(self):
        if not self:
            return None
        return self._items[self.cursor]

    @selected.setter
    def selected(self, val):
        self._selected = val

    def __iter__(self):
        start, end = self._viewport
        for i, item in enumerate(self._items[start:end]):
            item.selected = self._selected and (i + start) == self.cursor
            yield item

    def __len__(self):
        return len(self._items)

    @property
    def scrollable(self):
        flags = 0
        start, end = self._viewport
        if start > 0:
            flags = List.SCROLLABLE_LEFT
        if end < len(self):
            flags |= List.SCROLLABLE_RIGHT
        return flags


class Card(object):
    def __init__(self, name, width=25, height=4):
        self.name = name
        self.width = width
        self.height = height
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


class Column(List):
    def __init__(self, name, width=25, size=5):
        self.name = name
        self.width = width
        super().__init__(size=size)

    def add(self, card):
        card.width = self.width
        self._items.append(card)

    def paint(self, win, y, x, title='%s'):
        cur = y
        title = title % self.name
        win.addstr(cur, x, title.center(self.width))
        cur += 1
        if self.scrollable & List.SCROLLABLE_LEFT:
            win.addstr(cur, x, '▲'.center(self.width))
        cur += 1
        for card in self:
            card.paint(win, cur, x)
            cur += card.height
        if self.scrollable & List.SCROLLABLE_RIGHT:
            win.addstr(cur, x, '▼'.center(self.width))


class Board(List):
    def __init__(self, name, win, y=0, x=0, colwidth=25):
        self.name = name
        self.win = win
        self.y = y
        self.x = x
        self.colwidth = colwidth
        super().__init__()
        self.selected = True

    def add(self, column):
        column.width = self.colwidth
        self._items.append(column)

    def right(self):
        self.cursor += 1

    def left(self):
        self.cursor -= 1

    def down(self):
        if self.selected is not None:
            self.selected.cursor += 1

    def up(self):
        if self.selected is not None:
            self.selected.cursor -= 1

    def resize(self):
        maxy, maxx = self.win.getmaxyx()
        self.size = min(maxx // self.colwidth, len(self))
        colheight = (maxy - 3) // 4
        for column in self:
            column.size = colheight
            for card in column:
                card.height = 4

        self.x = (maxx - (self.size * self.colwidth)) // 2

    def paint(self):
        self.win.erase()
        maxy, maxx = self.win.getmaxyx()
        if maxy < 4 + 4 or maxx < self.colwidth + 1:
            return
        cur = self.x
        items = list(self)
        for i, column in enumerate(items):
            title = '%s'
            if i == 0 and self.scrollable & List.SCROLLABLE_LEFT:
                title = '◀ ' + title
            if i == len(items) - 1 and self.scrollable & List.SCROLLABLE_RIGHT:
                title += ' ▶'
            column.paint(self.win, self.y, cur, title)
            cur += column.width
        self.win.refresh()
