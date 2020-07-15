from urllib.request import urlopen

from bs4 import BeautifulSoup
from bs4 import NavigableString

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
            description = self.__get_description(item.description.text)
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
    
    def __get_description(self, text):
        description = ""
        soup = BeautifulSoup(text, "html.parser")

        p_tags = soup.find_all('p')
        if len(p_tags) == 0:
            return text
        
        for p_tag in p_tags:
            description += self.__recurse(p_tag, "") + " "

        ul_tags = soup.find_all('ul')
        for ul_tag in ul_tags:
            description += self.__recurse(ul_tag, "") + " "

        description = description.replace("\n", "")
        return description
    
    def __recurse(self, tag, text):
        if tag.children == None:
            text += tag.get_text()
            return text
        
        temp = ""
        for child in tag.children:
            if isinstance(child, NavigableString):
                temp += child.string + " "
            else:
                temp += self.__recurse(child, text) + " "
        
        return text + temp


    def episode_info_as_df(self):
        daily_episodes = self.__parse_feed()
        episode_data_df = pd.DataFrame.from_dict(daily_episodes)
        return episode_data_df


    def csv_to_text_data(self, data_path, file_path):
        episode_data_df = pd.read_csv(data_path)

        # write title and description to a different file
        titles = episode_data_df["title"].tolist()
        descriptions = episode_data_df["description"].tolist()

        writer = open(file_path,'w')
        for i in range(0, len(titles)):
            line = titles[i] + descriptions[i] + "\n"
            writer.write(line)
        
        writer.close()

    def write_data_to_csv(self, file_path):
        episode_data_df = self.episode_info_as_df()
        episode_data_df.to_csv(file_path, index=False)
