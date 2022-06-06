from scrapper.scrapper import OtoDomScrapper

if __name__ == "__main__":
    sc = OtoDomScrapper(
        "https://otodom.pl",
        accept_cookies=True,
        accept_cookies_xpath='//*[@id="onetrust-accept-btn-handler"]'
    )
    sc.get_scrapper()
    sc.set_filters(house_type='Mieszkania', rent_buy='wynajem',
                   localisation='Warszawa', price_min=10,
                   price_max=10000, rooms_number=['one', 'two'],
                   area_min=10, area_max=250)
    sc.end_session()
