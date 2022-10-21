from espn_api.basketball import League
from datetime import datetime as dt
from datetime import timedelta

league = League(league_id=1408591336, year=2023, espn_s2='AEA0XcSLoiCaw4CPshthcqt5KQO5ah2fxZpHNTVyKhrlkwMNGXFQHaox5mBT8czEcyrny3v9oW%2BYdI%2BcfGygrJjMYazKpph1mx2YpoK36Sx%2BzytFdIGgazFGmneYlAogzx980yT4%2BLpimP73ip3ixwHdZBNVCe2O6H3sb4kMbYP6CIR4yJQ8anWI%2FTUgWr92dH3zfe9qD1Q%2Fc6E9m1zy%2FdNYQZisCJfalYfsLAioB%2BhibLro%2F7Z8yG2SFMAodxmWJsQWOQAoyHm5BG6EPKbE0BIo1xO2Ldf5ka%2BrrJxWdjPSoHxQa5oD9Fw0n2PXiQv4pSs%3D', swid='{682DD6BF-1EC1-4B39-ADD6-BF1EC11B39B0}')

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
    
highest_team_string = str(get_highest_team(box).team_name).strip() + ": " + str(int(get_highest_team_score(box))) + " points"


highest_scorer = get_highest_player_week(box).name
highest_scorer_team = get_player_team(get_highest_player_week(box).playerId).team_abbrev

day_name = dt.today().strftime("%A")


highest_player_string = str(highest_scorer) + " (" + str(highest_scorer_team) + "): " + str(int(get_highest_player_week(box).points)) + " points"


# WEEKLY SCORES
# return all scores for the week
# def get_scores(box):
#     scores = []
#     for game in box:
#         scores.append(str(game.home_team.team_abbrev) + ": " + str(game.home_score) + " points")
#         scores.append(str(game.away_team.team_abbrev) + ": " + str(game.away_score) + " points")

#     return scores

matchups = []
def get_matchups_with_score(box):
    
    for game in box:
        # add new line for each game
        matchups.append(str(game.home_team.team_abbrev) + " vs " + str(game.away_team.team_abbrev) + ": " + str(int(game.home_score)) + "-" + str(int(game.away_score)))
    for i in range(len(matchups)):
        # print(matchups[i])
        scores_string = str(matchups[i])

    return matchups, scores_string


get_matchups_with_score(box)

def list_to_string(matchups):
    # initialize an empty string
    str1 = ""
    # return string
    return ('\n'.join(matchups))

scores_string = list_to_string(matchups)

# calculate team with most wins




# concatenate into tweet string
tweet_string = "Weekly Leaders:\n\n" + highest_team_string + "\n" +  highest_player_string

tweet_string_score = "Scores:\n\n" + scores_string

# print(tweet_string_score)

# for player in box[0].home_lineup:
#     print(player.name  + '\t' + str(int(player.points)))
