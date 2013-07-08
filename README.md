twitter-multiuserbot
====================

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



Requirements:
- python2.7
- https://github.com/sixohsix/twitter
- a consumer key/secret pair from https://dev.twitter.com/apps


