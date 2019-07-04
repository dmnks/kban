import curses


class List(object):
    SCROLLABLE_LEFT = 1
    SCROLLABLE_RIGHT = 2

    def __init__(self):
        self._items = []
        self.size = 0
        self.selected = False

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        self._size = val
        self._viewport = (0, val)
        self.cursor = 0

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, val):
        val = max(0, min(val, len(self) - 1))
        self._cursor = val
        delta = val - self._viewport[0]
        if delta >= self._size:
            self._viewport = (val - self._size + 1, val + 1)
        elif delta < 0:
            self._viewport = (val, val + self._size)

    @property
    def item(self):
        if not self:
            return None
        return self[self.cursor]

    def push(self, item):
        self._items.insert(0, item)

    def pop(self):
        item = self.item
        del self._items[self.cursor]
        self.cursor += 1
        return item

    def __getitem__(self, index):
        return self._items[index]

    @property
    def visible(self):
        start, end = self._viewport
        for i, item in enumerate(self._items[start:end]):
            item.selected = self.selected and (i + start) == self.cursor
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
        win.addstr(y, x, ' ' * self.width, reverse)
        win.addstr(y + 1, x, self.name.center(self.width), reverse)
        for i in range(self.height - 3):
            win.addstr(y + 2 + i, x, ' ' * self.width, reverse)
        if reverse:
            win.addstr(y + (self.height - 1), x, ' ' * self.width,
                       curses.A_REVERSE)


class Column(List):
    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def width(self):
        if not self:
            return 0
        return self[0].width

    def paint(self, win, y, x, title='%s'):
        cur = y
        title = title % self.name
        win.addstr(cur, x, title.center(self.width))
        cur += 1
        if self.scrollable & List.SCROLLABLE_LEFT:
            win.addstr(cur, x, '^' * self.width)
        cur += 1
        for card in self.visible:
            card.paint(win, cur, x)
            cur += card.height
        if self.scrollable & List.SCROLLABLE_RIGHT:
            win.addstr(cur, x, 'v' * self.width)


class Board(List):
    def __init__(self, name, win, y=0, x=0):
        super().__init__()
        self.name = name
        self.win = win
        self.y = y
        self.x = x
        self.selected = True

    @property
    def colwidth(self):
        if not self:
            return 0
        return self[0].width

    @property
    def cardheight(self):
        if not self:
            return 0
        col = self[0]
        if not col:
            return 0
        return col[0].height

    def right(self):
        self.cursor += 1

    def left(self):
        self.cursor -= 1

    def down(self):
        if self.item is not None:
            self.item.cursor += 1

    def up(self):
        if self.item is not None:
            self.item.cursor -= 1

    def promote(self):
        if self.item is None:
            return
        card = self.item.pop()
        self.right()
        self.item.push(card)

    def resize(self):
        my, mx = self.win.getmaxyx()
        self.size = min(mx // self.colwidth, len(self))
        colsize = (my - 3) // self.cardheight
        for column in self:
            column.size = colsize
        self.x = (mx - (self.size * self.colwidth)) // 2

    def paint(self):
        self.win.erase()
        my, mx = self.win.getmaxyx()
        if my < self.cardheight + 4 or mx < self.colwidth + 1:
            return
        cur = self.x
        items = list(self.visible)
        for i, column in enumerate(items):
            title = '%s'
            if i == 0 and self.scrollable & List.SCROLLABLE_LEFT:
                title = '< ' + title
            if i == len(items) - 1 and self.scrollable & List.SCROLLABLE_RIGHT:
                title += ' >'
            column.paint(self.win, self.y, cur, title)
            cur += column.width
        self.win.refresh()
