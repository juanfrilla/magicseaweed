from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import utils

class MSWScraper(object):

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(
            executable_path=r"/usr/bin/chromedriver", chrome_options=options)

    def page_is_loaded(self):
        x = self.driver.execute_script("return document.readyState")
        if x == "complete":
            return True
        return False

    def prepare_site(self):
        #self.driver.get(url)
        all_iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        if len(all_iframes) > 0:
            self.driver.execute_script("""
                var elems = document.getElementsByTagName("iframe"); 
                for(var i = 0, max = elems.length; i < max; i++)
                    {
                        elems[i].hidden=true;
                    }
                                """)

    def scrape(self):
        forecast = {"date": [], "time": [], "wind_state": [], "tides": []}
        if self.page_is_loaded():
            s = BeautifulSoup(self.driver.page_source, "html.parser")
            table = s.find(
                "table",
                class_=
                "table table-primary table-forecast allSwellsActive msw-js-table msw-units-large"
            )

            tablebodies = table.find_all(name="tbody", recursive=False)

            for tablebody in tablebodies:
                rows = tablebody.find_all("tr")
                for row in rows:
                    if 'data-date-anchor' in row.attrs:
                        r_date = ''.join(
                            filter(str.isdigit,
                                   row['data-date-anchor'].strip()))

                    cells = row.find_all("td")
                    tide_info = []
                    for index, cell in enumerate(cells):
                        if 'class' in cell.attrs:
                            class_cell = " ".join(cell['class']).strip()
                            if class_cell == "nopadding-left row-title background-clear msw-js-tooltip":
                                c_time = (cell.text.strip()).replace(
                                    "12am", "0am")
                                forecast["date"].append(r_date)
                                forecast["time"].append(c_time)
                            elif class_cell in [
                                    "text-center last msw-js-tooltip td-square background-warning",
                                    "text-center last msw-js-tooltip td-square background-success",
                                    "text-center last msw-js-tooltip td-square background-danger"
                            ]:
                                forecast["wind_state"].append(
                                    cell['data-original-title'])

                        if 'class' in row.attrs:
                            class_row = " ".join(row['class']).strip()
                            if "background-clear msw-js-tide" in class_row and index != 0:
                                if "Marea" in cell.text and len(tide_info) < 8:
                                    tide = cell.text
                                    tide = utils.format_tide(tide)
                                elif ":" in cell.text and len(tide_info) < 8:
                                    hour = utils.format_hour(
                                        tide_info, cell.text)
                                    hour = utils.convert24(hour)

                                    tide_info.append(tide)
                                    tide_info.append(hour.strip())

                                if index == 10 and cell.text.strip(
                                ) == "Amanecer":
                                    tide_info = utils.get_tide_info_list(
                                        tide_info)

                                    for element in tide_info:
                                        forecast["tides"].append(element)
                                    break

                                if index == len(cells) - 1:
                                    tide_info = utils.get_tide_info_list(
                                        tide_info)
                                    for element in tide_info:
                                        forecast["tides"].append(element)

        return forecast