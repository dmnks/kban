from curses import curs_set, wrapper

from model import Workflow, Column, Card


def main(stdscr):
    curs_set(False)
    # Clear screen
    stdscr.clear()

    wf = Workflow('default')
    col1 = Column('Backlog', 25)
    col2 = Column('Ready', 25)
    wf.columns.append(col1)
    wf.columns.append(col2)
    c1 = Card('Example card 1')
    c2 = Card('Example card 2')
    c3 = Card('Example card 3')
    c4 = Card('Example card 4')
    c5 = Card('Example card 5')
    col1.add(c1)
    col1.add(c2)
    col1.add(c3)
    col2.add(c4)
    col2.add(c5)

    wf.paint(stdscr, 0, 0)

    stdscr.refresh()
    stdscr.getkey()


wrapper(main)
