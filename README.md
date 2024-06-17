# League Play Scenarios for Esport.

[![Twitter Follow](https://img.shields.io/twitter/follow/dyl_m_tweets?label=%40dyl_m_tweets&style=social)](https://twitter.com/dyl_m_tweets)
[![Reddit User Karma](https://img.shields.io/reddit/user-karma/link/dyl_m?label=u%2Fdyl_m&style=social)](https://www.reddit.com/user/Dyl_M)

Introduction
-------------

Open source project to generate ranking / qualification scenarios for esport teams during League Play stage. This project is a work in progress.

For this task, two calculating method will be explored:
* Conditional probabilities with Monte Carlo algorithm for results estimation leading to ranking scenarios
* Brut-force method for "exact ranking probabilities", or more accurately proportion of scenarios leading to each rank for each team in a League Play stage.

Study Cases
-------------

1. Rocket League: [Rising League 2024](https://liquipedia.net/rocketleague/Rocket_Baguette/Rising_League/2024/Split_1/Main_Event)
2. Rocket League: [Shift Summer League - Europe](https://liquipedia.net/rocketleague/Shift/Shift_Summer_League/Europe)
3. Rocket League: [Shift Summer League - North America](https://liquipedia.net/rocketleague/Shift/Shift_Summer_League/North_America)
4. League of Legends: LEC / LCS / LCK / LPL


Repository structure
-------------

Elements followed by `(IGNORED)` are kept ignored / hidden by git for privacy purpose or due to their size.

```
├── data
│   └── rising_league_2024
│       └── results.csv
│
├── src
│   ├── _sandbox.py
│   └── main.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

External information
-------------

Codes are reviewed by the [DeepSource](https://deepsource.io/) bot.