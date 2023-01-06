import msw_scraper


def test_scrape():
    url = "https://es.magicseaweed.com/Playa-de-Janubio-Surf-Report/204/"
    scraper = msw_scraper.MSWScraper()
    forecast = scraper.scrape(url)

    assert forecast != {}
    assert forecast is not None
    assert type(forecast) == dict
