# AI: Sudoku Solver
## Introductory Project: Diagonal Sudoku Solver

This projected delivered as part of Udacity AI course to solve any sudoku puzzle

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: we used constraint propagation to find solution by eliminate the digits found in twin identical boxes as following:
<br/>1- loop on all units
<br/>2- identify identical twin in the unit (2 boxes with same two digits)
<br/>3- remove each digit in twin boxes from the unit peers.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: (while the sudoku not solved and there is digits to eliminate)<br/>
we eliminate the possible solutions from boxes then apply only choice and naked twins on
the units including two main diagonal units.


### Install

This project requires **Python 3**.

install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Team
The solution implemented by Ahmad Barqawi based on Udacity project and accepted by Udacity submission team
