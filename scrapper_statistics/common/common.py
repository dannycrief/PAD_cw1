import os
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException


def is_xpath_exists(driver, xpath) -> Exception or WebDriverWait:
    """
    Check if xpath exists
    :return: Boolean or Exception
    """
    try:
        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return element
    except TimeoutException:
        raise Exception(f"Cannot find element {accept_cookies_xpath}")


def verify_url_is_correct(driver):
    if "cala-polska" in driver.current_url:
        raise Exception(
            "Some parameters you set are invalid. Please set correct house_type or rent_buy or localisation")
    else:
        print("You was redirected to correct search link")


def wait_url_change(driver, url):
    try:
        _is_redirected = False
        while not _is_redirected:
            _is_redirected = WebDriverWait(driver, 3).until(EC.url_changes(url))
        return True
    except TimeoutException:
        raise Exception(f"Page loads is too slow. Try again..")


def is_reachable(link) -> bool or SystemExit:
    """
    Check if URL is reachable
    :return: Boolean or Exception
    """
    try:
        get = requests.get(link)
        return True if get.status_code == 200 else False
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"{link}: is Not reachable \nErr: {e}")


def set_min_price(driver, price: int):
    is_xpath_exists(driver, xpath='//*[@id="priceMin"]').send_keys(price)


def set_max_price(driver, price: int):
    is_xpath_exists(driver, xpath='//*[@id="priceMax"]').send_keys(price)


def set_min_area(driver, area: int):
    is_xpath_exists(driver, xpath='//*[@id="areaMin"]').send_keys(area)


def set_max_area(driver, area: int):
    is_xpath_exists(driver, xpath='//*[@id="areaMax"]').send_keys(area)


def set_rooms_number(driver, room_numbers: list):
    is_xpath_exists(driver, xpath='//*[@id="roomsNumber"]').click()
    ul = is_xpath_exists(driver,
                         xpath='/html/body/div[1]/div[1]/main/div[1]/div[2]/div/form/div[2]/div[3]/div/div/div/ul')
    li_options = ul.find_elements(By.TAG_NAME, value='li')
    for li_option in li_options:
        if li_option.text in room_numbers:
            li_option.click()
            print(f"Selected rooms number: {li_option.text}")


def create_csv_dir(path):
    if not os.path.exists(f"{path}/csv_dir"):
        os.makedirs(f"{os.getcwd()}/csv_dir")
