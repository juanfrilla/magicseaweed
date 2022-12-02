import utils
from msw_scraper import MSWScraper

if __name__ == "__main__":
    scraper = MSWScraper()

    urls = [{
        "beach":
        "Famara",
        "url":
        "https://es.magicseaweed.com/Playa-de-Famara-Surf-Report/209/"
    }, {
        "beach":
        "Las Conchas",
        "url":
        "https://es.magicseaweed.com/Playa-de-las-Conchas-Surf-Report/5891/"
    }, {
        "beach": "El Castillo",
        "url": "https://es.magicseaweed.com/Castillo-Surf-Report/8255/"
    }, {
        "beach":
        "Matagorda",
        "url":
        "https://es.magicseaweed.com/Matagorda-Beach-Surf-Report/6850/"
    }, {
        "beach":
        "Las Cucharas",
        "url":
        "https://es.magicseaweed.com/Playa-de-las-Cucharas-Surf-Report/6852/"
    }, {
        "beach":
        "Arrieta",
        "url":
        "https://es.magicseaweed.com/Arrieta-Beach-Surf-Report/6851/"
    }, {
        "beach":
        "Jameos",
        "url":
        "https://es.magicseaweed.com/Jameos-del-Agua-Surf-Report/206/"
    }, {
        "beach": "El Espino",
        "url": "https://es.magicseaweed.com/El-Espino-Surf-Report/6854/"
    }, {
        "beach": "La Santa",
        "url": "https://es.magicseaweed.com/La-Santa-Surf-Report/207/"
    }, {
        "beach": "Caleta Caballo",
        "url": "https://es.magicseaweed.com/Ghost-Town-Surf-Report/208/"
    }, {
        "beach": "San Juan",
        "url": "https://es.magicseaweed.com/San-Juan-Surf-Report/6853/"
    }]

    df = utils.scrape_multiple_sites(urls)

    df[['description', 'wind_state']] = df['wind_state'].str.split(',',
                                                                   1,
                                                                   expand=True)
    df[['wind_state',
        'wind_direction']] = df['wind_state'].str.split('shore',
                                                        1,
                                                        expand=True)
    df['wind_state'] = df.wind_state.apply(lambda s: (s + 'shore').strip())

    df = df.drop(df[(df["wind_state"] != "Offshore")
                    & (df["wind_state"] != "Cross/Offshore")].index)

    df = df.drop(df[(df["time"] == "9pm") | (df["time"] == "0am") |
                    (df["time"] == "3am")].index)

    df = df[[
        "date", "time", "wind_direction", "wind_state", "description", "beach",
        "tides"
    ]]
    
    df.sort_values(by=["date", "beach"], inplace=True, ascending=[True, True])

    utils.df_to_csv("magicseaweed.csv", df)
    scraper.driver.quit()