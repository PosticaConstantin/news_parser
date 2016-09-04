## Point.md news parser
Simple news parser for point.md, uses rss feed as source.

Uses [Mongodb](https://www.mongodb.com) v3.2.9 as database using [Motor](http://motor.readthedocs.io/en/stable)
for asynchronous driver and [Tornado](http://www.tornadoweb.org/en/stable/)  web framework.

Please install requirements, before use.

To run parser, run:

```bash
python news_parser.py
```

To run web-server, run:
```bash
python web_server.py
```
