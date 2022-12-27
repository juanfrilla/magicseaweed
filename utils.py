import os, re, pandas as pd, numpy as np
from typing import Dict
from datetime import datetime, timedelta

from threadingresult import ThreadWithReturnValue
from streamlit.runtime.scriptrunner import add_script_run_ctx

from datetime import datetime, timedelta

from msw_scraper import MSWScraper
import numpy as np


def df_to_csv(path, df: pd.DataFrame) -> None:
    if os.path.exists(path):
        os.remove(path)

    df.to_csv(path, index=False)

    if os.path.exists(path):
        os.system(f"explorer.exe {path}")


def df_to_html(df: pd.DataFrame) -> None:
    df_html = df.to_html()
    return df_html


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


def format_slot_time(s):
    digit_letter_list = list(filter(None, re.split(r'(\d+)', s)))
    x = [
        element + ":00" if element.isdigit() else element
        for element in digit_letter_list
    ]
    return " ".join(x)


def format_tide_time(tide_info, hour, row_length):
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

    duplicate_list = list(
        set([x for x in joined_list if joined_list.count(x) > 1]))

    joined_list.sort()

    if 'Bajando' in initial_status:
        status = False
    else:
        status = True

    for element in joined_list:
        if element in tide_info:
            status = not status

        if element in tide_list and element not in duplicate_list:
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
            new_list[index] = element.replace("False", "Bajando,")
        elif 'True' in element:
            new_list[index] = element.replace("True", "Subiendo,")

    new_list = [element.split("-")[1] for element in new_list]

    return new_list


def conditions(df: pd.DataFrame) -> pd.DataFrame:
    primary_wave_heigh = df["primary_wave"].str.replace('m', '').astype(float)
    period = df["period"].str.replace('s', '').astype(float)
    flatness_str = df['flatness'].str.strip()
    flatness_heigh = df['flatness'].str.split("-").str[1].str.replace(
        'm', '').str.strip().astype(float)

    #STRENGTH
    STRENGTH = ((primary_wave_heigh >= 1) & (primary_wave_heigh <= 2.5))

    #PERIOD
    PERIOD = (period > 7)

    FLATNESS_STR = (flatness_str != 'Plano')

    FLATNESS_NUM = flatness_heigh >= 1 & (flatness_heigh <= 2.5
                                          )  #flatness_heigh>primary_wave_heigh

    favorable = (STRENGTH & PERIOD & FLATNESS_STR & FLATNESS_NUM)

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


def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)

def format_datetime(dt_obj):
    return datetime.strftime(dt_obj, )


def format_dataframe(df):
    df[['date', 'time', 'date_name']] = df['date'].str.split(' ', 2, expand=True)

    df[['description', 'wind_state']] = df['wind_state'].str.split(',',
                                                                   1,
                                                                   expand=True)
    df[['wind_state',
        'wind_direction']] = df['wind_state'].str.split('shore',
                                                        1,
                                                        expand=True)
    df['wind_state'] = df.wind_state.apply(lambda s: (s + 'shore').strip())

    df[['tides_state', 'tides_hour']] = df['tides'].str.split(',',
                                                              1,
                                                              expand=True)

    df = conditions(df)

    df = df.drop(df[(df["wind_state"] != "Offshore")
                    & (df["wind_state"] != "Cross/Offshore")].index)

    df = df.drop(df[(df["time"] == "21:00:00") | (df["time"] == "00:00:00") |
                    (df["time"] == "03:00:00")].index)

    df = df[[
        "date_name", "date", "time", "beach", "tides_state", "tides_hour",
        "flatness", "primary_wave", "period", "swell_rate", "wind_direction",
        "wind_state", "description", "approval"
    ]]

    df['date_name'] = pd.Categorical(
        df['date_name'],
        ["Today", "Tomorrow", "Day After Tomorrow", "Another Day"])
    
    df["date"] = df["date"].astype('datetime64[ns]')

    df.sort_values(by=["date_name", "date", "beach"],
                   inplace=True,
                   ascending=[True, True, True])
    ##
    df["date"] = df["date"].astype('str')
    df["date"] = df["date"].str.replace("T00:00:00", "")
    df["time"] = df["time"].str.replace(":00:00", ":00")
    ##

    return df


def process_scrape_forecast(beach_data):
    url = beach_data['url']
    beach = beach_data['beach']

    msw_scraper = MSWScraper()

    forecast = msw_scraper.scrape(url)

    forecast = add_beach_to_forecast(forecast, beach)
    df = forecast_to_df(forecast)

    return df


def scrape_multiple_sites(beachs_data):
    threads = list()

    forecast = pd.DataFrame()

    for data in beachs_data:

        x = ThreadWithReturnValue(target=process_scrape_forecast,
                                  args=(data, ))

        add_script_run_ctx(x)
        threads.append(x)
        x.start()

    for thread in threads:
        df = thread.join()
        if df is not None:
            forecast = combine_df(forecast, df)

    return forecast
