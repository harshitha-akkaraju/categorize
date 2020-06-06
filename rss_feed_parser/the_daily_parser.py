from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

THE_DAILY_RSS_FEED_URL = "http://rss.art19.com/the-daily"

class TheDailyParser:
    def __init__(self):
        self.url = THE_DAILY_RSS_FEED_URL

    def __parse_feed(self):
        reader = urlopen(self.url)
        page = reader.read()
        reader.close()

        page_content = BeautifulSoup(page, "xml")
        item_list = page_content.findAll("item")
        item_durations = page_content.findAll("itunes:duration")

        daily_episodes = {}
        dates = []
        durations = []
        descriptions = []
        links = []
        titles = []

        for i, item in enumerate(item_list):
            title = item.title.text
            description = item.description.text
            date = item.pubDate.text
            duration = item_durations[i].string
            link = item.enclosure.get('url')

            dates.append(date)
            descriptions.append(description)
            durations.append(duration)
            links.append(link)
            titles.append(title)
        
        daily_episodes["date"] = dates
        daily_episodes["duration"] = durations
        daily_episodes["description"] = descriptions
        daily_episodes["link"] = links
        daily_episodes["title"] = titles
        
        return daily_episodes
    
    def episode_info_as_df(self):
        daily_episodes = self.__parse_feed()
        episode_data_df = pd.DataFrame.from_dict(daily_episodes)
        return episode_data_df