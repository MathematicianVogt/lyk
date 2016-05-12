# -*- coding: utf-8 -*-
from mongolib import *
from google import search
from newspaper import *
from time import gmtime, strftime
import unicodedata
import requests
import math
import random
import praw
import time
import pymongo
import pytumblr
import random as ran
import datetime

class newsArticle:
	def __init__(self,url):
		self.article=Article(url)
		self.article.download()
		self.article.parse()
		self.article.nlp()
	
	def getKeywords(self):
		x=self.article.keywords
		for i in range(0,len(x)):
			x[i]=x[i].encode('ascii', 'ignore')
		return x

		return self.article.keywords
	def getSummary(self):
		return self.article.summary.encode('ascii', 'ignore')
	def getAuthors(self):
		x=self.article.authors
		for i in range(0,len(x)):
			x[i]=x[i].encode('ascii', 'ignore')
		return x
	def getTitle(self):
		return self.article.title


class TwitterNewsBot:
	def __init__(self):
		self.reddit = praw.Reddit(user_agent='Going around Reddit giving summeries to different genre articles /u/ArticleBot')
		self.reddit.set_oauth_app_info(client_id='Qyrv_Uc2Hl7JMQ',client_secret='R1U7xFO0KZY81hrvS5pzpwUGGlY',redirect_uri='http://www.example.com/unused/redirect/uri')
		self.reddit.login("ArticleBot","dongs420")
		self.sublist=["news","worldnews","UpliftingNews"]
		self.client = pytumblr.TumblrRestClient(
		  '4B3SNHX8i9gcQ8NXUjhmJjzF4wVX8XUINRGpCVPejKgLUZR83O',
		  'VAFvL1jDkLBNpbLnf0IJCAZISMVDlnoWhWUIMdfnVowkmMtBtR',
		  '50nFPJ8wQTYDQKug5XDlinrHaEkNLzlAMNvvE0v95mn3fvg1YK',
		  'GFp1E97wn7sn3SqDXJiAo39F39s6wy9rGo8wNdZwBlMQevp75n'
		)
		self.db=MongoLib("database",'news')
	
	def upcase_first_letter(self,s):
	    return s[0].upper() + s[1:]	
	def buildOutput(self,urlLink):
		x=newsArticle(urlLink)
		a=x.getKeywords()
		b=x.getSummary()
		c=x.getAuthors()
		d=x.getTitle()
		keywords=""
		#print "1"
		return [urlLink,a,b,d]
	def startBot(self):
		counter=0
		my=0
		notdone=True	
		while notdone:
			try:
				x=ran.choice(self.sublist)
				submissions = self.reddit.get_subreddit(x).get_hot(limit=100)
				for submission in submissions:
					try:
						 #print "2"
						 art=submission.url.encode('ascii', 'ignore')
						 dic={'url':art}
						 #print 'got here'
						 #print dic
						 if self.db.in_set(dic):
						 	print 'we found it boys ' + str(my)
							my=my+1
							continue
						 else:
							 y=self.buildOutput(art)
							 for i in y[1]:
							 	i.encode('ascii', 'ignore')
							 y[2]=y[2] + "\n\n\n I am a bot written by a <a href=\"http://eigenvaluee.tumblr.com/\">Mathematician</a> \n\nPosted at " + str(time.ctime())
							 print str(self.client.create_link('newsstoriesnow.tumblr.com',title=y[3].encode('ascii', 'ignore'),url=y[0].encode('ascii', 'ignore'),description=y[2].encode('ascii', 'ignore'),tags=y[1],format='html'))
							 self.db.CollectionSubmitOne(dic)
							 counter+=1
							 print "Done with " + str(counter)
							 notdone=False
							 break
					except Exception as e:
						print e
						continue
			except Exception as e:
				print e



x=TwitterNewsBot()
x.startBot()
		




