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


def combine_df_tides(df, tides_data):
    #tides_data = tides_data[:12]
    tides_data = {k: tides_data[k] for k in list(tides_data)[:12]}

    for (index, row) in df.iterrows():
        if 'AM' in row['time'] and 'Subiendo' in tides_data[row['days']][0]:
            value = tides_data[row['days']][0]

        elif 'AM' in row['time'] and 'Bajando' in tides_data[row['days']][0]:
            value = tides_data[row['days']][1]

        # elif 'Bajando' in tides_data[row['days']][0] and 'Bajando' in tides_data[row['days']][1]: TODO corregir que está bajando en dos
        #     value = tides_data[row['days']][1]
        #     print("sssssir", tides_data[row['days']])

        elif 'PM' in row['time'] and 'Subiendo' in tides_data[row['days']][1]:
            value = tides_data[row['days']][1]
        elif 'PM' in row['time'] and 'Bajando' in tides_data[
                row['days']][1] and len(tides_data[row['days']]) > 2:
            value = tides_data[row['days']][2]
        # elif 'PM' in row['time'] and 'Bajando' in tides_data[row['days']][1] and len(tides_data[row['days']]) < 2:
        #     value = tides_data[row['days']][1]
        #     print("No lo usa")
        elif 'Night' in row['time'] and len(tides_data[row['days']]) > 2:
            value = tides_data[row['days']][2]
        elif 'Night' in row['time'] and len(tides_data[row['days']]) < 2:
            value = "-"
        df.loc[index, "tides"] = value
    return df


def hour_AM_PM(hours_dict):
    AM = [time(0, 0, 0), time(12, 0, 0)]
    PM = [time(12, 0, 0), time(20, 0, 0)]
    Night = [time(20, 0, 0), time(23, 59, 0)]

    new_dict = {}

    for key, value in hours_dict.items():
        new_list = []
        for element in value:
            if element is not None:
                h_m = element.split(" ")[1].replace("h", "")
                time_to_check = datetime.strptime(f"{h_m}:00",
                                                  "%H:%M:%S").time()

                if time_to_check > AM[0] and time_to_check < AM[1]:
                    text = check_ple_baj(f"{element} AM")
                elif time_to_check > PM[0] and time_to_check < PM[1]:
                    text = check_ple_baj(f"{element} PM")
                elif time_to_check > Night[0] and time_to_check < Night[1]:
                    text = check_ple_baj(f"{element} Night")
                new_list.append(text)
        new_dict[key] = new_list

    return new_dict


# Function to convert the date format
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


# def format_hour(tide_info, hour):
#     print("yeeeka", hour)
#     print(tide_info)
#     if len(hour.strip()) == 4:
#         hour = "0" + hour.strip()

#     if len(tide_info) <= 2: #estaba <=
#         hour = hour.replace("12:", "00:")
#         hour = hour.replace("AM", " AM")
#         print("!deeentroxxxxx", hour)
#         return f"{hour.strip()}"
#     else:
#         hour = hour.replace("PM", " PM")
#         print("!deeentrokkkk", hour)
#         return f"{hour.strip()}"


def check_ple_baj(text):
    if "ple" in text:
        return text.replace("ple", "Subiendo hasta las")
    elif "baj" in text:
        return text.replace("baj", "Bajando hasta las")


#TODO Posiblemente ponerle desde las hasta las


def get_greater_hour(my_dict):
    new_dict = {}
    for key, value in my_dict.items():
        AM_list = []
        PM_list = []
        Night_list = []

        for element in value:
            if element is not None and "AM" in element:
                AM_list.append(element)
            elif element is not None and "PM" in element:
                PM_list.append(element)
            elif element is not None and "Night" in element:
                Night_list.append(element)

        #TODO quedarme de aqui la subida y no la bajada
        if len(AM_list) > 1 and Night_list != []:
            new_dict[key] = [AM_list[1], PM_list[0], Night_list[0]]
        elif (len(AM_list) < 1 and Night_list != []) or (len(PM_list) < 1
                                                         and Night_list != []):
            new_dict[key] = [AM_list[0], PM_list[0], Night_list[0]]
        elif len(AM_list) > 1 and Night_list == []:
            new_dict[key] = [AM_list[1], PM_list[0]]
        elif (len(AM_list) < 1 and Night_list == []) or (len(PM_list) < 1
                                                         and Night_list == []):
            new_dict[key] = [AM_list[0], PM_list[0]]

        elif len(PM_list) > 1 and Night_list != []:
            new_dict[key] = [AM_list[0], PM_list[1], Night_list[0]]
        elif len(PM_list) > 1 and Night_list == []:
            new_dict[key] = [AM_list[0], PM_list[1]]

    return new_dict


def process_scrape_forecast(url, beach):
    msw_scraper = MSWScraper()
    
    msw_scraper.driver.get(url)

    msw_scraper.prepare_site()
    forecast = msw_scraper.scrape()

    forecast = add_beach_to_forecast(forecast, beach)
    df = forecast_to_df(forecast)
    
    msw_scraper.driver.quit()
    return df

    #return df TODO devolver datframe aqui




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



