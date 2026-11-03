# -*- coding: utf-8 -*-

import itertools as it

"""File Information
@file_name: compute.py
@author: Dylan "dyl-m" Monfret
To compute ranking probabilities
"""


def bo_outcomes(n_games: int) -> list:
    """Compute possible outcomes for a Series (Best of n-games)
    :param n_games: number of games to win the series
    :return: all the possible outcomes.
    """
    part1 = it.product([n_games], range(n_games))
    part2 = it.product(range(n_games - 1, -1, -1), [n_games])
    return list(it.chain(part1, part2))
