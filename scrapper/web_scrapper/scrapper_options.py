import selenium.common.exceptions
from selenium import webdriver
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class OtoDomScrapperOptions:
    def __init__(self, link: str, maximize_window: bool = False, accept_cookies: bool = False):
        """
        Initialize OtoDomScraper class
        :param link:
        :param maximize_window:
        :param accept_cookies:
        """
        self.link = link
        self.maximize_window = maximize_window
        self.accept_cookies = accept_cookies
        self.driver = None

        if not self.__is_reachable():
            raise Exception("Link is unreachable")

    def get_scrapper(self):
        """
        Set driver to Firefox and accept cookies if user set parametr
        :return: None
        """
        self.driver = webdriver.Firefox()
        if self.maximize_window:
            self.driver.maximize_window()
        self.driver.get(self.link)
        if self.accept_cookies:
            self.__is_xpath_exists(xpath='//*[@id="onetrust-accept-btn-handler"]').click()
            print("Cookies accepted")

    def set_filters(self, house_type: str, rent_buy: str, localisation: str, price_min: int,
                    price_max: int, rooms_number: list, area_min: int, area_max: int):
        """
        Set filters function
        :param area_max:
        :param area_min:
        :param house_type: ['Mieszkania', 'Domy', 'Pokoje', 'Działki', 'Lokale użytkowe', 'Hale i magazyny', 'Garaże']
        :param rent_buy: ['sprzedaz', 'wynajem']
        :param localisation:
        :param price_max:
        :param price_min:
        :param rooms_number: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'MORE']
        :return:None
        """
        house_type_list = ['mieszkania', 'domy', 'pokoje', 'działki', 'lokale użytkowe', 'hale i magazyny', 'garaże']
        rent_buy_list = ['sprzedaz', 'wynajem']
        rooms_number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Więcej niż 10']

        if house_type.lower() not in house_type_list:
            raise Exception(f"{house_type} not in list. Please, select from list: {house_type_list}")
        if rent_buy.lower() not in rent_buy_list:
            raise Exception(f"{rent_buy} not in list. Please, select from list: {rent_buy_list}")
        for rooms in rooms_number:
            if rooms not in rooms_number_list:
                raise Exception(f"{rooms} not in list. Please, select from list: {rooms_number_list}")

        self.driver.get(
            f'https://www.otodom.pl/pl/oferty/{rent_buy.lower()}/{house_type.lower()}/{localisation.lower()}'
        )

        self.__is_xpath_exists(xpath='/html/body/div[1]/div[2]/div/div/span').click()

        self.__set_min_price(price_min)
        self.__set_max_price(price_max)
        self.__set_min_area(area_min)
        self.__set_max_area(area_max)
        self.__set_rooms_number(list(map(str, rooms_number)))

    def end_session(self):
        """
        End driver session
        :return: None
        """
        self.driver.close()

    def __is_reachable(self) -> bool or SystemExit:
        """
        Check if URL is reachable
        :return: Boolean or Exception
        """
        try:
            get = requests.get(self.link)
            return True if get.status_code == 200 else False
        except requests.exceptions.RequestException as e:
            raise SystemExit(f"{self.link}: is Not reachable \nErr: {e}")

    def __is_xpath_exists(self, xpath=None) -> Exception or WebDriverWait:
        """
        Check if xpath exists
        :return: Boolean or Exception
        """
        try:
            if xpath is None:
                element = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, self.accept_cookies_xpath)))
            else:
                element = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath)))
            return element
        except selenium.common.exceptions.TimeoutException:
            raise Exception(f"Cannot find element {self.accept_cookies_xpath}")

    def __set_min_price(self, price: int):
        self.__is_xpath_exists(xpath='//*[@id="priceMin"]').send_keys(price)

    def __set_max_price(self, price: int):
        self.__is_xpath_exists(xpath='//*[@id="priceMax"]').send_keys(price)

    def __set_min_area(self, area: int):
        self.__is_xpath_exists(xpath='//*[@id="areaMin"]').send_keys(area)

    def __set_max_area(self, area: int):
        self.__is_xpath_exists(xpath='//*[@id="areaMax"]').send_keys(area)

    def __set_rooms_number(self, room_numbers: list):
        self.__is_xpath_exists(xpath='//*[@id="roomsNumber"]').click()
        ul = self.__is_xpath_exists(
            xpath='/html/body/div[1]/div[1]/main/div[1]/div[2]/div/form/div[2]/div[3]/div/div/div/ul')
        li_options = ul.find_elements(By.TAG_NAME, value='li')
        for li_option in li_options:
            if li_option.text in room_numbers:
                li_option.click()
                print(f"Selected rooms number: {li_option.text}")
