import os, pandas as pd, numpy as np
from typing import Dict
from datetime import datetime, timedelta

from threadingresult import ThreadWithReturnValue

from datetime import datetime, timedelta

from msw_scraper import MSWScraper


def df_to_csv(path, df: pd.DataFrame) -> None:
    if os.path.exists(path):
        os.remove(path)

    df.to_csv(path, index=False)

    if os.path.exists(path):
        os.system(f"explorer.exe {path}")


def forecast_to_df(dict: Dict) -> pd.DataFrame:
    df = pd.DataFrame(dict)

    return df


def add_beach_to_forecast(forecast, beach):
    count_row = len(forecast['wind_state'])
    same_beach_list = [beach for i in range(0, count_row)]

    forecast['beach'] = same_beach_list

    return forecast


def combine_df(df1, df2):
    df = pd.concat([df1, df2], axis=0, ignore_index=True)
    return df


def convert24(str1):
    in_time = datetime.strptime(str1, "%I:%M %p")
    out_time = datetime.strftime(in_time, "%H:%M")
    return out_time


def format_hour(tide_info, hour, row_length):
    if len(hour.strip()) == 4:
        hour = "0" + hour.strip()

    if (len(tide_info) < 4
            and row_length == 4) or (len(tide_info) < 4 and row_length == 3
                                     and "12:" not in hour):
        return f"{hour.strip()} AM"

    elif (len(tide_info) < 4 and "12:" in hour
          and row_length == 3) or (len(tide_info) >= 4):
        return f"{hour.strip()} PM"


def get_tide_info_list(tide_info):
    new_list = []
    initial_status = tide_info[0]
    i = 0

    tide_list = list(filter(lambda element: ':' in element, tide_info))
    forecast_list = [
        "00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"
    ]

    joined_list = tide_list + forecast_list
    joined_list.sort()

    if 'Bajando' in initial_status:
        status = False
    else:
        status = True

    for element in joined_list:
        if element in tide_info:
            status = not status

        if element in tide_list:
            i += 1
        if i < len(tide_list):
            till_tide = tide_list[i]
        else:
            till_tide = (datetime.strptime(tide_list[-1], "%H:%M") +
                         timedelta(hours=6, minutes=12.5)).strftime("%H:%M")

        new_list.append(f"{element}-{status} hasta las {till_tide}")

    for element in new_list:
        if element.split("-")[0] in tide_list:
            new_list.remove(element)

    for index, element in enumerate(new_list):
        if 'False' in element:
            new_list[index] = element.replace("False", "Bajando")
        elif 'True' in element:
            new_list[index] = element.replace("True", "Subiendo")

    new_list = [element.split("-")[1] for element in new_list]

    return new_list


def conditions(df: pd.DataFrame) -> pd.DataFrame:
    strength = df["strength"].str.replace('m', '').astype(float)
    period = df["period"].str.replace('s', '').astype(float)

    #STRENGTH
    STRENGTH = ((strength >= 1) & (strength <= 2.5))

    #PERIOD
    PERIOD = (period > 7)

    favorable = (STRENGTH & PERIOD)

    default = "No Favorable"

    str_list = ["Favorable"]

    df["approval"] = np.select(
        [favorable],
        str_list,
        default=default,
    )
    return df


def format_tide(tide):
    if tide.strip() == "Marea Alta":
        return "Subiendo hasta las"
    elif tide.strip() == "Marea Baja":
        return "Bajando hasta las"


def count_swell_rate(swell_rate_list):
    active = swell_rate_list.count("active")
    inactive = swell_rate_list.count("inactive")

    return f"{active}/{inactive}"


def format_dataframe(df):
    df[['description', 'wind_state']] = df['wind_state'].str.split(',',
                                                                   1,
                                                                   expand=True)
    df[['wind_state',
        'wind_direction']] = df['wind_state'].str.split('shore',
                                                        1,
                                                        expand=True)
    df['wind_state'] = df.wind_state.apply(lambda s: (s + 'shore').strip())

    df = conditions(df)

    df = df.drop(df[(df["wind_state"] != "Offshore")
                    & (df["wind_state"] != "Cross/Offshore")].index)

    df = df.drop(df[(df["time"] == "9pm") | (df["time"] == "0am") |
                    (df["time"] == "3am")].index)

    df = df[[
        "date", "time", "strength", "period", "swell_rate", "wind_direction",
        "wind_state", "description", "beach", "tides", "approval"
    ]]
    df.sort_values(by=["date", "beach"], inplace=True, ascending=[True, True])

    return df


def process_scrape_forecast(url, beach):
    msw_scraper = MSWScraper()

    msw_scraper.driver.get(url)

    msw_scraper.prepare_site()
    forecast = msw_scraper.scrape()

    forecast = add_beach_to_forecast(forecast, beach)
    df = forecast_to_df(forecast)

    msw_scraper.driver.quit()
    return df


def scrape_multiple_sites(urls):
    threads = list()

    forecast = pd.DataFrame()

    for element in urls:
        url = element['url']
        beach = element['beach']
        x = ThreadWithReturnValue(target=process_scrape_forecast,
                                  args=(url, beach))
        threads.append(x)
        x.start()

    for thread in threads:
        df = thread.join()
        if df is not None:
            forecast = combine_df(forecast, df)

    return forecast
