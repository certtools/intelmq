import twitter
import requests
from url_normalize import url_normalize
from tld import get_tld
from tld.utils import update_tld_names
from intelmq.lib.bot import CollectorBot


class TwitterCollectorBot(CollectorBot):
    def init(self):
        update_tld_names()
        self.id_map = {}
        self.target_timelines = self.parameters.target_timelines.split(",")
        self.users = self.parameters.users.split(",")
        self.api = twitter.Api(consumer_key=self.parameters.consumer_key,
                               consumer_secret=self.parameters.consumer_secret,
                               access_token_key=self.parameters.access_token_key,
                               access_token_secret=self.parameters.access_token_secret, tweet_mode="extended")

    def max_id_finder(self, tweets: list, name: str):
      # Finds max twee_id in tweets from specific user, so next time the bot gets tweets with ids from this maximum
        for tweet in tweets:
            if tweet.id > self.id_map[name]:
                self.id_map[name] = tweet.id

    def get_data_from_url(self, url: str) -> list:
        data = []
        supported_sources = ["pastebin.com"]
        for source in supported_sources:
            if source in url:
                if "raw" not in url:
                    request = requests.get(url.replace("pastebin.com", "pastebin.com/raw"))
                else:
                    request = requests.get(url)
                for source in request.content.decode().split("\r\n"):
                    if "." or "/" in source:
                        data.append(source)
        return data

    def get_data_from_text(self, tweet: list) -> list:
        data = []
        for part in tweet:
            if "t.co" not in part:
                result = get_tld(part, fail_silently=True, as_object=True)
                if result is not None:
                        data.append(url_normalize(part))
        return data

    def analyze_tweet(self, tweet) -> list:
        data = []
        tweet_text = []
        tweet_text.extend(tweet.full_text.split(" "))
        if tweet.quoted_status is not None:
            tweet_text.extend(tweet.quoted_status.full_text.split(" "))
        if len(tweet.urls) > 0:
            for source in [tweet.urls, tweet.quoted_status.urls]:
                for url in source:
                    data.extend(self.get_data_from_url(url.expanded_url))
        data.extend(self.get_data_from_text(tweet_text))
        return data

    def process(self):
        tweets = []
        for target in self.target_timelines:
            try:
                statuses = self.api.GetUserTimeline(screen_name=target, count=self.parameters.tweet_count,
                                                    since_id=self.id_map[target])
            except KeyError:
                self.id_map[target] = 0
                statuses = self.api.GetUserTimeline(screen_name=target, count=self.parameters.tweet_count)
            except Exception as e:
                self.logger.info("Getting tweets failed {}".format(e))
            self.max_id_finder(statuses, target)
            tweets.extend(statuses)

        for user in self.users:
            try:
                statuses = self.api.GetFavorites(screen_name=user, count=self.parameters.tweet_count,
                                                 since_id=self.id_map[user])
            except KeyError:
                self.id_map[user] = 0
                statuses = self.api.GetFavorites(screen_name=user, count=self.parameters.tweet_count)
            except Exception as e:
                self.logger.info("Getting tweets failed {}".format(e))
            self.max_id_finder(statuses, user)
            tweets.extend(statuses)

        data = []
        for tweet in tweets:
            data.extend(self.analyze_tweet(tweet))
        data = "\n".join(data)

        report = self.new_report()
        report.add("raw", data)
        report.add("feed.url", "<data source>")
        self.send_message(report)


BOT=TwitterCollectorBot
