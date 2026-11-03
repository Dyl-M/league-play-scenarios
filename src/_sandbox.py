# -*- coding: utf-8 -*-

# Built-in packages
import itertools as it
import json
import numpy as np
import pandas as pd

# Project-specific packages
import compute
import datasets

"""File Information
@file_name: _sandbox.py
@author: Dylan "dyl-m" Monfret
To test things / backup functions.
"""


def calculate_standings(df, remaining_matches, outcome):
    teams = df['team_1'].unique()
    standings = pd.DataFrame(index=teams, columns=['wins', 'losses', 'game_diff', 'games_won', 'games_lost'],
                             dtype='float64').fillna(0).astype(int)
    head_to_head = pd.DataFrame(0, index=teams, columns=teams)

    # Process existing results
    for _, row in df.iterrows():
        team_1, team_2, score_1, score_2 = row['team_1'], row['team_2'], int(row['score_1']), int(row['score_2'])
        standings.loc[team_1, 'games_won'] += score_1
        standings.loc[team_1, 'games_lost'] += score_2
        standings.loc[team_2, 'games_won'] += score_2
        standings.loc[team_2, 'games_lost'] += score_1
        standings.loc[team_1, 'wins'] += score_1 > score_2
        standings.loc[team_1, 'losses'] += score_1 <= score_2
        standings.loc[team_2, 'wins'] += score_2 > score_1
        standings.loc[team_2, 'losses'] += score_2 <= score_1
        head_to_head.loc[team_1, team_2] += score_1 > score_2
        head_to_head.loc[team_2, team_1] += score_2 > score_1

    # Simulated outcomes
    for i, (result_1, result_2) in enumerate(outcome):
        team_1, team_2 = remaining_matches[i]
        standings.loc[team_1, 'games_won'] += result_1
        standings.loc[team_1, 'games_lost'] += result_2
        standings.loc[team_2, 'games_won'] += result_2
        standings.loc[team_2, 'games_lost'] += result_1
        standings.loc[team_1, 'wins'] += result_1 > result_2
        standings.loc[team_1, 'losses'] += result_1 <= result_2
        standings.loc[team_2, 'wins'] += result_2 > result_1
        standings.loc[team_2, 'losses'] += result_2 <= result_1
        head_to_head.loc[team_1, team_2] += result_1 > result_2
        head_to_head.loc[team_2, team_1] += result_2 > result_1

    standings['game_diff'] = standings['games_won'] - standings['games_lost']

    return standings, head_to_head


def apply_tiebreakers(standings, head_to_head):
    sorted_teams = standings.sort_values(by=['wins', 'game_diff', 'games_won'], ascending=False)

    # Handle head-to-head tiebreakers
    tie_indices = sorted_teams['wins'].duplicated(keep=False)
    tied_teams = sorted_teams[tie_indices]

    if not tied_teams.empty:
        for team in tied_teams.index:
            tied_group = tied_teams[tied_teams['wins'] == tied_teams.loc[team, 'wins']]
            if len(tied_group) > 1:
                head_to_head_scores = head_to_head.loc[tied_group.index, tied_group.index]
                head_to_head_wins = head_to_head_scores.apply(np.sum, axis=1)
                sorted_teams.loc[tied_group.index] = tied_group.loc[
                    head_to_head_wins.sort_values(ascending=False).index]

    return sorted_teams


if __name__ == '__main__':
    # Read and store Aliases
    with open('../data/rising_league_2024/team_aliases.json', 'r', encoding='utf-8') as aliases_file:
        ALIASES = json.load(aliases_file)

    EVENT_ID = 'c1be-rising-league-2024-spring-split'
    EXPORT_PATH = '../data/rising_league_2024/results.csv'
    NB_TEAMS = 8
    ROUND_TH = 7

    RESULTS = datasets.get_results_shift(EVENT_ID, NB_TEAMS, aliases=ALIASES)
    RESULTS_RX, REMAINING = datasets.filter_rounds(RESULTS, ROUND_TH)

    # Generate all possible Best of 5 outcomes
    bo5_outcomes = compute.bo_outcomes(3)
    print(f'Number of scenarios to compute: {len(bo5_outcomes) ** len(REMAINING)}')

    # Generate all possible outcomes for the remaining matches
    all_possible_outcomes = list(it.product(bo5_outcomes, repeat=len(REMAINING)))

    # Example usage
    STANDINGS, H2H = calculate_standings(RESULTS_RX, REMAINING, all_possible_outcomes[-1])
    SORTED_STANDINGS = apply_tiebreakers(STANDINGS, H2H)
    print(SORTED_STANDINGS)
