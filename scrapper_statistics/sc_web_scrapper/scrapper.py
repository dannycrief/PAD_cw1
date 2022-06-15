import csv
from selenium.webdriver.common.by import By

from scrapper_statistics.common import get_title, get_location, get_price, get_area, \
    get_media_price, get_rooms_number, get_deposit_price, get_floor_number, get_construction_type, get_available_from, \
    get_balcony_garden_terrace, get_advertiser_type, get_is_for_students, get_equipment, get_media, get_heating, \
    get_security, get_windows, get_elevator, get_year_built, get_parking_space, get_building_material, \
    get_additional_information, is_xpath_clickable


class OtoDomScrapper:
    """
    Parent scrapper class that scrape data from OtoDom web page
    """
    __COLUMNS = ['title', 'location', 'price', 'area', 'media_price', 'rooms_number', 'deposit_price', 'floor_number',
                 'construction_type', 'available_from', 'balcony_garden_terrace', 'advertiser_type', 'is_for_students',
                 'equipment', 'media', 'heating', 'security', 'windows', 'elevator', 'parking_space', 'year_built',
                 'building_material', 'additional_information']

    __NEXT_BUTTON_XPATH = "//button[@aria-label='następna strona']"

    def __init__(self, driver):
        """
        Initialize OtoDomScrapper class
        :param driver: selenium web driver
        """
        self.driver = driver

    def parse_data(self, file_name):
        with open(file_name, 'w', encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.__COLUMNS)
            while self.__is_next_button_disabled():
                links = self.driver.find_elements(
                    By.XPATH,
                    value='/html/body/div[1]/div[1]/main/div[1]/div[3]/div[1]/div[2]/div[2]/ul/li/a'
                )
                links_hrefs = [link.get_attribute('href') for link in links]
                for link in links_hrefs:
                    self.driver.get(link)
                    row = self.__parse_element()
                    writer.writerow(row)
                    self.driver.back()
                if not is_xpath_clickable(self.driver, self.__NEXT_BUTTON_XPATH):
                    break
                self.driver.find_element(By.XPATH, "//button[@aria-label='następna strona']").click()

    def __is_next_button_disabled(self):
        return self.driver.find_element(By.XPATH, self.__NEXT_BUTTON_XPATH).get_attribute('disabled') is not None

    def __parse_element(self) -> list:
        title = self.__check_not_null(get_title(self.driver))
        location = self.__check_not_null(get_location(self.driver))  # Tu błąd
        price = self.__check_not_null(get_price(self.driver))
        area = self.__check_not_null(get_area(self.driver))
        media_price = self.__check_not_null(get_media_price(self.driver))
        rooms_number = self.__check_not_null(get_rooms_number(self.driver))
        deposit_price = self.__check_not_null(get_deposit_price(self.driver))
        floor_number = self.__check_not_null(get_floor_number(self.driver))
        construction_type = self.__check_not_null(get_construction_type(self.driver))
        available_from = self.__check_not_null(get_available_from(self.driver))
        balcony_garden_terrace = self.__check_not_null(get_balcony_garden_terrace(self.driver))
        advertiser_type = self.__check_not_null(get_advertiser_type(self.driver))
        is_for_students = self.__check_not_null(get_is_for_students(self.driver))
        equipment = self.__check_not_null(get_equipment(self.driver))
        media = self.__check_not_null(get_media(self.driver))
        heating = self.__check_not_null(get_heating(self.driver))
        security = self.__check_not_null(get_security(self.driver))
        windows = self.__check_not_null(get_windows(self.driver))
        elevator = self.__check_not_null(get_elevator(self.driver))
        parking_space = self.__check_not_null(get_parking_space(self.driver))
        year_built = self.__check_not_null(get_year_built(self.driver))
        building_material = self.__check_not_null(get_building_material(self.driver))
        additional_information = self.__check_not_null(get_additional_information(self.driver))
        return [title, location, price, area, media_price, rooms_number, deposit_price, floor_number, construction_type,
                available_from, balcony_garden_terrace, advertiser_type, is_for_students, equipment, media, heating,
                security, windows, elevator, parking_space, year_built, building_material, additional_information]

    @classmethod
    def __check_not_null(cls, string: str):
        return string if string.lower() not in ["zapytaj", "brak informacji"] else ""
