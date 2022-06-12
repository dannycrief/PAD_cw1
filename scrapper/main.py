from scrapper.web_scrapper.scrapper_options import OtoDomScrapperOptions

if __name__ == "__main__":
    sc_options = OtoDomScrapperOptions(
        "https://otodom.pl",
        accept_cookies=True,
    )
    sc_options.get_scrapper()
    sc_options.set_filters(house_type='Mieszkania', rent_buy='wynajem',
                           localisation='Warszawa', price_min=10,
                           price_max=10000, rooms_number=[1, 2],
                           area_min=10, area_max=250)
    sc_options.end_session()
