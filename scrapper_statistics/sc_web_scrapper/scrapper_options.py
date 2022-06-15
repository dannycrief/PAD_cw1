import sys

from selenium import webdriver

from scrapper_statistics.common import *
from scrapper_statistics.sc_web_scrapper import Scrapper
from selenium.webdriver.firefox.options import Options


class OtoDomScrapperOptions(Scrapper):
    """
    Child scrapper class that set options before parse data
    from OtoDom web page
    """

    __FILENAME = ""

    def __init__(self, link: str, maximize_window: bool = True, accept_cookies: bool = False):
        """
        Initialize OtoDomScrapperOptions class
        :param link: URL link to parse data
        :param maximize_window:
        :param accept_cookies:
        """
        self.link = link
        self.maximize_window = maximize_window
        self.accept_cookies = accept_cookies
        self.__get_scrapper()

        if not self.__is_reachable() and len(link) < 1:
            raise Exception("Link is unreachable")
        Scrapper.__init__(self, self.driver)

        print("HINT: You can set filter localisation as 'warszawa' or 'warszawa/bemowo'\n")

        create_csv_dir(os.getcwd())  # create dir for csvs if not exists

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
        house_type_list = ['mieszkanie', 'domy', 'pokoje', 'działki', 'lokale użytkowe', 'hale i magazyny', 'garaże']
        rent_buy_list = ['sprzedaz', 'wynajem']
        rooms_number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Więcej niż 10']

        if house_type.lower() not in house_type_list:
            raise Exception(f"{house_type} not in list. Please, select from list: {house_type_list}")
        if rent_buy.lower() not in rent_buy_list:
            raise Exception(f"{rent_buy} not in list. Please, select from list: {rent_buy_list}")
        for rooms in rooms_number:
            if rooms not in rooms_number_list:
                raise Exception(f"{rooms} not in list. Please, select from list: {rooms_number_list}")

        search_url = f'https://www.otodom.pl/pl/oferty/{rent_buy.lower()}/{house_type.lower()}/{localisation.lower()}'

        self.driver.get(search_url)

        verify_url_is_correct(self.driver)

        wait_for_element_by_xpath(self.driver, xpath='/html/body/div[1]/div[2]/div/div/span').click()  # Close ads

        set_min_price(self.driver, price_min)
        set_max_price(self.driver, price_max)
        set_min_area(self.driver, area_min)
        set_max_area(self.driver, area_max)
        set_rooms_number(self.driver, list(map(str, rooms_number)))

        self.__FILENAME = f"{os.getcwd()}/csv_dir/{rent_buy.lower()}_{house_type.lower()}_{localisation.lower().replace('/', '_')}.csv"

    def search(self):
        wait_for_element_by_xpath(self.driver, xpath='//*[@id="search-form-submit"]').click()
        self.parse_data(self.__FILENAME)  # parse page

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

    def __get_scrapper(self):
        """
        Set driver to Firefox and accept cookies if user set parametr
        :return: None
        """
        fo = Options()
        fo.add_argument("--headless")
        if sys.platform == 'win32':
            self.driver = webdriver.Firefox(executable_path="C:/WebDriver/geckodriver.exe", options=fo)
        elif sys.platform == 'linux':
            self.driver = webdriver.Firefox()  # options=fo
        if self.maximize_window:
            self.driver.maximize_window()  # change on production
        self.driver.get(self.link)
        if self.accept_cookies:
            wait_for_element_by_xpath(self.driver, xpath='//*[@id="onetrust-accept-btn-handler"]').click()
            print("Cookies accepted")
