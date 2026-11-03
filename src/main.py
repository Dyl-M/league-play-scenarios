# -*- coding: utf-8 -*-

# Built-in packages
import json

# Project-specific packages
import datasets

"""File Information
@file_name: _sandbox.py
@author: Dylan "dyl-m" Monfret
To execute each step of probabilities computing at once.
"""

if __name__ == '__main__':
    with open('../data/rising_league_2024/team_aliases.json', 'r', encoding='utf-8') as aliases_file:
        ALIASES = json.load(aliases_file)

    EVENT_ID = 'c1be-rising-league-2024-spring-split'
    EXPORT_PATH = '../data/rising_league_2024/results.csv'
    NB_TEAMS = 8

    RESULTS = datasets.get_results_shift(EVENT_ID, NB_TEAMS, aliases=ALIASES)
    RESULTS_R5, REMAINING = datasets.filter_rounds(RESULTS, 5)
