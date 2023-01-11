from bs4 import BeautifulSoup
from requests_html import HTMLSession

import utils, os
from dotenv import load_dotenv


class MSWScraper(object):
    def __init__(self):
        load_dotenv()

    def scrape(self, url):
        forecast = {
            "date": [],
            "flatness": [],
            "wind_state": [],
            "tides": [],
            "primary_wave": [],
            "period": [],
            "swell_rate": [],
        }

        days = {0: "Hoy", 1: "Mañana", 2: "Pasado"}

        session = HTMLSession()
        r = session.get(url)

        s = BeautifulSoup(r.html.html, "html.parser")

        table_class = (
            "table table-primary table-forecast allSwellsActive msw-js-table msw-units-large"
            if os.getenv("stage") == "DEV"
            else "table table-primary table-forecast allSwellsActive msw-js-table"
        )

        table = s.find(
            "table",
            class_=table_class,
        )

        tablebodies = table.find_all(name="tbody", recursive=False)

        for index_tb, tablebody in enumerate(tablebodies):
            rows = tablebody.find_all("tr")

            for row in rows:
                # DATE
                if "data-date-anchor" in row.attrs:
                    r_date = utils.timestamp_to_datetime(
                        int(row["data-timestamp"].strip())
                    )
                cells = row.find_all("td")
                tide_info = []
                for index, cell in enumerate(cells):
                    if "class" in cell.attrs:
                        class_cell = " ".join(cell["class"]).strip()

                        # TIME
                        if (
                            class_cell
                            == "nopadding-left row-title background-clear msw-js-tooltip"
                        ):
                            if index_tb in [0, 1, 2]:
                                forecast["date"].append(f"{r_date} {days[index_tb]}")
                            else:
                                forecast["date"].append(f"{r_date} Otro día")

                        # WIND STATE
                        elif class_cell in [
                            "text-center last msw-js-tooltip td-square background-warning",
                            "text-center last msw-js-tooltip td-square background-success",
                            "text-center last msw-js-tooltip td-square background-danger",
                        ]:

                            forecast["wind_state"].append(cell["title"])

                        # STRENGTH AND PERIOD
                        elif class_cell == "text-center background-gray-lighter":

                            if "ft" in cell.text.strip():
                                meters = utils.feet_to_m(
                                    str(cell.text.strip()).replace("ft", "")
                                )
                                forecast["primary_wave"].append(meters)
                            elif "m" in cell.text.strip():
                                forecast["primary_wave"].append(
                                    cell.text.strip().replace("m", "")
                                )
                            elif "s" in cell.text.strip():
                                forecast["period"].append(cell.text.strip())

                        # SWELL RATE
                        elif class_cell == "table-forecast-rating td-nowrap":
                            ul = cell.find("ul")
                            lis = ul.find_all("li")

                            swell_rate_list = [li["class"][0] for li in lis]

                            swell_rate = utils.count_swell_rate(swell_rate_list)

                            forecast["swell_rate"].append(swell_rate)

                        elif (
                            class_cell
                            == "text-center background-info table-forecast-breaking-wave"
                        ):
                            if "ft" in cell.text.strip():
                                flats = cell.text.strip().replace("ft", "").split("-")

                                flatness_def = (
                                    f"{utils.feet_to_m(flats[0])}-{utils.feet_to_m(flats[1])}"
                                    if len(flats) == 2
                                    else f"{utils.feet_to_m(flats[0])}"
                                )

                                forecast["flatness"].append(flatness_def)
                            else:
                                forecast["flatness"].append(
                                    cell.text.strip().replace("m", "")
                                )

                    if "class" in row.attrs:
                        class_row = " ".join(row["class"]).strip()

                        # TIDES
                        if "background-clear msw-js-tide" in class_row and index != 0:
                            table = row.find("table")
                            trs = table.find_all("tr")
                            row_length = len(trs)

                            if "Marea" in cell.text.strip() and len(tide_info) < 8:
                                tide = cell.text.strip()
                                tide = utils.format_tide(tide)
                            elif ":" in cell.text.strip() and len(tide_info) < 8:
                                hour = utils.format_tide_time(
                                    tide_info, cell.text.strip(), row_length
                                )
                                hour = utils.convert24(hour)

                                tide_info.append(tide)
                                tide_info.append(hour.strip())

                            if index == 10 and cell.text.strip() == "Amanecer":
                                tide_info = utils.get_tide_info_list(tide_info)

                                for element in tide_info:
                                    forecast["tides"].append(element)
                                break

                            if index == len(cells) - 1:
                                tide_info = utils.get_tide_info_list(tide_info)
                                for element in tide_info:
                                    forecast["tides"].append(element)
        return forecast
