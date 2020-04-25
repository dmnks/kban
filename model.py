import curses

CARD_WIDTH = 25
CARD_HEIGHT = 4


class List(object):
    SCROLLABLE_LEFT = 1
    SCROLLABLE_RIGHT = 2

    def __init__(self):
        self._items = []
        self._cursor = 0
        self._viewport = (0, 0)
        self.selected = False

    @property
    def size(self):
        return self._viewport[1]

    @size.setter
    def size(self, val):
        self._viewport = (0, val)
        if self._cursor not in range(self._viewport[1]):
            self._cursor = self._viewport[1] - 1

    def next(self):
        if (self._cursor == len(self) - 1):
            return
        self._cursor += 1
        if (self._cursor == self._viewport[1]):
            self._viewport = tuple(map(lambda x: x + 1, self._viewport))

    def prev(self):
        if (self._cursor == 0):
            return
        self._cursor -= 1
        if (self._cursor < self._viewport[0]):
            self._viewport = tuple(map(lambda x: x - 1, self._viewport))

    @property
    def offset(self):
        return self._cursor - self._viewport[0]

    @offset.setter
    def offset(self, val):
        self._cursor = max(0, min(self._viewport[0] + val,
                                  self._viewport[1] - 1,
                                  len(self) - 1))

    @property
    def current(self):
        if not self._items:
            return None
        return self[self._cursor]

    def push(self, item):
        self._items.insert(0, item)

    def pop(self):
        item = self.current
        if item is None:
            return None
        del self._items[self._cursor]
        if self._cursor == len(self):
            self.prev()
        return item

    def __getitem__(self, index):
        return self._items[index]

    def __iter__(self):
        start, end = self._viewport
        for i, item in enumerate(self._items[start:end]):
            item.selected = self.selected and (i + start) == self._cursor
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
    def __init__(self, name):
        self.name = name
        self.width = CARD_WIDTH
        self.height = CARD_HEIGHT
        self.selected = False

    def paint(self, win, y, x):
        attr = curses.A_REVERSE if self.selected else 0
        win.addstr(y, x, self.name.center(self.width), attr)
        for i in range(self.height):
            win.addstr(y + 1 + i, x, ' ' * self.width, attr)


class Column(List):
    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def width(self):
        return CARD_WIDTH

    def paint(self, win, y, x, title='%s'):
        cur = y
        title = ' %s ' % (title % self.name)
        win.addstr(cur, x + ((self.width - len(title)) // 2), title,
                   curses.A_REVERSE if self.selected else 0)
        cur += 1
        if self.scrollable & List.SCROLLABLE_LEFT:
            win.addstr(cur, x, '^' * self.width)
        cur += 1
        for card in self:
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
        return CARD_WIDTH

    @property
    def cardheight(self):
        return CARD_HEIGHT

    def right(self):
        offset = self.current.offset
        self.next()
        self.current.offset = offset

    def left(self):
        offset = self.current.offset
        self.prev()
        self.current.offset = offset

    def down(self):
        if self.current is not None:
            self.current.next()

    def up(self):
        if self.current is not None:
            self.current.prev()

    def promote(self):
        if self.current is None:
            return
        card = self.current.pop()
        self.right()
        if card is None:
            return
        self.current.push(card)
        self.current.offset = 0

    def denote(self):
        if self.current is None:
            return
        card = self.current.pop()
        self.left()
        if card is None:
            return
        self.current.push(card)
        self.current.offset = 0

    def resize(self):
        my, mx = self.win.getmaxyx()
        self.size = min(mx // self.colwidth, len(self))
        colsize = (my - 3) // self.cardheight
        for column in self._items:
            column.size = colsize
        self.x = (mx - (self.size * self.colwidth)) // 2

    def paint(self):
        self.win.erase()
        my, mx = self.win.getmaxyx()
        if my < self.cardheight + 4 or mx < self.colwidth + 1:
            return
        cur = self.x
        items = list(self)
        for i, column in enumerate(items):
            title = '%s'
            if i == 0 and self.scrollable & List.SCROLLABLE_LEFT:
                title = '< ' + title
            if i == len(items) - 1 and self.scrollable & List.SCROLLABLE_RIGHT:
                title += ' >'
            column.paint(self.win, self.y, cur, title)
            cur += column.width + 2
        self.win.refresh()
