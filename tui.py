from curses import curs_set, wrapper

from model import Workflow, Column, Card


def main(stdscr):
    curs_set(False)

    wf = Workflow('default', stdscr, 0, 0)
    col1 = Column('Backlog', 25)
    col2 = Column('Ready', 25)
    wf.add(col1)
    wf.add(col2)
    c1 = Card('Example card 1')
    c2 = Card('Example card 2')
    c3 = Card('Example card 3')
    c4 = Card('Example card 4')
    c5 = Card('Example card 5')
    c6 = Card('Example card 6')
    c7 = Card('Example card 7')
    c8 = Card('Example card 8')
    c9 = Card('Example card 9')
    col1.add(c1)
    col1.add(c2)
    col1.add(c3)
    col1.add(c4)
    col1.add(c5)
    col1.add(c6)
    col1.add(c7)
    col2.add(c8)
    col2.add(c9)
    wf.selected = True

    wf.paint()

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break
        elif c == ord('j'):
            if wf.down():
                wf.paint()
        elif c == ord('k'):
            if wf.up():
                wf.paint()
        elif c == ord('l'):
            if wf.right():
                wf.paint()
        elif c == ord('h'):
            if wf.left():
                wf.paint()


wrapper(main)
