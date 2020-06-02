import requests
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

URL = 'https://www.nytimes.com/column/the-daily'
CHROME_DRIVER_PATH = './chromedriver'

class TheDailyScraper:
    def __init__(self):
        self.__initialize_driver()
    
    def get_episode_data(self):
        print("retrieving html elements...")
        print()
        html_elements = self.__get_html_elements()

        episode_metadata = self.__get_episode_metadata(html_elements)

        self.__close_driver()
        return episode_metadata

    def __get_html_elements(self):
        num_iterations = 88
        counter = 1
        results = []

        while counter <= num_iterations:
            print("loading results from section: ", counter)

            SHOW_MORE_BUTTON_CSS_SELECTOR = '#stream-panel > div.css-13mho3u > div > div > div > button'
            LIST_ELEM_CSS_SELECTOR = '#stream-panel > div.css-13mho3u > ol > li'

            try:
                button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, SHOW_MORE_BUTTON_CSS_SELECTOR)))
                button.click()
            except:
                print("unable to click on the `Show More` button")
            
            time.sleep(3)
            counter += 

        results = self.driver.find_elements_by_css_selector(LIST_ELEM_CSS_SELECTOR) 
        return results

    def __get_episode_metadata(self, html_elements):
        daily_episodes = {}
        titles = []
        headlines = []
        dates = []
        links = []

        print("compiling episode metadata...")
        print()
        for elem in html_elements:
            title_tag = elem.find_element_by_tag_name('h2')
            headline_tag = elem.find_element_by_tag_name('p')
            time_tag = elem.find_element_by_tag_name('time')
            ref_tag = elem.find_element_by_tag_name('a')

            title = title_tag.get_attribute('innerHTML')
            headline = headline_tag.get_attribute('innerHTML')
            date = time_tag.get_attribute('innerHTML')
            link = ref_tag.get_attribute('href')
            
            titles.append(title)
            headlines.append(headline)
            dates.append(date)
            links.append(link)

        daily_episodes["title"] = titles
        daily_episodes["headline"] = headlines
        daily_episodes["date"] = dates
        daily_episodes["link"] = links
        daily_episodes["description"] = self.__get_episode_descriptions(daily_episodes)
        return daily_episodes
    
    def __get_episode_descriptions(self, episode_metadata):
        links = episode_metadata["link"]
        descriptions = []

        print("retrieving episode descriptions...")
        print()
        for link in links:
            response = requests.get(link)
            page_content = BeautifulSoup(response.text, 'html.parser')

            DESCRIPTION_SECTION_CLASS_NAME = 'css-53u6y8'
            P_TAGS_CLASS_NAME = 'css-158dogj evys1bk0'

            section_tag = page_content.find('div', class_=DESCRIPTION_SECTION_CLASS_NAME)
            p_tags = section_tag.find_all('p', class_=P_TAGS_CLASS_NAME)
            # concatenate description paragraphs
            description = ''
            for i in range(len(p_tags)):
                if i != 0:
                    description += (p_tags[i].text + '\n')

            descriptions.append(description)
        
        return descriptions


    def __initialize_driver(self):
        # selenium also supports other WebDrivers 
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)
        self.driver.get(URL) 
    

    def __close_driver(self):
        self.driver.quit()


       