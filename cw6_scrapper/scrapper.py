import os
from os import listdir
from selenium.webdriver.support import expected_conditions as EC
import urllib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

WEBSITE = "https://www.pap.pl/"

driver = webdriver.Firefox()

driver.get(WEBSITE)

accept_cookies = driver.find_element(by=By.CLASS_NAME, value="buttons")
ActionChains(driver).click(accept_cookies).perform()

driver.maximize_window()


def click_li_a(html_list: WebElement, key_word: str):
    for html_elem in html_list.find_elements(by=By.TAG_NAME, value="li"):
        current_item = html_elem.find_element(by=By.TAG_NAME, value='a')
        if key_word in current_item.text.lower():
            current_item.click()


languages = driver.find_element(by=By.CLASS_NAME, value="language")
click_li_a(languages, "en")

en_main_navigation = driver.find_element(by=By.CLASS_NAME, value="menu--main-navigation-en")
click_li_a(en_main_navigation, "business")

BUSINESS_PAGE = driver.current_url

news_titles = []
news_list = driver.find_element(by=By.CLASS_NAME, value="newsList")
for news in news_list.find_elements(by=By.CLASS_NAME, value="news"):
    new_text = news.text
    if new_text != '':
        news_titles.append(new_text)

print(news_titles)

img_list = []
for img in driver.find_elements(by=By.TAG_NAME, value='img'):
    """
    Delete all images if exists and get ulr list of images
    """
    [os.remove(f) for f in listdir(os.getcwd()) if f.__contains__('.jpg')]
    if '.png' not in img.get_attribute('src'):
        img_list.append(img.get_attribute('src').split('?')[0])

for img in img_list:
    """
    Go through img_list and download images to source folder (cw6_scrapper)
    """
    driver.get(img)
    driver.get_screenshot_as_file(img.split('/')[-1])

driver.get(BUSINESS_PAGE)

html = driver.find_element(by=By.TAG_NAME, value='html')
html.send_keys(Keys.END)  # scroll down

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//a[@title="Go to last page"]'))).click()

current_page_nr = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//a[@title="Current page"]')))
print(f'The last page is: {current_page_nr.text}')

driver.close()
