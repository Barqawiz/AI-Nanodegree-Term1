
# Implement a Planning Search

## Run project
Example terminal command to run project:
```
python run_search.py -p 1 -s 1
```
Available options: <br/>

Problems <br/>
1. Air Cargo Problem 1
2. Air Cargo Problem 2
3. Air Cargo Problem 3

Search Algorithms <br/>
1. breadth_first_search
2. breadth_first_tree_search
3. depth_first_graph_search
4. depth_limited_search
5. uniform_cost_search
6. recursive_best_first_search h_1
7. greedy_best_first_graph_search h_1
8. astar_search h_1
9. astar_search h_ignore_preconditions
10. astar_search h_pg_levelsum


## Synopsis

This project includes skeletons for the classes and functions needed to solve deterministic logistics planning problems for an Air Cargo transport system using a planning search agent.

![Progression air cargo search](images/Progression.PNG)


## Environment requirements
- Python 3.4 or higher
- Starter code includes a copy of [companion code](https://github.com/aimacode) from the Stuart Russel/Norvig AIMA text.  

## Contribution
My part in the project was to implement following functions:
- `AirCargoProblem.get_actions` method including `load_actions` and `unload_actions` sub-functions
- `AirCargoProblem.actions` method
- `AirCargoProblem.result` method
- `air_cargo_p2` function
- `air_cargo_p3` function

And write problem analysis in the document:<br>
(code_analysis.pdf)

## Improving Execution Time

The exercises in this project can take a *long* time to run (from several seconds to a several hours) depending on the heuristics and search algorithms you choose, as well as the efficiency of your own code.  (You may want to stop and profile your code if runtimes stretch past a few minutes.) One option to improve execution time is to try installing and using [pypy3](http://pypy.org/download.html) -- a python JIT, which can accelerate execution time substantially.  Using pypy is *not* required (and thus not officially supported) -- an efficient solution to this project runs in very reasonable time on modest hardware -- but working with pypy may allow students to explore more sophisticated problems than the examples included in the project.
