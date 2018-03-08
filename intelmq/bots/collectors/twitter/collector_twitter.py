"""
Twitter Collector Bot

Extracts tweet_text from tweets and follows urls in supported_sources.
Url text and tweet text are sent separately.

Parameters:

    feed - feed name (Twitter)

    tweet_count : int default 20

    target_timelines : comma separated screen_names of users whose timelines are followed

    follow_urls : comma separated screen_names of tweeters for which it is
            allowed to follow urls, currently extraction only from pastebin is supported


    include_rts : bool default False (include retweets)

    exclude_replies: bool default True

    timelimit: int default 84400s, how far to the past do we accept tweets?

    Api login data:
        consumer_key
        consumer_secret
        access_token_key
        access_token_secret

To get api login data see: https://python-twitter.readthedocs.io/en/latest/getting_started.html

"""

import time
from intelmq.lib.bot import CollectorBot

try:
    import requests
except ImportError:
    requests = None

try:
    import twitter
except ImportError:
    twitter = None


class TwitterCollectorBot(CollectorBot):

    def init(self):
        if requests is None:
            raise ValueError("Could not import 'requests'. Please install it.")
        if twitter is None:
            raise ValueError("Could not import 'twitter'. Please install it.")
        self.current_time_in_seconds = int(time.time())
        self.target_timelines = []
        if getattr(self.parameters, "target_timelines", '') is not '':
            self.target_timelines.extend(
                self.parameters.target_timelines.split(','))
        self.tweet_count = int(getattr(self.parameters, "tweet_count", 20))
        self.follow_urls = []
        if getattr(self.parameters, "follow_urls", '') is not '':
            self.follow_urls.extend(
                self.parameters.follow_urls.split(','))
        self.include_rts = getattr(self.parameters, "include_rts", False)
        self.exclude_replies = getattr(self.parameters, "exclude_replies", False)
        self.timelimit = int(getattr(self.parameters, "timelimit", 24 * 60 * 60))
        self.api = twitter.Api(
            consumer_key=self.parameters.consumer_key,
            consumer_secret=self.parameters.consumer_secret,
            access_token_key=self.parameters.access_token_key,
            access_token_secret=self.parameters.access_token_secret,
            tweet_mode="extended")

    def get_text_from_url(self, url: str) -> str:
        if "pastebin.com" in url:
            self.logger.debug('Processing url %r.', url)
            if "raw" not in url:
                request = requests.get(
                    url.replace("pastebin.com", "pastebin.com/raw"))
            else:
                request = requests.get(url)
            return request.text
        return ''

    def process(self):
        tweets = []
        for target in self.target_timelines:
            statuses = self.api.GetUserTimeline(
                screen_name=target,
                count=self.tweet_count,
                include_rts=self.include_rts,
                exclude_replies=self.exclude_replies)
            tweets.extend(statuses)
        tweets_new = []
        for tweet in tweets:  # filter out new tweets
            if tweet.created_at_in_seconds > (self.current_time_in_seconds - self.timelimit):
                tweets_new.append(tweet)
        for tweet in tweets_new:
            self.logger.debug('Processing Tweet ID %r.', tweet.id)
            report = self.new_report()
            report.add('raw', tweet.full_text)
            report.add(
                'feed.url',
                'https://twitter.com/{0}/status/{1}'.format(tweet.user.screen_name, tweet.id))
            self.send_message(report)
            if tweet.user.screen_name in self.follow_urls:
                if len(tweet.urls) > 0:
                    text = ''
                    for source in tweet.urls:
                        text = text + self.get_text_from_url(source.expanded_url)
                    if len(text) > 0:
                        report = self.new_report()
                        report.add('raw', text)
                        report.add('feed.code', 'url_text')
                        report.add(
                            'feed.url',
                            'https://twitter.com/{0}/status/{1}'.format(tweet.user.screen_name, tweet.id))
                        self.send_message(report)


BOT = TwitterCollectorBot
