# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  

**Naked Twins Problem:** There exists a pair of numbers that are the same in a row, column or unit. For example, F3 and I3 both have a 2 and a 3 as a possible solution. Based on Sudoku rules, a row, column or unit cannot have the same number repeated.
![Naked Twins Image](/images/naked-twins.png)

**Solution:** Find pairs that match the criteria above and attempt to solve the puzzle as much as possible. To solve the puzzle:
1) Search the unit for the same number(s) and remove them since these numbers cannot exist in the any other box based on sudoku rules.
![Naked Twins Remove Image](/images/naked-twins-2.png)

2) Repeat until all naked twins are removed from the puzzle and the puzzle cannot solved further.
3) Use other strategies to solve the puzzle if naked twins technique cannot solve completely.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  

**Diagonal Sudoku Problem:** In addition to standard constraits/rules, a diagonal sudoku puzzle requires that the diagonals does have the number repeated.
![Diagonal Sudoku Image](/images/diagonal-sudoku.png)

**Solution:**
1) Add left and right diagonals to the list of constraits.
2) Search the puzzle to find the correct number that belongs in each box using the list of contstraits.
3) Repeat the search until the puzzle is solved.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
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

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

