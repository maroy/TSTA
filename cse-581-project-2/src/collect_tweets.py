import os
import logging
import tweepy
import consumer
import access_token

from config import Config
from tweetrepo import TweetRepository


class StdOutListener(tweepy.StreamListener):

    def __init__(self, tweet_repo):
        super(StdOutListener, self).__init__()
        self.tweet_repo = tweet_repo

    def on_data(self, data):
        self.tweet_repo.add(data)

        if os.path.isfile("stop"):
            self.tweet_repo.close()
            return False

        return True

    def on_error(self, status):
        logging.error("tweepy error: " + status)


class App:

    def __init__(self, config):
        self.config = config

    def collect_tweets(self, repo):
        auth = tweepy.OAuthHandler(consumer.key, consumer.secret)
        auth.set_access_token(access_token.key, access_token.secret)

        stream = tweepy.Stream(auth, StdOutListener(repo))

        stream.filter(
            languages=self.config.languages(),
            track=self.config.key_words()
        )


def run():

    logging.basicConfig(filename='collect_tweets.log', level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())

    os.remove("stop")
    cfg = Config()

    while True:
        try:
            repo = TweetRepository(cfg)
            app = App(cfg)
            app.collect_tweets(repo)
            logging.info("done")
            break
        except Exception as ex:
            logging.error("Exception: " + ex.message)
            logging.error("Restarting")


if __name__ == "__main__":
    run()