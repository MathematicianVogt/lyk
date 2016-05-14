import tornado.ioloop
import tornado.web
import tornado.template as template
import os
import motor
import bson
import pymongo
import random


class LyketHome(tornado.web.RequestHandler):
    def get(self):
        db = pymongo.MongoClient()
        size=db.lyket.articles.count()
        stories=db.lyket.articles.find().limit(-10)
        print type(stories)
        loader=template.Loader(os.getcwd())
        source=loader.load("index.html").generate(stories=stories)
        self.write(source)

class ArticlePage(tornado.web.RequestHandler):
    def get(self,uuid):
        try:
            db = pymongo.MongoClient()
            size=db.lyket.articles.count()
            article=db.lyket.articles.find_one({'_id':uuid})
            loader=template.Loader(os.getcwd())
            author=""
            for i in range(0,len(article['author'])):
                if (i==len(article['author'])-1):
                    author=author + article['author'][i] + " - "
                else:
                    author=author + article['author'][i]
            source=loader.load("article.html").generate(title=article['title'],sum=article['sum'],url=article['url'],author=author)
            self.write(source)
        except:
            loader=template.Loader(os.getcwd())
            source=loader.load("article_not_found.html")
            self.write(source)




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
            tornado.web.url(r'/', LyketHome) ,tornado.web.url(r'/(?P<uuid>.+)', ArticlePage) 
        ],
        db=database,
        debug=True
    )
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
