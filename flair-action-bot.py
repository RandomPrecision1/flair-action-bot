import sqlite3 as sl
import praw
import pprint
import re
import datetime
import time
import sys

# db access
def markAsWritten(postName):
	con = sl.connect('flair.db')
	cursor = con.cursor()
	insert = """insert into TaggedPosts(Id, Date) values(?, ?)"""
	data = (postName, datetime.datetime.now())
	cursor.execute(insert, data)
	con.commit()
	cursor.close()
	con.close()

def checkIfWritten(postName):
	con = sl.connect('flair.db')
	data = con.execute('select Id from TaggedPosts')
	result = postName in list(map(lambda x: x[0], data))
	con.close()
	return result
	
def markAsHub(postName, subreddit, type):
	con = sl.connect('flair.db')
	cursor = con.cursor()
	insert = """insert into Hubs(Id, Date, Subreddit, Type) values(?, ?, ?, ?)"""
	data = (postName, datetime.datetime.now(), subreddit, type)
	cursor.execute(insert, data)
	con.commit()
	cursor.close()
	con.close()
	
def getHubId(subreddit, type):
	con = sl.connect('flair.db')
	cursor = con.cursor()
	query = 'select Id from Hubs where Subreddit = ? and Type = ? order by Date desc limit 1'
	data = (subreddit, type)
	result = cursor.execute(query, data)
	for row in result:
		hub = row[0]
	cursor.close()
	con.close()
	return hub

# strings
botDisclaimer = '\n\n*(this reply was generated by a bot)*'
def hubUrl(subreddit, id):
	return "\n\n[Here's a link to a recent thread I found!](https://reddit.com/r/" + subreddit + "/comments/" + id  + "/_/)"

# commands
def removeWithReason(post, reason):
	print(post)
	comment = post.reply(reason + botDisclaimer)
	comment.mod.distinguish(how='yes', sticky=True)
	post.mod.remove()
	
def removeWithoutReason(post):
	print(post)
	post.mod.remove()
	
def addMessage(post, message):
	if not checkIfWritten(post.id):
		print(post)
		comment = post.reply(message + botDisclaimer)
		comment.mod.distinguish(how='yes', sticky=True)
		markAsWritten(post.id)

def addAsHubWithMessage(post, message, subreddit, type):
	if not checkIfWritten(post.id):
		print(post)
		comment = post.reply(message + botDisclaimer)
		comment.mod.distinguish(how='yes', sticky=True)
		markAsHub(post.id, subreddit, type)
		markAsWritten(post.id)

def addAsHubWithoutMessage(post, subreddit, type):
	if not checkIfWritten(post.id):
		print(post)
		markAsHub(post.id, subreddit, type)
		markAsWritten(post.id)
		
def removeForHub(post, message, subreddit, type):
	print(post)
	hubId = getHubId(subreddit, type)
	comment = post.reply(message + hubUrl(subreddit, hubId) + botDisclaimer)
	comment.mod.distinguish(how='yes', sticky=True)
	post.mod.remove()

r = praw.Reddit('flairactionbot', user_agent='randombot')

gizz = r.subreddit('kgatlw').new(limit=50)
for post in gizz:
	if post.link_flair_text == 'Spotify':
		removeWithReason(post, "Hey, this appears to be a Spotify-related topic that's been discussed elsewhere on the sub (e.g. reversed Polygondwanaland or album visualizations). Feel free to search the topic as the original post is likely still around!")
	if post.link_flair_text == 'BuySellRoot':
		addAsHubWithMessage(post, "**Reminder to be wary of users that haven't been active on the subreddit, or accounts that are clearly farming for karma!**\n\nWe occasionally have scammers who are either banned from /r/KGATLW and thus cannot comment here, or brand-new accounts created by those users.", 'KGATLW', 'BuySell')
	if post.link_flair_text == 'BuySell':
		removeForHub(post, "Hey, there's usually a dedicated sticky thread for buying / selling / trading - I'll try to link it below:", 'KGATLW', 'BuySell')
	if post.link_flair_text == 'MegaRoot':
		addAsHubWithoutMessage(post, 'KGATLW', 'Mega')
	if post.link_flair_text == 'Mega':
		removeForHub(post, "Hey, this topic seems to have an active megathread to consolidate the discussion a bit - I'll try to link it below:", 'KGATLW', 'Mega')
	if post.link_flair_text == 'EOYRoot':
		addAsHubWithoutMessage(post, 'KGATLW', 'EOY')
	if post.link_flair_text == 'EOY':
		removeForHub(post, "Hey, there have been some recent threads about these end-of-year summaries - to consolidate these posts I'll try to link one below:", 'KGATLW', 'EOY')

