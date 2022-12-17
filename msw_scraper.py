from bs4 import BeautifulSoup
import streamlit as st
from requests_html import HTMLSession




import utils

class MSWScraper(object):
    
            
    def scrape(self, url):
        forecast = {
            "date": [],
            "time": [],
            "flatness": [],
            "wind_state": [],
            "tides": [],
            "primary_wave": [],
            "period": [],
            "swell_rate": []
        }
        
        days ={
            0: "Today",
            1: "Tomorrow",
            2: "Day After Tomorrow"
        }
        
        session = HTMLSession()
        r = session.get(url)
        
        
        s = BeautifulSoup(r.html.html, "html.parser")
        table = s.find(
            "table",
            class_=
            "table table-primary table-forecast allSwellsActive msw-js-table msw-units-large"
        )
        
        
        

        tablebodies = table.find_all(name="tbody", recursive=False)

        for index_tb, tablebody in enumerate(tablebodies[0:3]):
            rows = tablebody.find_all("tr")
            
            for row in rows:
                #DATE
                if 'data-date-anchor' in row.attrs:
                    r_date = ''.join(filter(str.isdigit,row['data-date-anchor'].strip()))
                cells = row.find_all("td")
                tide_info = []
                for index, cell in enumerate(cells):
                    if 'class' in cell.attrs:
                        class_cell = " ".join(cell['class']).strip()
                        
                        #TIME
                        if class_cell == "nopadding-left row-title background-clear msw-js-tooltip":
                            c_time = (cell.text.strip()).replace(
                                "12am", "0am")
                            forecast["date"].append(f"{r_date} {days[index_tb]}")
                            forecast["time"].append(c_time)
                        
                        #WIND STATE
                        elif class_cell in [
                                "text-center last msw-js-tooltip td-square background-warning",
                                "text-center last msw-js-tooltip td-square background-success",
                                "text-center last msw-js-tooltip td-square background-danger"
                        ]:
                            forecast["wind_state"].append(
                                cell['title'])
                        
                        #STRENGTH AND PERIOD
                        elif class_cell == "text-center background-gray-lighter":

                            if "m" in cell.text:
                                forecast["primary_wave"].append(cell.text)
                            elif "s" in cell.text:
                                forecast["period"].append(cell.text)
                                
                        #SWELL RATE
                        elif class_cell == "table-forecast-rating td-nowrap":
                            ul = cell.find("ul")
                            lis = ul.find_all("li")

                            swell_rate_list = [
                                li['class'][0] for li in lis
                            ]

                            swell_rate = utils.count_swell_rate(
                                swell_rate_list)

                            forecast['swell_rate'].append(swell_rate)
                        
                        elif class_cell == "text-center background-info table-forecast-breaking-wave":
                            forecast['flatness'] = cell.text
                            #print(cell.text)
                    
                    if 'class' in row.attrs:
                        class_row = " ".join(row['class']).strip()
                        
                        #TIDES
                        if "background-clear msw-js-tide" in class_row and index != 0:
                            table = row.find("table")
                            trs = table.find_all("tr")
                            row_length = len(trs)
                            
                            
                            if "Marea" in cell.text and len(tide_info) < 8:
                                tide = cell.text
                                tide = utils.format_tide(tide)
                            elif ":" in cell.text and len(tide_info) < 8:
                                hour = utils.format_hour(
                                    tide_info, cell.text, row_length)
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