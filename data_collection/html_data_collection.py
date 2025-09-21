import requests
import pandas as pd
from lxml import html
from urllib.parse import urljoin
from base.base_classes import IWeatherSource

base_url = "https://meteo.arso.gov.si/met/en/service2/"
table_url = "observation_si/index.html"
city_data_url = "history.html"
class HtmlDataCollection(IWeatherSource):
    def __init__(self,url:str = base_url):
        self.url = url
    ''' Function fetch_data fetches the data from a given URL.
        The function finds first the link to the page of table
        with the data of the weather for all the cities.
        Then from this the function finds the separate links
        for each city with the weather data in the last 48h and
        saves them in a list.
        @param: url
        @return: list of links of weather data in the last 48 by each city
    '''
    def fetch_data(self):
        r_main_link = requests.get(self.url,timeout=20)
        r_main_link.raise_for_status()
        list_of_links = html.fromstring(r_main_link.content)
        link = list_of_links.xpath(f"//a[contains(@href,'{table_url}')]/@href")[0]
        full_data_url = urljoin(self.url, link)
        r_data = requests.get(full_data_url)
        list_data_links = html.fromstring(r_data.content)
        data_links = list_data_links.xpath(f"//a[contains(@href, '{city_data_url}')]/@href")
        full_data_links = []
        for i in data_links:
            full_data_links.append(urljoin(self.url, i))
        return full_data_links

    '''Function that creates a dataframe for a city from a provided url (HTML link).
       The function goes through the HTML and saves data by row.
       Since the wind column is presented with mini icons and not text,
       the function has to iterate through the HTML file in order to save
       this weather parameter in text form (looking at rows of <img src).
        The function additionally processes and returns the processed dataframe 
        with columns where temperature, wind and pressure are present.
        
        @param: url - city URL (HTML link)
        @return df_city_data - dataframe with columns containing wind, temperature and pressure
    '''

    def fetch_city_data(self, url):
    # Saving column names
        df = pd.read_html(url)[0]
        column_names = df.columns.values
    # Extracting data from URL and creating a dataframe
        r_city_data = requests.get(url,timeout=20)
        r_city_data.raise_for_status()
        city_data = html.fromstring(r_city_data.content)
        rows = []
        for tr in city_data.xpath("//table//tr[td]"):
            tds = tr.xpath("./td")
            if not tds:
                continue
            row = []
            for td in tds:
                img = td.xpath(".//img/@src")
                if img:
                    val = img[0].split("/")[-1].replace(".png", "")
                else:
                    val = td.text_content().strip()
                row.append(val)
            rows.append(row)

        df = pd.DataFrame(rows, columns=column_names)
        candidate = self.column_candidates(df)
        df_city_data = df[candidate]
        print("Columns for the processed dataframe are: \n", df_city_data.columns.values)
        print("\n")
        print("The processed dataframe: \n", df_city_data)
        return df_city_data

    ''' Function that returns column candidates of a dataframe for presenting
            weather data in the last 48 hours. The function accepts
            the dataframe as a parameter.
            @param: df - dataframe
            @return: column_list - list of column candidates for presenting weather data
    '''
    def column_candidates(self,df):
        # Column candidate list
        candidates = ["wind", "temperature", "pressure"]
        column_names = df.columns.values
        # Defining the column list with the first column to not lose time data
        column_list = [column_names[0]]
        for i in column_names:
            k = i.lower()
            for j in candidates:
                if j in k:
                    column_list.append(i)
        return column_list


url = "https://meteo.arso.gov.si/met/en/service/"
reader = HtmlDataCollection(url)
links_for_data = reader.fetch_data()
city_data = reader.fetch_city_data(links_for_data[0])
