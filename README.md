# Towers of Hanoi

![Version](https://img.shields.io/badge/version-2.1.4-3776AB)
![Status: Archived](https://img.shields.io/badge/status-archived-lightgrey)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/game%20library-Pygame-00A86B)](https://www.pygame.org/)

A small interactive Towers of Hanoi game I made with Python and Pygame.

This was one of my early programming projects, created while I was learning the basics of programming at school. It was later featured at my school's vocational fair.

## Features

* Choose between 1 and 13 disks.
* Move disks between three towers using the mouse.
* Prevents illegal moves.
* Keeps track of the current move count.
* Shows the theoretical minimum number of moves.
* Reset the game at any time.
* Displays a message when the puzzle is completed.

The `old/` directory contains earlier versions of the project kept for reference.

## Requirements

* Python 3.10 or newer
* `pygame`
* `colorama`

Install the dependencies with:

```bash
python -m pip install pygame colorama
```

## Running the game

Clone the repository:

```bash
git clone https://github.com/josmrpy/towers-of-hanoi.git
cd towers-of-hanoi
```

Then run:

```bash
python towers_of_hanoi.py
```

Choose a number from `1` to `13` when prompted.

## How to play

Click a tower to pick up its top disk, then click another tower to place it.

The game follows the classic Towers of Hanoi rules: a larger disk cannot be placed on top of a smaller one.

The theoretical minimum number of moves is calculated with:

```text
2^n - 1
```

where `n` is the number of disks.

## Project files

```text
.
├── towers_of_hanoi.py    # Current version
└── old/                # Previous versions (removed)
    ├── __towers of hanoi.py
    ├── 2towers of hanoi.py
    └── towers of hanoi.py
```

## About this project

This project was an early experiment with Python, graphical interfaces, user input, and implementing a classic algorithm as an interactive game.

More of my projects can be found on my portfolio:

<https://josmrpy.github.io/>

## License

This repository is primarily intended to showcase my work and development process. It does not currently include a separate open-source license.
