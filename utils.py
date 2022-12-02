import os, pandas as pd, numpy as np
from typing import Dict, List
from datetime import datetime, timedelta

from collections import defaultdict

from threadingresult import ThreadWithReturnValue

from datetime import time, datetime, timedelta

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


def add_days_to_forecast(forecast):
    time_list = forecast['time']
    days_list = []
    date = datetime.now()
    for index, time in enumerate(time_list):
        if time == "AM" and index != 0:
            date += timedelta(days=1)
            days_list.append(date.strftime("%d-%m, %A"))
        else:
            days_list.append(date.strftime("%d-%m, %A"))
    forecast['days'] = days_list
    return forecast


def add_beach_to_forecast(forecast, beach):
    count_row = len(forecast['wind_state'])
    same_beach_list = [beach for i in range(0, count_row)]

    forecast['beach'] = same_beach_list

    return forecast


def combine_df(df1, df2):
    df = pd.concat([df1, df2], axis=0, ignore_index=True)
    return df


def convert24(str1):
    if not 'AM' in str1 and not "12:" in str1:
        in_time = datetime.strptime(str1, "%I:%M %p")
        out_time = datetime.strftime(in_time, "%H:%M")
        return out_time
    return str1.replace("AM", "").replace("PM", "").strip()


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


def format_tide(tide):
    if tide.strip() == "Marea Alta":
        return "Subiendo hasta las"
    elif tide.strip() == "Marea Baja":
        return "Bajando hasta las"


def format_hour(tide_info, hour):
    if len(hour.strip()) == 4:
        hour = "0" + hour.strip()

    if len(tide_info) <= 2:
        hour = hour.replace("12:", "00:")
        return f"{hour.strip()} AM"
    else:
        return f"{hour.strip()} PM"


def format_dataframe(df):
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
