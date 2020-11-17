import sqlite3 as sl
import praw
import pprint
import re
import datetime
import time
import sys

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

r = praw.Reddit('flairactionbot', user_agent='randombot')

gizz = r.subreddit('kgatlw').new(limit=50)
for post in gizz:
	if post.link_flair_text == 'Spotify':
		print(post)
		comment = post.reply("Hey, this appears to be a Spotify-related topic that's been discussed elsewhere on the sub (e.g. ELTS or Quarters being added, or that some dude uploaded Poly reversed). Feel free to search the topic as the original post is likely still around!\n\n*(this reply was generated by a bot)*")
		comment.mod.distinguish(how='yes', sticky=True)
		post.mod.remove()
	if post.link_flair_text == 'BuySell':
		print(post)
		comment = post.reply("Hey, there's a dedicated sticky thread for buying / selling / trading - feel free to check that thread out!\n\n*(this reply was generated by a bot)*")
		comment.mod.distinguish(how='yes', sticky=True)
		post.mod.remove()

duo = r.subreddit('duolingo').new(limit=50)
for post in duo:
	if post.link_flair_text == 'Memes':
		print(post)
		comment = post.reply("Heya, we tend to get quite a few template memes, and it can bury actual discussion of the app that this subreddit is for - you might want to check out /r/duolingomemes or a more general meme sub for these!\n\n*(this reply was generated by a bot)*")
		comment.mod.distinguish(how='yes', sticky=True)
		post.mod.remove()
	if post.link_flair_text == 'SDS':
		print(post)
		comment = post.reply("Heya, we tend to get quite a few screenshots of these phrases, especially before courses get into more useful vocabulary - leading to things like 'I am an apple' or 'The bear drinks beer'. You might want to check out /r/shitduolingosays, which is an entire sub for this content!\n\n*(this reply was generated by a bot)*")
		comment.mod.distinguish(how='yes', sticky=True)
		post.mod.remove()
	if post.link_flair_text == 'Progress' and not checkIfWritten(post.id):
		print(post)
		comment = post.reply("This post is flaired as 'Progress'. Congrats!\n\nWe get hundreds of progress screenshots, so if this is a screenshot we'd please ask that you either A.) leave a couple paragraphs in this post describing this milestone, _or_ B.) post screenshots in the Weekly Progress Thread instead.\n\n*(I'm a bot - if this isn't a screenshot at all, feel free to disregard this message!)*")
		comment.mod.distinguish(how='yes', sticky=True)
		markAsWritten(post.id)
	if post.link_flair_text == 'Progress-NoComment':
		print(post)
		post.mod.remove()
	if post.link_flair_text == 'Followers':
		print(post)
		comment = post.reply("Heya, we sometimes get a lot of posts for followers, clubs, classes, and other gatherings - feel free to check out the stickied thread for finding friends and followers!\n\n*(this reply was generated by a bot)*")
		comment.mod.distinguish(how='yes', sticky=True)
		post.mod.remove()
	if post.link_flair_text == 'How-to' and not checkIfWritten(post.id):
		print(post)
		comment = post.reply("Heya, a lot of people with this question find this article useful: https://making.duolingo.com/whats-the-best-way-to-learn-with-duolingo\n\n*(this reply was generated by a bot)*")
		comment.mod.distinguish(how='yes', sticky=True)
		markAsWritten(post.id)
	if post.link_flair_text == 'Flair' and not checkIfWritten(post.id):
		print(post)
		comment = post.reply("If you're looking to update your subreddit flair, you'll need to be on the desktop site (or use an app that supports flair). You can edit the text of your flair and include flag emojis that we've added to the subreddit.\n\nTo edit flair on old.reddit.com, click 'edit' in the sidebar below 'Show my flair on this subreddit.' To edit flair on new.reddit.com, click 'Community Options' in the sidebar, then click the pencil icon near 'User Flair Preview'.\n\nThe subreddit emojis are the two-letter [ISO 639-1](http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) abbreviations. For example, the `:fr:` emoji is the French flag. Duolingo supports some constructed languages that do not have an ISO 639-1 code - in these cases, we use whatever Duolingo uses in their URLs for that language.\n\n*(this reply was generated by a bot)*")
		comment.mod.distinguish(how='yes', sticky=True)
		markAsWritten(post.id)
	if post.link_flair_text == 'Hearts-Root' and not checkIfWritten(post.id):
		print(post)
		comment = post.reply("Hi, this was flagged as a post about the heart system - we get quite a high volume of these so other threads may be redirected here! Some people use [Duolingo classrooms](https://www.reddit.com/r/duolingo/comments/gs36bc/if_you_have_the_hearts_system_and_do_not_like_it/) to avoid the heart system entirely.\n\n*(this reply was generated by a bot)*")
		comment.mod.distinguish(how='yes', sticky=True)
		markAsHub(post.id, 'Duolingo', 'Hearts')
		markAsWritten(post.id)
	if post.link_flair_text == 'Hearts':
		print(post)
		hubId = getHubId('Duolingo', 'Hearts')
		comment = post.reply("Hi, this was flagged as a post about the heart system - we get quite a high volume of these, so please consider joining a [recent Hearts thread like this one!](http://reddit.com/r/duolingo/comments/{}/_/)\n\n*(this reply was generated by a bot)*".format(hubId))
		comment.mod.distinguish(how='yes', sticky=True)
		post.mod.remove()
		
