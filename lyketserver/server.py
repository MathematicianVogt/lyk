import tornado.ioloop
import tornado.web
import tornado.template as template
import os
import motor
import bson


class LyketHome(tornado.web.RequestHandler):
    def get(self):
        database = self.settings['db']
        entry=database.lyket.articles.find_one()
        res= {}
        res['title']="dongs"
        res['sum']="sumarrydomgs"
        loader=template.Loader(os.getcwd())
        source=loader.load("index.html").generate(title="dongs",sum="pi")
        self.write(source)

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            os.path.join(
                os.getcwd(), 
                'static', 
                'modules', 
                'lyket', 
                'lyket.html'
            )
        )

class ArticleHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):

        database = self.settings['db']

        articles = database.lyket.articles.find().sort('creationtime', -1).limit(10)
        articles = yield articles.to_list(10)

        for article in articles:
            article['_id'] = str(article['_id'])
            article['creationtime'] = article['creationtime'].isoformat()
            if article['pub']:
                article['pub'] = article['pub'].isoformat()

        self.write({'results': articles})

class LykeHandler(tornado.web.RequestHandler):
    def get(self, article_id=''):

        db = pymongo.MongoClient()

        db.lyket.articles.update({
            '_id': bson.objectid.ObjectId(article_id)},
            {'$inc': {'likes': 1}
        })

        self.write('successful')

class DislykeHandler(tornado.web.RequestHandler):
    def get(self, article_id=''):

        db = pymongo.MongoClient()

        db.lyket.articles.update({
            '_id': bson.objectid.ObjectId(article_id)},
            {'$inc': {'dislikes': 1}
        })

        self.write('successful')

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
            tornado.web.url(r'/', LyketHome)
        ],
        db=database,
        debug=True
    )
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
