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













