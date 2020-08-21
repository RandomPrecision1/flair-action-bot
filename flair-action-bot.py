import praw
import pprint
import re
import time
import sys

def markAsWritten(postName):
	f = open("posts.log", "a")
	f.write(postName + "\n")
	f.close()
	
def checkIfWritten(postName):
	f = open("posts.log", "r")
	contents = f.readlines()
	return postName + "\n" in contents
	
modularSearch = "https://cdn.modulargrid.net/img/racks/modulargrid_"
modularRegex = 'https:\/\/cdn\.modulargrid\.net\/img\/racks\/modulargrid_([0-9]+)\.jpg'

r = praw.Reddit('flairactionbot', user_agent='randombot')

gizz = r.subreddit('kgatlw').new(limit=50)
for post in gizz:
	if post.link_flair_text == 'Spotify':
		print(post)
		comment = post.reply("Hey, this appears to be a Spotify-related topic that's been discussed elsewhere on the sub (e.g. ELTS or Quarters being added, Mind Fuzz skipping being fixed). Feel free to search the topic as the original post is likely still around!\n\n*(this reply was generated by a bot)*")
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
		comment = post.reply("This post is flaired as 'Progress'. Congrats!\n\nWe get hundreds of progress screenshots, so if this is a screenshot we'd please ask that you either leave a comment here describing your experience and what you learned along the way, _or_ instead post the screenshot as a comment in the Weekly Progress Thread. Progress screenshots without comments will eventually be hidden to other users, to make sure that other kinds of posts are seen.\n\nIf this isn't a screenshot at all, feel free to disregard this message!\n\n*(this reply was generated by a bot)*")
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
		comment = post.reply("If you're looking to update your subreddit flair, you'll need to be on the desktop site (or use an app that supports flair). You can edit the text of your flair and include flag emojis that we've added to the subreddit.\n\nTo edit flair on old.reddit.com, click 'edit' in the sidebar below 'Show my flair on this subreddit.' To edit flair on new.reddit.com, click 'Community Options' in the sidebar, then click the pencil icon near 'User Flair Preview'\n\nThe subreddit emojis are the two-letter [ISO 639-1](http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) abbreviations. For example, the `:fr:` emoji is the French flag. Duolingo supports some constructed languages that do not have an ISO 639-1 code - in these cases, we use whatever Duolingo uses in their URLs for that language.\n\n*(this reply was generated by a bot)*")
		comment.mod.distinguish(how='yes', sticky=True)
		markAsWritten(post.id)
		
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
	if re.search(modularSearch, post.selftext, re.IGNORECASE) and not checkIfWritten(post.id):
		print(post)
		botcomment = "Hi! You posted a link to your ModularGrid rack image. The link to the actual rack is more helpful in providing advice as it allows users to see a module's function without having seen it before.\n\nHere's the link to the actual rack: https://www.modulargrid.net/e/racks/view/"
		botcommentpart2 = "\n\n*(this reply was generated by a bot)*"
		mgid = re.search(modularRegex, post.selftext)
		comment = post.reply(botcomment + mgid.group(1) + botcommentpart2)
		comment.mod.distinguish(how='yes', sticky=True)
		markAsWritten(post.id)
		