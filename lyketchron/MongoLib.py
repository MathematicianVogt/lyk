import pymongo
from pymongo import MongoClient
class MongoLib:
	 
	#create db and collection object via mongo. Default host, but can be changed. 
	 def __init__(self,dbName,collectionName, host='localhost', port=27017):
	 	self.client = MongoClient(host,port)
		self.db = self.client[dbName]
	 	self.collection = self.db[collectionName]
	 
	 
	 #return db object for personal use
	 def GetDB(self):
	 	return self.db
	 
	 
	 #return collections object for personal use
	 def GetCol(self):
	 	return self.collection
	 
	 
	 #submit one piece of data to collection of this instance
	 def CollectionSubmitOne(self, post):
	 	
	 	self.collection.insert(post)
	 
	 #submit multiple pieces of data to collection of this instance
	 def CollectionSubmitMany(self,postList):
	 	
	 	posts = self.collection.posts
	 	posts.insert_many(postList)
	 #prints the entire collection of this instance
	 def PrintCollection(self):
	 	
	 	allContent=self.getCol().find()
	 	for entry in allContent:
	 		print entry
	 #returns all enteries in the instance of this collection
	 def ReturnAllEnteries():
	 	return self.GetCol().find()
	 #rerturns all instances of the collection that meet the rules specified as a dictionary
	 def CollectionFind(self,rules):
	 	return self.GetCol().find(rules)
	 def getLastN(self, N):
	 	return self.collection.find().skip(db.collection.count() - N)

	 def findOne(self,rules):
	 	return self.collection.findOne(rules)
	 def size(self):
	 	return self.collection.count()
	 def in_set(self,dic):
	 	return bool(self.collection.find_one(dic))





