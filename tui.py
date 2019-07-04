import curses

from model import Board, Column, Card


def main(stdscr):
    curses.curs_set(False)
    stdscr.clear()

    board = Board('default', stdscr)
    col1 = Column('Backlog')
    col2 = Column('Ready')
    col3 = Column('In Progress')
    col4 = Column('Done')
    board.add(col1)
    board.add(col2)
    board.add(col3)
    board.add(col4)
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
    col2.add(c4)
    col2.add(c5)
    col2.add(c6)
    col2.add(c7)
    col3.add(c8)
    col3.add(c9)
    col4.add(c10)

    board.resize()
    board.paint()

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break
        elif c == curses.KEY_RESIZE:
            board.resize()
            board.paint()
        elif c == ord('j'):
            board.down()
            board.paint()
        elif c == ord('k'):
            board.up()
            board.paint()
        elif c == ord('l'):
            board.right()
            board.paint()
        elif c == ord('h'):
            board.left()
            board.paint()


curses.wrapper(main)
