# Maze-and-caves

## Maze genetration and solving

This is an implementation of program that can generate and render perfect mazes and caves:
- The program is developed in Python language
- The program is built with Makefile which contains standard set of targets for GNU-programs: all, install, uninstall, clean, dvi, dist, tests. Installation directory could be arbitrary, except the building one
- GUI implementation, based on any GUI library for Python
- The program has a button to load the maze from a file, which is in examples folder
- Maximum size of the maze is
  50x50
- The program can generate a perfect maze according to **Eller's algorithm**
- The user enters only the dimensionality of the maze: the number of rows and columns
- The generated maze can be saved in the file
- The program can solve the maze currently shown on the screen
- The user sets the starting and ending points
- The route, which is the solution, is displayed with a line 2 pixel thick, passing through the middle of all the cells in the maze through which the solution runs.
- The color of the solution line must be different from the color of the walls, and the field
- The full coverage of the maze solving module with unit-tests prepared

## Cave Generation

- The user selects the file that describes the cave which is in examples folder
- Maximum size of the cave is 50 x 50
- The user sets the limits for "birth" and "death" of a cell, as well as the chance for the starting initialization of the cell
- The "birth" and "death" limits can have values from 0 to 7
- Cells outside the cave are considered alive
- There is a step-by-step mode for rendering the results of the algorithm in two variants:
    - Pressing the next step button will lead to rendering the next iteration of the algorithm
    - Pressing the automatic work button starts rendering iterations of the algorithm with a frequency of 1 step in `N` milliseconds, where the number of milliseconds `N` is set through a special field in the user interface
- The full coverage of the cave generation module with unit-tests prepared