modular = r.subreddit('modular').new(limit=50)
for post in modular:
	if post.link_flair_text == 'BuySell':
		print(post)
		comment = post.reply("Hey, there's a dedicated sticky thread for buying / selling / trading - feel free to check that thread out!\n\n*(this reply was generated by a bot)*")
		comment.mod.distinguish(how='yes', sticky=True)
		post.mod.remove()
	if post.link_flair_text == 'Feedback' and not checkIfWritten(post.id):
		print(post)
		comment = post.reply("This post is flaired as 'Feedback' - if you're looking for advice on a rack, some frequent tips are:\n\n* Start small - your needs may change as you learn more about what you want to get out of your instrument\n* If you're not sure at all where to start, consider one of the preconfigured systems by a vendor like Make Noise or Pittsburgh Foundation - they've been designing modular instruments for quite some time\n* We've had some good feedback discussions on the sub previously - if you haven't already, see if someone has already tried to make a rack similar to yours, and what advice they got\n* If you make some changes to your setup, consider a follow-up to let us know how it worked out!\n\nFor smaller gear questions, you might also want to check out the weekly gear thread that's stickied throughout the week.\n\n*(this reply was generated by a bot)*")
		comment.mod.distinguish(how='yes', sticky=True)
		markAsWritten(post.id)
	if post.link_flair_text == 'Beginner' and not checkIfWritten(post.id):
		print(post)
		comment = post.reply("This post is flaired as 'Beginner' - just a reminder to check out the sidebar if you haven't already! In particular there's a [beginner's guide](https://docs.google.com/document/d/1N46vujaaUOv2yyZq66Tuw5PNQmiBcRPypyQyHzghqos) with a lot of great info that users have put together.\n\n*(this reply was generated by a bot)*")
		comment.mod.distinguish(how='yes', sticky=True)
		markAsWritten(post.id)

testing = r.subreddit('andomprecision1').new(limit=50)
for post in testing:
	if post.link_flair_text == 'Heart-Root' and not checkIfWritten(post.id):
		print(post)
		comment = post.reply("heart root message\n\n*(this reply was generated by a bot)*")
		comment.mod.distinguish(how='yes', sticky=True)
		markAsHub(post.id, 'andomprecision1', 'hearts')
		markAsWritten(post.id)
	if post.link_flair_text == 'Heart-Branch':
		print(post)
		hubId = getHubId('andomprecision1', 'hearts')
		comment = post.reply("[link](http://reddit.com/r/andomprecision1/comments/{}/_/) \n\n*(this reply was generated by a bot)*".format(hubId))
		comment.mod.distinguish(how='yes', sticky=True)
		post.mod.remove()