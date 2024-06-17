# -*- coding: utf-8 -*-

import json
import math
import pandas as pd
import requests
import sys

"""File Information
@file_name: _sandbox.py
@author: Dylan "dyl-m" Monfret
To test things / backup functions.
"""


def get_results_shift(event_slug: str, nb_teams, team_alias: list = None, export_path: str = None) -> pd.DataFrame:
    """Retrieve League Play results from Shift API (Octane ZSR)
    :param event_slug: event ID (part of event URL on SHIFT)
    :param nb_teams: number of teams in League Play
    :param team_alias: optional teams' alias, list of list with original name in the first one and replacement in the
    second
    :param export_path: path for  data export as CSV file
    :return lpm_df: League Play results Pandas dataframe.
    """
    m_fix = nb_teams // 2  # Coefficient to compute round & match number

    try:
        matches = requests.get(f'https://zsr.octane.gg/matches?event={event_slug}').json()['matches']

        lpm_basics = [{'round': math.ceil(match['number'] / m_fix),
                       'match': math.ceil(match['number'] % m_fix) if math.ceil(
                           match['number'] % m_fix) != 0 else m_fix,
                       'team_1': match['blue']['team']['team']['name'].upper(),
                       'team_2': match['orange']['team']['team']['name'].upper(),
                       'score_1': match['blue'].get('score', 0),
                       'score_2': match['orange'].get('score', 0)}
                      for match in matches if match['stage']['name'] == 'League Play']

        lpm_df = pd.DataFrame(lpm_basics).sort_values(['round', 'match', 'team_1', 'team_2']).reset_index(drop=True)

        if team_alias:
            lpm_df.replace(team_alias[0], team_alias[1], inplace=True)

        if export_path:
            lpm_df.to_csv(export_path, index=False, encoding='utf-8')

        return lpm_df

    except json.decoder.JSONDecodeError:
        print('json.decoder.JSONDecodeError')
        sys.exit()


if __name__ == '__main__':
    EVENT_ID = 'c1be-rising-league-2024-spring-split'
    NB_TEAMS = 8
    ALIAS = [['JUNGLE JUICERS'], ['MAD CAP']]
    EXPORT_PATH = '../data/rising_league_2024/results.csv'

    RESULTS = get_results_shift(event_slug=EVENT_ID, nb_teams=NB_TEAMS, team_alias=ALIAS, export_path=EXPORT_PATH)
    print(RESULTS)
