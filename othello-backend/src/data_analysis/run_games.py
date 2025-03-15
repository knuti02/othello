"""
Python script to run n amount of games where the models use slightly different heuristics
The purpose of this script is to evaluate the performance of the models

Will save into a star schema database where the fact table contains the game results
and the dimension tables contain the gamestates, moves and the models used
"""

import random