# SPDX-FileCopyrightText: 2018 Karel
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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
from urllib.parse import urlsplit

from intelmq.lib.bot import CollectorBot
from intelmq.lib.mixins import HttpMixin
from intelmq.lib.exceptions import MissingDependencyError

try:
    import twitter
except ImportError:
    twitter = None


class TwitterCollectorBot(CollectorBot, HttpMixin):
    "Collect tweets from given target timelines"
    access_token_key: str = ""
    access_token_secret: str = ""
    consumer_key: str = ""
    consumer_secret: str = ""
    default_scheme: str = "http"
    exclude_replies: bool = False
    follow_urls: str = ""
    include_rts: bool = True
    target_timelines: str = ""
    timelimit: int = 24 * 60 * 60
    tweet_count: int = 20
    _target_timelines = []
    _follow_urls = []

    def init(self):
        if twitter is None:
            raise MissingDependencyError("twitter")
        self.current_time_in_seconds = int(time.time())
        if self.target_timelines != '':
            self._target_timelines.extend(
                self.target_timelines.split(','))
        if self.follow_urls != '':
            self._follow_urls.extend(
                self.follow_urls.split(','))
        self.api = twitter.Api(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token_key=self.access_token_key,
            access_token_secret=self.access_token_secret,
            tweet_mode="extended")

    def get_text_from_url(self, url: str) -> str:
        # netloc could include the port explicityly, but we ignore that improbable case here
        netloc = urlsplit(url).netloc
        if netloc == "pastebin.com" or netloc.endswith('.pastebin.com'):
            self.logger.debug('Processing url %r.', url)
            if "raw" not in url:
                request = self.http_get(
                    url.replace("pastebin.com", "pastebin.com/raw", count=1))
            else:
                request = self.http_get(url)
            return request.text
        return ''

    def process(self):
        tweets = []
        for target in self._target_timelines:
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
                'https://twitter.com/{}/status/{}'.format(tweet.user.screen_name, tweet.id))
            self.send_message(report)
            if tweet.user.screen_name in self._follow_urls:
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
                            'https://twitter.com/{}/status/{}'.format(tweet.user.screen_name, tweet.id))
                        self.send_message(report)


BOT = TwitterCollectorBot
