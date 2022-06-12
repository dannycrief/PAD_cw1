from selenium.webdriver.common.by import By

from scrapper_statistics.common import is_xpath_exists, wait_url_change


class OtoDomScrapper:
    def __init__(self, driver):
        self.driver = driver

    def parse_data(self):
        posts_number = self.__get_ads_number()
        posts_ul = is_xpath_exists(
            driver=self.driver,
            xpath="/html/body/div[1]/div[1]/main/div[1]/div[3]/div[1]/div[2]/div[2]/ul"
        )
        posts_li = posts_ul.find_elements(By.TAG_NAME, value='li')
        for element in posts_li:
            self.__explore_element(element=element)
            self.driver.back()

    def __get_ads_number(self) -> int:
        wait_url_change(self.driver, self.driver.current_url)
        posts_number_xpath = '/html/body/div[1]/div[1]/main/div[1]/div[3]/div[1]/div[1]/div/div/div[1]/strong/span[2]'
        return int(is_xpath_exists(self.driver, posts_number_xpath).text)

    def __explore_element(self, element):
        current_page = self.driver.current_url
        post_a = element.find_element(By.TAG_NAME, 'a')
        self.__parse_element(post_a, current_page)

    def __parse_element(self, ads, current_page):
        ads.click()
        wait_url_change(self.driver, current_page)
