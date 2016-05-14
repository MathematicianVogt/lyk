import redis 

x=redis.Redis()
print str(x.keys())