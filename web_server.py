import base64
import datetime

import tornado.ioloop
import tornado.web
import tornado.gen

import settings
import db


class MainHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        take = 20
        page = self.get_argument("page", default="1")
        page = int(page)
        skip = (page - 1) * take
        news_result = yield db.get_news(skip=skip, take=take)
        news = news_result["news"]
        total = news_result["total"]
        total_pages = total / take
        self.render('index.html', news=news, page=page, take=take, total_pages=total_pages, )


class NewPostHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render('new_post.html')

    @tornado.gen.coroutine
    def post(self):
        title = self.get_argument("title", "")
        description = self.get_argument("description", "")
        link = self.get_argument("link", "")
        image = None
        if self.request.files:
            content_type = self.request.files["image"][0].content_type
            image_base64 = unicode(base64.b64encode(self.request.files["image"][0].body))
            image = u"data:" + content_type + u";base64," + image_base64
        source = self.get_argument("source", "")
        date = datetime.datetime.now()
        new_posts = yield db.add_news(description=description, title=title, link=link, image=image, source=source,
                                      date=date)
        self.redirect('/')


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/upload", NewPostHandler),
    ], template_path="templates")


if __name__ == "__main__":
    print 'started http://127.0.0.1:{0}'.format(settings.listener_port)
    app = make_app()
    app.listen(settings.listener_port)
    tornado.ioloop.IOLoop.current().start()
