from curses import curs_set, wrapper

from model import Board, Column, Card


def main(stdscr):
    curs_set(False)

    board = Board('default', stdscr)
    col1 = Column('Backlog')
    col2 = Column('Ready')
    col3 = Column('Done')
    board.add(col1)
    board.add(col2)
    board.add(col3)
    c1 = Card('Example card 1')
    c2 = Card('Example card 2')
    c3 = Card('Example card 3')
    c4 = Card('Example card 4')
    c5 = Card('Example card 5')
    c6 = Card('Example card 6')
    c7 = Card('Example card 7')
    c8 = Card('Example card 8')
    c9 = Card('Example card 9')
    c10 = Card('Example card 10')
    col1.add(c1)
    col1.add(c2)
    col1.add(c3)
    col1.add(c4)
    col1.add(c5)
    col1.add(c6)
    col1.add(c7)
    col2.add(c8)
    col2.add(c9)
    col3.add(c10)

    board.resize()
    board.paint()

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break
        elif c == ord('j'):
            if board.down():
                board.paint()
        elif c == ord('k'):
            if board.up():
                board.paint()
        elif c == ord('l'):
            if board.right():
                board.paint()
        elif c == ord('h'):
            if board.left():
                board.paint()


wrapper(main)
