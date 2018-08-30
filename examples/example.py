from pymine import Game

help = '''
*==================================================*
|                                                  |
|                     PyMine                       |
|                                                  |
*==================================================*

How to play:

- Write the coordinates of the cell you want to
  uncover, when asked for "Your move".
  Example:
  >>> Your move: 5,5

- If you want to flag a cell to mark it as bomb,
  use a third argument "f" (ex: 5,5,f).
  To unflag it, use "u".
'''


def main():
    print(help)

    # Start the game
    g = Game(9,9,10)
    starting_cell = input('Your move: ').split(',')
    row, col = int(starting_cell[0]), int(starting_cell[1])
    g.start(row, col)
    print(g)

    # Play
    while True:
        next_move = input('Your move: ').split(',')
        row, col = int(next_move[0]), int(next_move[1])
        action = ''
        if len(next_move) == 3:
            action = next_move[2]
        
        if action == 'f':
            g.mark_cell_as_bomb(row, col)
        elif action == 'u':
            g.unmark_cell(row, col)
        else:  # the default action is to uncover the cell
            g.uncover_cell(row, col)
            g.check()
        print(g)

        # if we win or lost g.is_over becomes True
        if g.is_over:
            print('* Game is over *')
            print(f'* Outcome: {g.outcome.name} *')
            break


if __name__ == '__main__':
    main()
