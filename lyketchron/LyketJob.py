import feedparser
import time
import thread
import json
from MongoLib import *
from multiprocessing.dummy import Pool as ThreadPool 
import datetime
from NewsArticle import NewsArticle
import cProfile
import signal
from tld import get_tld
import uuid

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

signal.signal(signal.SIGALRM, timeout_handler)



class LyketJob:
	def __init__(self):
		self.file=open('lyketstreams.txt')
		self.db=MongoLib("lyket", "articles")
		self.reddit = praw.Reddit(user_agent='Going around Reddit giving summeries to different genre articles /u/ArticleBot')
		self.reddit.set_oauth_app_info(client_id='Qyrv_Uc2Hl7JMQ',client_secret='R1U7xFO0KZY81hrvS5pzpwUGGlY',redirect_uri='http://www.example.com/unused/redirect/uri')
		self.reddit.login("ArticleBot","dongs420")
		self.sublist=["news","worldnews","politics"]

	#thread function, will put enteries into DB in paraell. Will build json, then put into DB
	def put_article_in_db(self,story_url):
		try:
			for x in self.sublist:
				submissions=self.reddit.get_subreddit(x).get_hot(limit=100)
				for submission in submissions:
					story_url=submission.url.encode('ascii', 'ignore')

					if( not self.db.in_set({'url':story_url})):
						current_article = NewsArticle(story_url)
						

						
						#publish date for article : datetime object 
						article_published = current_article.date_made()
						
						

						#title of article : String
						article_title=current_article.get_title()
						#print article_title


					
						current_article.goodArticle()
						#keywords in article: Array of Strings
						article_key_words = current_article.getKeywords()
						
						#videos in story : Array of Strings (url to videos)
						article_videos = current_article.get_videos()


						#summary of article : String
						article_summary = current_article.getSummary()
						
						#authors of article: Array of Strings
						article_authors = current_article.getAuthors()
						
						#image for article : String (url to image)
						article_thumbnaillink = current_article.thumbnail_url()

						article_url = current_article.get_url()

						res=get_tld(article_url, as_object=True)
						new_entry = {}
						new_entry['title']=article_title
						new_entry['sum']=article_summary
						new_entry['auth']=article_authors
						new_entry['thumb'] = article_thumbnaillink
						new_entry['pub'] = article_published
						new_entry['keywords'] = article_key_words
						new_entry['vids']  = article_videos
						new_entry['likes']=0
						new_entry['dislikes']=0
						new_entry['comments'] = []
						new_entry['url'] = article_url
						new_entry['_id'] = uuid.uuid4().hex

						new_entry['creationtime']=datetime.datetime.now()
						new_entry['publisher'] = res.domain

						new_entry['creationtime']=datetime.datetime.utcnow()
						new_entry['companycreator'] = res.domain

						self.db.CollectionSubmitOne(new_entry)

				except Exception as e:
					print "------"
					print "its fucked emma"
					print e
					print "------"

	def runJob(self):
		try:
			for stream in self.file:

				currentstream = feedparser.parse(stream)
				for entry in currentstream['entries']:
					story_url = entry['link']
					signal.alarm(10)  
					try:
						self.put_article_in_db(story_url)
					except TimeoutException:
						continue
					else:
						signal.alarm(0)
					
		except Exception as e:
			print "The following issue occured: "
			print e
			print " "

					
			


x=LyketJob()
x.runJob()
#cProfile.run('x.runJob()')
			
