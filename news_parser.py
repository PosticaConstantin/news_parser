import re
import urllib as url
import xml.etree.ElementTree as et
import datetime

import db



def parse():
    web_data = url.urlopen("http://point.md/ro/rss/noutati/")
    str_data = web_data.read()
    xml_data = et.fromstring(str_data)
    channel = xml_data.find("channel")
    items = channel.findall("item")

    for x in items:
        title = x.find('title').text
        link = x.find('link').text
        description = x.find('description').text
        image_found = re.findall('src="(.*)"', description, flags=re.U)
        image = None
        if image_found:
            image = image_found[0]
            description = description.strip('<img src= "%s" /><br />' % image)
        pub_date = x.find('pubDate').text
        pub_date = pub_date.split(',')[1].strip().rstrip(' GMT')
        date = datetime.datetime.strptime(pub_date, "%d %b %Y %H:%M:%S")
        item = {"title": title, "link": link, "description": description, "date": date, "source": "point.md",
                "image": image}
        db.mongo_item_insert(item)
    print '<<< Parsing www.point.md, Done!!! >>>'


if __name__ == "__main__":
    parse()
