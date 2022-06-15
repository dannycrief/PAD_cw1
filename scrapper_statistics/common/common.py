import os
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException


def wait_for_element_by_xpath(driver, xpath) -> Exception or WebDriverWait:
    """
    Check if xpath exists
    :return: selenium element or custom exception
    """
    try:
        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return element
    except TimeoutException:
        raise Exception(f"Cannot find element {xpath} or page is broken..")


def is_xpath_clickable(driver, xpath) -> bool:
    """
    Check if element with such xpath is clickable
    :param driver: selenium webdriver
    :param xpath: link to element by xpath
    :return: is element clickable
    """
    try:
        return WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath))) is not None
    except:
        return False


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
    wait_for_element_by_xpath(driver, xpath='//*[@id="priceMin"]').send_keys(price)


def set_max_price(driver, price: int):
    wait_for_element_by_xpath(driver, xpath='//*[@id="priceMax"]').send_keys(price)


def set_min_area(driver, area: int):
    wait_for_element_by_xpath(driver, xpath='//*[@id="areaMin"]').send_keys(area)


def set_max_area(driver, area: int):
    wait_for_element_by_xpath(driver, xpath='//*[@id="areaMax"]').send_keys(area)


def set_rooms_number(driver, room_numbers: list):
    wait_for_element_by_xpath(driver, xpath='//*[@id="roomsNumber"]').click()
    ul = wait_for_element_by_xpath(driver,
                                   xpath='/html/body/div[1]/div[1]/main/div[1]/div[2]/div/form/div[2]/div[3]/div/div/div/ul')
    li_options = ul.find_elements(By.TAG_NAME, value='li')
    for li_option in li_options:
        if li_option.text in room_numbers:
            li_option.click()
            print(f"Selected rooms number: {li_option.text}")


def create_csv_dir(path):
    if not os.path.exists(f"{path}/csv_dir"):
        os.makedirs(f"{os.getcwd()}/csv_dir")


def get_title(driver) -> str:
    return wait_for_element_by_xpath(driver=driver, xpath='/html/body/div[1]/main/div[3]/div[2]/header/h1').text


def get_location(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/header/div[2]').text


def get_price(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/header/strong').text


def get_area(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[1]/div/div[1]/div[2]').text


def get_media_price(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[1]/div/div[2]/div[2]').text


def get_rooms_number(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[1]/div/div[3]/div[2]').text


def get_deposit_price(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[1]/div/div[4]/div[2]').text


def get_floor_number(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[1]/div/div[5]/div[2]').text


def get_construction_type(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[1]/div/div[6]/div[2]').text


def get_available_from(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[1]/div/div[7]/div[2]').text


def get_balcony_garden_terrace(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[1]/div/div[8]/div[2]').text


def get_advertiser_type(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[3]/div/div[1]/div[2]').text


def get_is_for_students(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[3]/div/div[2]/div[2]').text


def get_equipment(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[3]/div/div[3]/div[2]').text


def get_media(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[3]/div/div[4]/div[2]').text


def get_heating(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[3]/div/div[5]/div[2]').text


def get_security(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[3]/div/div[6]/div[2]').text


def get_windows(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[3]/div/div[7]/div[2]').text


def get_elevator(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[3]/div/div[7]/div[2]').text


def get_parking_space(driver) -> str:
    return wait_for_element_by_xpath(driver, xpath='/html/body/div[1]/main/div[3]/div[2]/div[3]/div/div[9]/div[2]').text


def get_year_built(driver) -> str:
    return wait_for_element_by_xpath(driver,
                                     xpath='/html/body/div[1]/main/div[3]/div[2]/div[3]/div/div[10]/div[2]').text


def get_building_material(driver) -> str:
    return wait_for_element_by_xpath(driver,
                                     xpath='/html/body/div[1]/main/div[3]/div[2]/div[3]/div/div[11]/div[2]').text


def get_additional_information(driver) -> str:
    return wait_for_element_by_xpath(driver,
                                     xpath='/html/body/div[1]/main/div[3]/div[2]/div[3]/div/div[12]/div[2]').text
