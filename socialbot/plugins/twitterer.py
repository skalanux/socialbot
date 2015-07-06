#!/usr/bin/python
# -*- coding: utf-8 -*-
#from pyshorteners.shorteners  import Shortener
from twitter import *

from socialbot.utils import get_config

TWITTER_CONSUMER_KEY = 'uS6hO2sV6tDKIOeVjhnFnQ'
TWITTER_CONSUMER_SECRET = 'MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk'


class Twitterer(object):
    ACTION_NAME = 'Twitted'

    def do(self, text, link):
        config = get_config()
        oauth_token = config.get('twitter', 'token')
        oauth_secret = config.get('twitter', 'secret')
        body = link + " " + text

        twitter = Twitter(
            auth=OAuth(
                oauth_token, oauth_secret,
                TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET),
            api_version='1.1',
            domain='api.twitter.com')

        twitter.statuses.update(status=body)
