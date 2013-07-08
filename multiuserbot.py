#!/usr/bin/python2.7

import twitter
import argparse

CONSUMER_KEY     = ''
CONSUMER_SECRET  = ''


class Bot(object):
    """Twitter Multiuserbot

    This bot can be used to send tweets from another account using direct
    messages. If you want to tweet from several accounts or many users need to
    use only one account, run this bot and send a direct message to the twitter
    account to publish the tweet from this account. Permissions are
    administered by following/unfollowing or by defining a blacklist or
    whitelist.

    Usage:
    Account A follows B, C, D. Start this script and authorize using account A.
    Direct messages from B, C and D to A will be twittered by A. Define a
    whitelist or a blacklist to exclude or include only a subgroup of the user
    B, C, D, who are allowed to twitter through acocunt A.
    """

    def __init__(self, token, token_secret, whitelist=None, blacklist=None,
                 userstream_url='userstream.twitter.com', **kwargs):
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.auth      = twitter.OAuth(
            consumer_key    = CONSUMER_KEY,
            consumer_secret = CONSUMER_SECRET,
            token           = token,
            token_secret    = token_secret
        )
        self.api       = twitter.Twitter(auth=self.auth)
        self.ustream   = twitter.TwitterStream(auth=self.auth, domain=userstream_url)

    def __call__(self):
        print "Listening for new direct messages..."
        # TODO is there a clean way to close all sockets?
        for msg in self.ustream.user():
            if 'direct_message' in msg:
                dm     = msg['direct_message']
                sender = dm['sender']['screen_name']
                text   = dm['text']
                if self._tweet_message(sender, text):
                    print "TWITTERING: @%s\n%s\n" % (sender, text)
                    self.api.statuses.update(status=text)

    def _tweet_message(self, sender, text):
        if self.blacklist is not None and sender in self.blacklist:
            return False
        elif self.whitelist is not None and sender in self.whitelist:
            self._check_already_tweeted(text)
        return True

    def _check_already_tweeted(self, text):
        for status in self.api.statuses.user_timeline():
            if text == status['text']:
                error_msg = "Text already tweeted. Exiting because probably " \
                            "there is another bot active. Message: '%s'" % text
                raise RuntimeError(error_msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=Bot.__doc__.replace('\n\n', ' # # #'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--whitelist', nargs='+', metavar='USER',
                       help='allows twittering *only* for these users (bot '
                            'account must follow these users)')
    parser.add_argument('--blacklist', nargs='+', metavar='USER',
                       help='forbid twittering for these users (not '
                        'combinable with option --whitelist)')
    parser.add_argument('--token',
                       help='token for oauth (if not given will ask for oauth)')
    parser.add_argument('--token-secret',
                       help='token secret for oauth (if not given will ask for oauth)')

    # TODO:
    #parser.add_argument('--reconnect-tries', metavar='N', type=int, default=10,
    #                   help='number of tries if connection fails, set to 0 to'
    #                    'disable')
    #parser.add_argument('--reconnect-delay', metavar='SEC', type=int, default=60,
    #                   help='number of tries if connection fails, set to 0')
    #parser.add_argument('--starts-with', metavar='STRING', default='',
    #                   help='tweet only messages starting with STRING, e.g. '
    #                   "tw"')
    # TODO add timeout option <-- not so easy, need to patch twitter module?

    args = parser.parse_args()

    if args.token is None or args.token_secret is None:
        auth = twitter.oauth_dance('twitter-multiuserbot',
                                   CONSUMER_KEY,
                                   CONSUMER_SECRET)
        args.token, args.token_secret = auth
        print "Token: %s, Token secret: %s" % auth

    bot = Bot(**vars(args))
    bot()
