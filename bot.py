from datetime import datetime
import tweepy
from keysproton import *
from espn import *
import numpy as np
import time


def api():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    return tweepy.API(auth)


def tweet(api: tweepy.API, message: str):
    api.update_status(message)
    print("Tweeted: " + message)


if __name__ == "__main__":
    api = api()
    # tweet(api, tweet_string)

bot_id = int(api.get_user(screen_name='cprotontweets').id_str)
mention_id = 1

words = ["stats", "fantasy"]

words_score = ["score", "scores", "matchup"]

words_top = ["top", "top5", "top 5", "topfive", "top five"]


while True:

    # pull in the data from api
    league = League(league_id=1408591336, year=2023,
                espn_s2='AEA0XcSLoiCaw4CPshthcqt5KQO5ah2fxZpHNTVyKhrlkwMNGXFQHaox5mBT8czEcyrny3v9oW%2BYdI%2BcfGygrJjMYazKpph1mx2YpoK36Sx%2BzytFdIGgazFGmneYlAogzx980yT4%2BLpimP73ip3ixwHdZBNVCe2O6H3sb4kMbYP6CIR4yJQ8anWI%2FTUgWr92dH3zfe9qD1Q%2Fc6E9m1zy%2FdNYQZisCJfalYfsLAioB%2BhibLro%2F7Z8yG2SFMAodxmWJsQWOQAoyHm5BG6EPKbE0BIo1xO2Ldf5ka%2BrrJxWdjPSoHxQa5oD9Fw0n2PXiQv4pSs%3D',
                swid='{682DD6BF-1EC1-4B39-ADD6-BF1EC11B39B0}')

    box = league.box_scores()

    # reconstruct tweet strings

    highest_team_string = str(get_highest_team(box).team_name).strip() + ": " + str(
    int(get_highest_team_score(box))) + " points"

    highest_scorer = get_highest_player_week(box).name
    highest_scorer_team = get_player_team(get_highest_player_week(box).playerId).team_abbrev


    highest_player_string = str(highest_scorer) + " (" + str(highest_scorer_team) + "): " + str(
        int(get_highest_player_week(box).points)) + " points"

    matchups = []

    def get_matchups_with_score(box):
        for game in box:
            # add new line for each game
            matchups.append(str(game.home_team.team_abbrev) + " vs " + str(game.away_team.team_abbrev) + ": " + str(
                int(game.home_score)) + "-" + str(int(game.away_score)))
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

    # calculate the top five highest scoring players of the week

    def get_top_five(box):
        top_five = []
        for game in box:
            for player in game.home_lineup:
                top_five.append(player)
            for player in game.away_lineup:
                top_five.append(player)
        top_five.sort(key=lambda x: x.points, reverse=True)
        return top_five[:5]

    # get the team of the top five highest scoring players of the week

    def get_top_five_team_abbrev(player_name):
        for team in league.teams:
            for player in team.roster:
                if player.name == player_name:
                    return team.team_abbrev


    top_five = get_top_five(box)


    top_five_string = ""
    for player in top_five:
        top_five_string += str(player.name) + " (" + str(get_top_five_team_abbrev(player.name)) + "): " + str(
            int(player.points)) + " points\n"


    # concatenate into tweet string

    tweet_string_top_five = "Top 5 scorers this week:\n\n" + top_five_string

    tweet_string = "Weekly Leaders:\n\n" + highest_team_string + "\n" + highest_player_string

    tweet_string_score = "Scores:\n\n" + scores_string    

    # listen for mentions

    mentions = api.mentions_timeline(since_id=mention_id)
    for mention in mentions:

        if time.time() - mention.created_at.timestamp() >= 15:
            continue

        print("found mentioned tweet")
        print(f"{mention.author.screen_name}: {mention.text}")
        mention_id = mention.id

        if mention.in_reply_to_status_id is None and mention.author.id != bot_id:
            if True in [word in mention.text.lower() for word in words]:
                try:
                    print("attempting to reply")
                    api.update_status("@" + str(mention.author.screen_name) + " " + tweet_string,
                                      in_reply_to_status_id=mention.id)
                    print("replied")
                except Exception as exc:
                    print(exc)

            if True in [word in mention.text.lower() for word in words_score]:
                try:
                    print("attempting to reply")
                    api.update_status("@" + str(mention.author.screen_name) + " " + tweet_string_score,
                                      in_reply_to_status_id=mention.id)
                    print("replied")
                except Exception as exc:
                    print(exc)

            if True in [word in mention.text.lower() for word in words_top]:
                try:
                    print("attempting to reply")
                    api.update_status("@" + str(mention.author.screen_name) + " " + tweet_string_top_five,
                                      in_reply_to_status_id=mention.id)
                    print("replied")
                except Exception as exc:
                    print(exc)


    time.sleep(15)

