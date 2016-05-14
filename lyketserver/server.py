import tornado.ioloop
import tornado.web
import tornado.template as template
import os
import motor
import bson
import pymongo
import random
import uuid
import datetime
from pycket.session import SessionManager


class LyketHome(tornado.web.RequestHandler):

    def get(self):
        
        db = pymongo.MongoClient()
        size=db.lyket.articles.count()
        post_amount=30
        real_amount=size-post_amount
        stories=db.lyket.articles.find({"postnum" : {"$gt" : real_amount}}).sort([("postnum",-1)]])
        loader=template.Loader(os.getcwd())

        try:
            session=SessionManager(self)
            source=loader.load("indexlogged.html").generate(stories=stories,session=session)
            self.write(source)

        except Exception as e:
            print e
            source=loader.load("index.html").generate(stories=stories)
            self.write(source)

        

class ArticlePage(tornado.web.RequestHandler):
    def get(self,uuid):
        try:
            db = pymongo.MongoClient()
            size=db.lyket.articles.count()
            article=db.lyket.articles.find_one({'_id':uuid})

            loader=template.Loader(os.getcwd())
            source=loader.load("article.html").generate(title=article['title'],sum=article['sum'],url=article['url'])
            self.write(source)
        except:
            loader=template.Loader(os.getcwd())
            source=loader.load("article_not_found.html").generate()
            self.write(source)
class AccountCreationHandler(tornado.web.RequestHandler):
    def post(self):
        db = pymongo.MongoClient()
        email = self.get_argument('email', '')
        username=self.get_argument('username', '')
        password=self.get_argument('password', '')

        user_dic = {}
        user_dic['email']=email
        user_dic['username']=username
        user_dic['password']=password
        user_dic['_id'] = uuid.uuid4().hex
        user_dic['birth']=datetime.datetime.now()
        user_dic['bio']=""
        user_dic['comments']=[]
        db.lyket.users.insert(user_dic)
        self.redirect("http://lyket.com/")

class LogoutHandler(tornado.web.RequestHandler):
    def post(self):
        session=SessionManager(self)
        session.delete(self)
        self.redirect("http://lyket.com/")
class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        db = pymongo.MongoClient()
        username=self.get_argument('username')
        password=self.get_argument('password')
        user=db.lyket.users.find_one({'username':username , 'password':password})
        session=SessionManager(self)

        try:
            print str(session['user']['username'])
        except:
            pass

        print "got here"
        if user:
            
            session['user']=user
            print "fuck"
            self.redirect("http://lyket.com/")

        else:
            self.redirect("http://lyket.com/")
class SignUpHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("signup.html")







def main():

    database = motor.motor_tornado.MotorClient()
    database.lyket.articles.create_index(
        'creationtime',
        backgreat=True
    )

    '''
    app = tornado.web.Application([
            tornado.web.url(r'/lyke/(?P<article_id>.+)', LykeHandler),
            tornado.web.url(r'/dislyke/(?P<article_id>.+)', DislykeHandler),
            tornado.web.url(r'/articles', ArticleHandler),
            tornado.web.url(r'/static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.getcwd(), 'static')}),
            tornado.web.url(r'/', HomeHandler)
        ],
        db=database,
        debug=True
    )

    '''
    
    app = tornado.web.Application([
            tornado.web.url(r'/', LyketHome) ,tornado.web.url(r'/signup', SignUpHandler),tornado.web.url(r'/login', LoginHandler) ,tornado.web.url(r'/makeacc', AccountCreationHandler),tornado.web.url(r'/logout', LogoutHandler),tornado.web.url(r'/(?P<uuid>.+)', ArticlePage) 
        ],cookie_secret='4cd86ac2-dba9-4a5c-992a-fc60e5847149',**{
    'pycket': {
        'engine': 'redis',
        'storage': {
            'host': 'localhost',
            'port': 6379,
            'db_sessions': 10,
            'db_notifications': 11,
            'max_connections': 2 ** 31,
        },
        'cookies': {
            'expires_days': 120,
        },
    }})
    




    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
