import sqlite3 as sl
import praw
import pprint
import re
import datetime
import time
import sys
import pytesseract
import requests
import os
from termcolor import colored

os.system('color')

# file access
def downloadImage(url, id):
	with open('ocr.jpg', 'wb') as handle:
		response = requests.get(url,stream=True)
		
		for block in response.iter_content(1024):
			if not block:
				break
			handle.write(block)

r = praw.Reddit('flairactionbot', user_agent='randombot')

gizz = r.subreddit('kgatlw').new(limit=30)
for post in gizz:
	matches = ['top song', 'top artist', 'spotify', 'total streams', 'share this story', 'you were in', 'favorite song of theirs']
	if (post.domain == 'i.redd.it' or post.domain == 'i.imgur.com') and post.link_flair_text != 'EOYRoot':
		print(colored(post.id + ' - direct image detected', 'blue'))
		url = post.url
		downloadImage(url, post.id)
		text = pytesseract.image_to_string('ocr.jpg').lower()
		print(colored(text, 'green'))
		if any(x in text for x in matches):
			print(colored(post.id + ' matched', 'red'))
			post.mod.flair(text='EOY')
	if hasattr(post, 'is_gallery') and post.is_gallery == True and post.link_flair_text != 'EOYRoot':
		print(colored(post.id + ' - reddit gallery detected', 'blue'))
		firstId = post.gallery_data['items'][0]['media_id']
		url = post.media_metadata[firstId]['p'][3]['u']
		downloadImage(url, post.id)
		text = pytesseract.image_to_string('ocr.jpg').lower()
		print(colored(text, 'green'))
		if any(x in text for x in matches):
			print(colored(post.id + ' matched', 'red'))
			post.mod.flair(text='EOY')
	if (post.domain == 'imgur.com' and 'imgur.com' in post.url and '/a/' not in post.url):
		print(colored(post.id + ' - imgur indirect image detected', 'blue'))
		pattern = 'https://imgur.com/(.*)'
		search = re.search(pattern, post.url)
		result = search.group(1)
		url = 'https://i.imgur.com/' + result + '.jpg'
		downloadImage(url, post.id)
		text = pytesseract.image_to_string('ocr.jpg').lower()
		print(colored(text, 'green'))
		if any(x in text for x in matches):
			print(colored(post.id + ' matched', 'red'))
			post.mod.flair(text='EOY')
	
duolingo = r.subreddit('duolingo').new(limit=30)
for post in duolingo:
	matches = ['year in review', 'i got better', 'other languages', 'minutes spent', 'words studied', 'for the year', 'top of duolingo']
	if (post.domain == 'i.redd.it' or post.domain == 'i.imgur.com'):
		print(colored(post.id + ' - direct image detected', 'blue'))
		url = post.url
		downloadImage(url, post.id)
		text = pytesseract.image_to_string('ocr.jpg').lower()
		print(colored(text, 'green'))
		if any(x in text for x in matches):
			print(colored(post.id + ' matched', 'red'))
			post.mod.flair(text='YiR')
	if hasattr(post, 'is_gallery') and post.is_gallery == True:
		print(colored(post.id + ' - reddit gallery detected', 'blue'))
		firstId = post.gallery_data['items'][0]['media_id']
		url = post.media_metadata[firstId]['p'][3]['u']
		downloadImage(url, post.id)
		text = pytesseract.image_to_string('ocr.jpg').lower()
		print(colored(text, 'green'))
		if any(x in text for x in matches):
			print(colored(post.id + ' matched', 'red'))
			post.mod.flair(text='YiR')
	if (post.domain == 'imgur.com' and 'imgur.com' in post.url and '/a/' not in post.url):
		print(colored(post.id + ' - imgur indirect image detected', 'blue'))
		pattern = 'https://imgur.com/(.*)'
		search = re.search(pattern, post.url)
		result = search.group(1)
		url = 'https://i.imgur.com/' + result + '.jpg'
		downloadImage(url, post.id)
		text = pytesseract.image_to_string('ocr.jpg').lower()
		print(colored(text, 'green'))
		if any(x in text for x in matches):
			print(colored(post.id + ' matched', 'red'))
			post.mod.flair(text='YiR')