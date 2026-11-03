# -*- coding: utf-8 -*-

import json
import math
import pandas as pd
import requests
import sys

"""File Information
@file_name: datasets.py
@author: Dylan "dyl-m" Monfret
To retrieve and format input data.
"""


def filter_rounds(results_df: pd.DataFrame, round_th: int) -> (pd.DataFrame, list):
    """Filter results with a round threshold, return filtered results and the remaining rounds filtered out
    :param results_df: original results Pandas DataFrame
    :param round_th: round threshold
    :return filtered_results_df, remaining_rounds: filtered results Pandas DataFrame and remaining rounds filtered
    out as list of tuples.
    """
    filtered_results_df = results_df[results_df['round'] <= round_th]
    remaining_rounds_df = results_df[results_df['round'] > round_th].reset_index(drop=True)
    remaining_rounds = list(zip(remaining_rounds_df['team_1'], remaining_rounds_df['team_2']))
    return filtered_results_df, remaining_rounds


def get_results_shift(event_slug: str, nb_teams: int, aliases: dict = None, export_path: str = None) -> pd.DataFrame:
    """Retrieve League Play results from Shift API (Octane ZSR)
    :param event_slug: event ID (part of event URL on SHIFT)
    :param nb_teams: number of teams in League Play
    :param aliases: optional teams' aliases, dictionary with former name as key and new name as value
    :param export_path: path for  data export as CSV file
    :return lpm_df: League Play results Pandas dataframe.
    """
    m_fix = nb_teams // 2  # Coefficient to compute round & match number

    try:
        matches = requests.get(f'https://zsr.octane.gg/matches?event={event_slug}').json()['matches']

        lpm_basics = [{'round': math.ceil(match['number'] / m_fix),
                       'match': math.ceil(match['number'] % m_fix)
                       if math.ceil(match['number'] % m_fix) != 0 else m_fix,
                       'team_1': match['blue']['team']['team']['name'].upper(),
                       'team_2': match['orange']['team']['team']['name'].upper(),
                       'score_1': match['blue'].get('score', 0),
                       'score_2': match['orange'].get('score', 0)}
                      for match in matches if match['stage']['name'] == 'League Play']

        lpm_df = pd.DataFrame(lpm_basics).sort_values(['round', 'match', 'team_1', 'team_2']).reset_index(drop=True)

        if aliases:
            l_aliases = [aliases.keys(), aliases.values()]
            lpm_df.replace(l_aliases[0], l_aliases[1], inplace=True)

        if export_path:
            lpm_df.to_csv(export_path, index=False, encoding='utf-8')

        return lpm_df

    except json.decoder.JSONDecodeError:
        print('json.decoder.JSONDecodeError')
        sys.exit()
