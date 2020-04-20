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
    board.push(col4)
    board.push(col3)
    board.push(col2)
    board.push(col1)
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
    col4.push(c10)
    col3.push(c9)
    col3.push(c8)
    col2.push(c7)
    col2.push(c6)
    col2.push(c5)
    col2.push(c4)
    col1.push(c3)
    col1.push(c2)
    col1.push(c1)

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
        elif c == ord('L'):
            board.promote()
            board.paint()
        elif c == ord('H'):
            board.denote()
            board.paint()


curses.wrapper(main)
