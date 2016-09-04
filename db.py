import motor.motor_tornado
import tornado.ioloop as ioloop
import settings
import tornado.gen

client = motor.motor_tornado.MotorClient(settings.mongo_host, settings.mongo_port)
db = client.simpalsTest


def insert_callback(result, error):
    print ('result %s' % repr(result))
    ioloop.IOLoop.instance().stop()


def mongo_item_insert(item):
    db.news.insert(item, callback=insert_callback)
    ioloop.IOLoop.instance().start()


@tornado.gen.coroutine
def get_news(skip, take):
    news = yield db.news.find(sort=[('date', -1)], skip=skip, limit=take).to_list(take)
    total = yield db.news.find().count()
    result = {"news": news, "total": total}
    raise tornado.gen.Return(result)


@tornado.gen.coroutine
def add_news(title, description, link, image, source, date):
    new_item = {"title": title, "description": description, "image": image, "link": link, "source": source,
                "date": date,}
    res = yield db.news.insert(new_item)
