import requests
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


URL = 'https://www.nytimes.com/column/the-daily'
CHROME_DRIVER_PATH = './chromedriver'

browser = webdriver.Chrome(CHROME_DRIVER_PATH)
browser.get(URL)

num_iterations = 88
counter = 1
results = []

while counter <= num_iterations:
    print("loading results from section: ", counter)

    SHOW_MORE_BUTTON_CSS_SELECTOR = '#stream-panel > div.css-13mho3u > div > div > div > button'
    LIST_ELEM_CSS_SELECTOR = '#stream-panel > div.css-13mho3u > ol > li'

    try:
       button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, SHOW_MORE_BUTTON_CSS_SELECTOR)))
       button.click()
    except:
       print("unable to click on the `Show More` button")
    else:
        try:
            temp = browser.find_elements_by_css_selector(LIST_ELEM_CSS_SELECTOR)
            results.extend(temp)
        except:
            print("no elements with the said list elem styles")
    
    # time.sleep(3)
    counter += 1

    if counter == 2:
        break

for elem in results:
    title_tag = elem.find_element_by_tag_name('h2')
    headline_tag = elem.find_element_by_tag_name('p')
    time_tag = elem.find_element_by_tag_name('time')
    ref_tag = elem.find_element_by_tag_name('a')

    title = title_tag.get_attribute('innerHTML')
    headline = headline_tag.get_attribute('innerHTML')
    date = time_tag.get_attribute('innerHTML')
    link = ref_tag.get_attribute('href')
    
    print(title)
    print(headline)
    print(date)
    print(link)
    break

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()


