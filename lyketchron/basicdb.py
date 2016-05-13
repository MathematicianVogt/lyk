from pymongo import MongoClient


client = MongoClient('localhost', 27017)



db = client['ryans_db']
collection = db['ryan']

post={"myname":"Ryan", "number":5}

posts = collection.posts

collection.insert_one(post)