from urllib.request import urlopen
from bs4 import BeautifulSoup

THE_DAILY_RSS_FEED_URL = "http://rss.art19.com/the-daily"

class TheDailyParser:
    def __init__(self):
        self.url = THE_DAILY_RSS_FEED_URL

    def parse_feed(self):
        reader = urlopen(self.url)
        page = reader.read()
        reader.close()

        page_content = BeautifulSoup(page, "xml")
        item_list = page_content.findAll("item")

        for item in item_list:
            title = item.title.text
            description = item.description.text
            date = item.pubDate.text

            print(title)
            print(description)
            print(date)

            break