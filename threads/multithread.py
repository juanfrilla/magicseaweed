from threadingresult import ThreadWithReturnValue
from streamlit.runtime.scriptrunner import add_script_run_ctx
from msw_scraper import MSWScraper
import utils
import pandas as pd


def process_scrape_forecast(beach_data):
    url = beach_data["url"]
    beach = beach_data["beach"]
    msw_scraper = MSWScraper()

    forecast = msw_scraper.scrape(url)

    forecast = utils.add_beach_to_forecast(forecast, beach)
    df = utils.forecast_to_df(forecast)

    return df


def scrape_multiple_sites(beachs_data):
    threads = list()

    forecast = pd.DataFrame()

    for data in beachs_data:

        x = ThreadWithReturnValue(target=process_scrape_forecast, args=(data,))

        add_script_run_ctx(x)
        threads.append(x)
        x.start()

    for thread in threads:
        df = thread.join()
        if df is not None:
            forecast = utils.combine_df(forecast, df)

    return forecast
