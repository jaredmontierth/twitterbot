from espn_api.basketball import League
from datetime import datetime as dt
from datetime import timedelta

league = League(league_id=1408591336, year=2023,
                espn_s2='AEA0XcSLoiCaw4CPshthcqt5KQO5ah2fxZpHNTVyKhrlkwMNGXFQHaox5mBT8czEcyrny3v9oW%2BYdI%2BcfGygrJjMYazKpph1mx2YpoK36Sx%2BzytFdIGgazFGmneYlAogzx980yT4%2BLpimP73ip3ixwHdZBNVCe2O6H3sb4kMbYP6CIR4yJQ8anWI%2FTUgWr92dH3zfe9qD1Q%2Fc6E9m1zy%2FdNYQZisCJfalYfsLAioB%2BhibLro%2F7Z8yG2SFMAodxmWJsQWOQAoyHm5BG6EPKbE0BIo1xO2Ldf5ka%2BrrJxWdjPSoHxQa5oD9Fw0n2PXiQv4pSs%3D',
                swid='{682DD6BF-1EC1-4B39-ADD6-BF1EC11B39B0}')

box = league.box_scores()


# WEEKLY LEADERS
# calculate the highest scoring player of the week

def get_highest_player_week(box):
    highest_score = 0
    highest_scorer = ''
    for game in box:
        for player in game.home_lineup:
            if player.points > highest_score:
                highest_score = player.points
                highest_scorer = player
        for player in game.away_lineup:
            if player.points > highest_score:
                highest_score = player.points
                highest_scorer = player
    return highest_scorer


# get that player's team

def get_player_team(player_id):
    for team in league.teams:
        for player in team.roster:
            if player.playerId == player_id:
                return team


# get the highest scoring team of the week

def get_highest_team(box):
    highest_score = 0
    highest_team = ''
    for game in box:
        if game.home_score > highest_score:
            highest_score = game.home_score
            highest_team = game.home_team
        if game.away_score > highest_score:
            highest_score = game.away_score
            highest_team = game.away_team
    return highest_team


# get that team's score

def get_highest_team_score(box):
    highest_score = 0
    highest_team = ''
    for game in box:
        if game.home_score > highest_score:
            highest_score = game.home_score
            highest_team = game.home_team
        if game.away_score > highest_score:
            highest_score = game.away_score
            highest_team = game.away_team
    return highest_score


