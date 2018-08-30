# pymine-engine

## Installation

```shell
$ pip install https://github.com/ndrbrt/pymine-engine/archive/master.zip
```

## Usage

A backend engine to implement the Minesweeper game in Python(3). It computes the logic behind the game and exposes an API that you can use to build your frontend.

Here is a simple example of the usage:

```python
>>> from pymine import Game

>>> g = Game(9,9,10)
>>> g.start(5,5)
>>> print(g)
```

The code above initialize a Game object `g`, with a board that has 9 rows, 9 columns (then 81 cells) and 10 bombs.

After that, it starts the game on cell with coordinates (5,5) that is row 5, column 5. The `start` method compiles the board to have a "zero cell" in the given coordinates, then uncovers that cell and its neighbors (more details on this below).

The third statement prints the game, that is it prints the board with the actual uncovered or flagged cells. Note: this utility is mostly useful when using the package interactively in a shell, mainly for debug purposes. (If you actually want to display the board, showing all the cells' values either they are covered or uncovered, you can do so with `print(g.board)`)

Once the game is started, you have three possible actions you can accompish: uncover a cell, mark it as a bomb cell, or mark it as doubt.

The following two methods mark a cell as "bomb" or as "doubt" respectively

```python
>>> g.mark_cell_as_bomb(7,6)
>>> g.mark_cell_as_doubt(8,6)
```

If you now print the game (`print(g)`), you would see an "f" (for "flagged") on cell (7,6) and a "?" on cell (8,6). (Remember the coordinates of a cell are in the form or (row, column), as in a matrix)

To uncover a cell, just use

```python
>>> g.uncover_cell(7,7)
```

Now, marking a cell, actually, is just helpful for whom is playing the game, but has nothing to do with logic of the game itself.
On the contrary, the action for uncover a cell is a key action that can determine if we win or lost. Every time we uncover a cell we could end up winning the game (if we correctly uncovered all the cells that are not bombs) or loosing it (if we uncover a cell that is actually a bomb).

Because of this, every time you uncover a cell, you should check the game. Do so with

```python
>>> g.check()
```

The `check()` method, returns None if the game is neither win nor lost, or an Outcome object otherwise.

## API

## Example

This is a very minimal and trivial example that implements an actual playable game of Minesweeper using this api.

```python
# example.py

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

```

You can play it with:

```shell
$ python3 example.py
```
