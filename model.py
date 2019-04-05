import curses


class List(object):
    def __init__(self, items=None, height=5):
        if items is None:
            items = []
        self._items = items
        self.height = height
        self.cursor = 0
        self.selected = False

    def _select(self, down):
        cursor = self.cursor
        delta = 1 if down else -1
        vdelta = 0

        cursor += delta
        if cursor == -1 or cursor == len(self._items):
            return False
        if cursor == self.viewport[0] - 1:
            vdelta = -1
        if cursor == self.viewport[1]:
            vdelta = 1
        if vdelta != 0:
            self.viewport = tuple(map(lambda x: x + vdelta, self.viewport))

        self.cursor = cursor
        return True

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        self._height = val
        self.viewport = (0, val)

    def down(self):
        return self._select(True)

    def up(self):
        return self._select(False)

    @property
    def item(self):
        return self._items[self.cursor]

    @property
    def items(self):
        start, end = self.viewport
        for i, item in enumerate(self._items[start:end]):
            item.selected = self.selected and (i + start) == self.cursor
            yield item

    @property
    def scrollable(self):
        code = 0
        start, end = self.viewport
        if start > 0:
            code = 1
        if end < len(self._items):
            code += 2
        return code


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
    def __init__(self, name, width=25, height=5):
        self.name = name
        self.width = width
        super().__init__(height=height)

    def add(self, card):
        card.width = self.width
        self._items.append(card)

    def paint(self, win, y, x, title='%s'):
        cur = y
        title = title % self.name
        win.addstr(cur, x, title.center(self.width))
        cur += 1
        if self.scrollable % 2:
            win.addstr(cur, x, '▲'.center(self.width))
        cur += 1
        for card in self.items:
            card.paint(win, cur, x)
            cur += card.height
        if self.scrollable > 1:
            win.addstr(cur, x, '▼'.center(self.width))


class Board(List):
    def __init__(self, name, win, y=0, x=0, width=25):
        self.name = name
        self.win = win
        self.y = y
        self.x = x
        self._card_height = 4
        self.width = width
        super().__init__()
        self.selected = True

    def add(self, column):
        self._items.append(column)

    def right(self):
        return super().down()

    def left(self):
        return super().up()

    def down(self):
        return self.item.down()

    def up(self):
        return self.item.up()

    def resize(self):
        self.height = curses.COLS // self.width
        col_height = (curses.LINES - 3) // self._card_height
        for column in self._items:
            column.width = self.width
            column.height = col_height
            for card in column._items:
                card.height = self._card_height

    def paint(self):
        self.win.clear()
        cur = self.x
        items = list(self.items)
        if not items:
            return

        items[0].paint(self.win, self.y, cur,
                       '◀ %s' if self.scrollable % 2 else '%s')
        cur += items[0].width

        for column in items[1:-1]:
            column.paint(self.win, self.y, cur)
            cur += column.width

        # TODO CONTINUE HERE: fix 1-column case
        if len(items) > 1:
            items[-1].paint(self.win, self.y, cur,
                            '%s ▶' if self.scrollable > 1 else '%s')
