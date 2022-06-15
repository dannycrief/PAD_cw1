from scrapper_statistics.sc_web_scrapper import ScrapperOptions

if __name__ == "__main__":
    sc = ScrapperOptions(
        link="https://otodom.pl/",
        accept_cookies=True,
    )

    sc.set_filters(
        house_type='Mieszkanie', rent_buy='wynajem', localisation='warszawa/wola',
        price_min=2000, price_max=2750, rooms_number=[1],
        area_min=25, area_max=45
    )

    sc.search()

    sc.end_session()
