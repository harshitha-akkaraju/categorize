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
            else:
                try:
                    temp = self.driver.find_elements_by_css_selector(LIST_ELEM_CSS_SELECTOR)
                    results.extend(temp)
                except:
                    print("no elements with the said list elem styles")
            
            # time.sleep(3)
            counter += 1

            if counter == 3:
                break

        return results


    def __get_episode_metadata(self, html_elements):
        daily_episodes = {}
        titles = []
        headlines = []
        dates = []
        links = []

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

        return daily_episodes
    
    def __initialize_driver(self):
        # selenium also supports other WebDrivers 
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)
        self.driver.get(URL) 
    

    def __close_driver(self):
        self.driver.quit()


       