duo = r.subreddit('duolingo').new(limit=50)
for post in duo:
	if post.link_flair_text == 'Memes':
		removeWithReason(post, "Heya, we tend to get quite a few template memes, and it can bury actual discussion of the app that this subreddit is for - you might want to check out /r/duolingomemes or a more general meme sub for these!")
	if post.link_flair_text == 'SDS':
		removeWithReason(post, "Heya, we tend to get quite a few screenshots of these phrases, especially before courses get into more useful vocabulary - leading to things like 'I am an apple' or 'The bear drinks beer'. You might want to check out /r/shitduolingosays, which is an entire sub for this content!")
	if post.link_flair_text == 'Progress':
		addMessage(post, "This post is flaired as 'Progress'. Congrats!\n\nWe get hundreds of progress screenshots, so if this is a screenshot we'd please ask that you either A.) leave a couple paragraphs in this post describing this milestone, _or_ B.) post screenshots in the Weekly Progress Thread instead.")
	if post.link_flair_text == 'Progress-NoComment':
		removeWithoutReason(post)
	if post.link_flair_text == 'Followers':
		removeWithReason(post, "Heya, we sometimes get a lot of posts for followers, clubs, classes, and other gatherings - feel free to check out the stickied thread for finding friends and followers!")
	if post.link_flair_text == 'How-to':
		addMessage(post, "Heya, a lot of people with this question find this article useful: https://making.duolingo.com/whats-the-best-way-to-learn-with-duolingo")
	if post.link_flair_text == 'Flair':
		addMessage(post, "If you're looking to update your subreddit flair, you'll need to be on the desktop site (or use an app that supports flair). You can edit the text of your flair and include flag emojis that we've added to the subreddit.\n\nTo edit flair on old.reddit.com, click 'edit' in the sidebar below 'Show my flair on this subreddit.' To edit flair on new.reddit.com, click 'Community Options' in the sidebar, then click the pencil icon near 'User Flair Preview'.\n\nThe subreddit emojis are the two-letter [ISO 639-1](http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) abbreviations. For example, the `:fr:` emoji is the French flag. Duolingo supports some constructed languages that do not have an ISO 639-1 code - in these cases, we use whatever Duolingo uses in their URLs for that language.")
	if post.link_flair_text == 'Hearts-Root':
		addAsHubWithMessage(post, "Hi, this was flagged as a post about the heart system - we get quite a high volume of these so other threads may be redirected here!\n\nDuolingo has a [FAQ about Hearts](https://support.duolingo.com/hc/en-us/articles/115002887326-What-are-Hearts-), as well as one [on how to restore them](https://support.duolingo.com/hc/en-us/articles/360048809311).", 'Duolingo', 'Hearts')
	if post.link_flair_text == 'Hearts':
		removeForHub(post, "Hi, this was flagged as a post about the heart system - we get quite a high volume of these, so please consider joining an already-existing thread!", 'Duolingo', 'Hearts')
	if post.link_flair_text == 'YiRRoot':
		addAsHubWithoutMessage(post, 'Duolingo', 'YiR')
	if post.link_flair_text == 'YiR':
		removeForHub(post, "Hi, this was detected as a Year-in-Review post - since many of these are being posted, there's a dedicated megathread here:", 'Duolingo', 'YiR')
		
modular = r.subreddit('modular').new(limit=50)
for post in modular:
	if post.link_flair_text == 'BuySell':
		removeWithReason(post, "Hey, there's a dedicated sticky thread for buying / selling / trading - feel free to check that thread out!")
	if post.link_flair_text == 'Feedback':
		addMessage(post, "This post is flaired as 'Feedback' - if you're looking for advice on a rack, some frequent tips are:\n\n* Start small - your needs may change as you learn more about what you want to get out of your instrument\n* If you're not sure at all where to start, consider one of the preconfigured systems by a vendor like Make Noise or Pittsburgh Foundation - they've been designing modular instruments for quite some time\n* We've had some good feedback discussions on the sub previously - if you haven't already, see if someone has already tried to make a rack similar to yours, and what advice they got\n* If you make some changes to your setup, consider a follow-up to let us know how it worked out!\n\nFor smaller gear questions, you might also want to check out the weekly gear thread that's stickied throughout the week.")
	if post.link_flair_text == 'Beginner':
		addMessage(post, "This post is flaired as 'Beginner' - just a reminder to check out the sidebar if you haven't already! In particular there's a [beginner's guide](https://docs.google.com/document/d/1N46vujaaUOv2yyZq66Tuw5PNQmiBcRPypyQyHzghqos) with a lot of great info that users have put together.")
