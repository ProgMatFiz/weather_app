import requests
import pandas as pd
from lxml import html
from urllib.parse import urljoin
from base.base_classes import IWeatherSource

base_url = "https://meteo.arso.gov.si/met/en/service2/"
table_url = "observation_si/index.html"
city_data_url = "history.html"

"""
Class for collecting, formatting and combining all weather data from HTML links
"""


class HtmlDataCollection(IWeatherSource):
    def __init__(self, url: str = base_url):
        self.url = url

    @property
    def fetch_data(self) -> list[str]:

        """ Function fetch_data fetches the data from a given URL.
            The function finds first the link to the page of table
            with the data of the weather for all the cities.
            Then from this, the function finds the separate links
            for each city with the weather data in the last 48h and
            saves them in a list.

            :return full_data_links: list of links of weather data in the last 48 by each city
        """

        try:
            # Finding the main link to the table from the given page
            r_main_link = requests.get(self.url, timeout=20)
            if r_main_link.raise_for_status() is None:
                list_of_links = html.fromstring(r_main_link.content)
                link = list_of_links.xpath(f"//a[contains(@href,'{table_url}')]/@href")[0]
                full_data_url = urljoin(self.url, link)

                # Finding all the links of data from the table in HTML form
                r_data = requests.get(full_data_url, timeout=20)
                list_data_links = html.fromstring(r_data.content)
                data_links = list_data_links.xpath(f"//a[contains(@href, '{city_data_url}')]/@href")
                full_data_links = []
                for i in data_links:
                    full_data_links.append(urljoin(self.url, i))
                return full_data_links

        except requests.exceptions.HTTPError as error:
            print("An HTTP error occurred: ", error)

    def fetch_city_data(self, url: str):

        """ Function that creates a DataFrame for a city from a provided url (HTML link).
            The function goes through the HTML and saves data by row.
            Since the wind and cloud cover columns are presented with mini icons and not text,
            the function has to iterate through the HTML file in order to save
            these parameters in text form (looking at rows of <img src).
            The function additionally processes and returns the processed DataFrame
            with columns where temperature, wind and pressure are present.

            :param url: city URL (HTML link)
            :return df_city_data: DataFrame with columns containing wind, temperature and pressure
        """

        # Saving column names
        df = pd.read_html(url)[0]
        column_names = df.columns.values

        try:
            # Extracting data from URL and creating a DataFrame
            r_city_data = requests.get(url, timeout=20)
            if r_city_data.raise_for_status() is None:
                city_data = html.fromstring(r_city_data.content)
                rows = []

                # Going through the td content
                for tr in city_data.xpath("//table//tr[td]"):
                    tds = tr.xpath("./td")
                    if not tds:
                        continue
                    row = []
                    for td in tds:
                        img = td.xpath(".//img/@src")
                        if img:
                            # Extracting wind data (lightSE, modSW for example)
                            val = img[0].split("/")[-1].replace(".png", "")
                        else:
                            val = td.text_content().strip()
                        row.append(val)
                    rows.append(row)

                df = pd.DataFrame(rows, columns=column_names)
                candidate = self.column_candidates(df)
                df_city_data = df[candidate]
                return df_city_data
        except requests.exceptions.HTTPError as error:
            print("An HTTP error occurred: ", error)

    def combine_all_data(self):

        """ Function that creates a joint DataFrame for all weather data from every city.
            The function iterates through the list of links of weather data for each city,
            and it adds an extra column for city names. The final DataFrame is created by
            merging separate weather DataFrames of every city.

            :return df_all_data: DataFrame with columns containing wind, temperature and pressure
        """
        # Fetching city data links
        city_data_links = self.fetch_data
        df = []
        df_all = []
        for i in city_data_links:
            df = self.fetch_city_data(i)
            city_name = df.columns.values[0]
            df.insert(1, "City", city_name)
            df.rename(columns={f"{city_name}": "Date and time"}, inplace=True)
            df_all.append(df)
        # Forming full data frame
        df_all_data = pd.concat(df_all, ignore_index=True)
        df_all_data.replace(r'^\s*$', "No data provided", regex=True, inplace=True)
        df_all_data["Wind"] = df_all_data["Wind"].str.replace(r'(?<=[a-z])(?=[A-Z])', ' ', regex=True)
        return df_all_data

    @staticmethod
    def column_candidates(df: pd.DataFrame) -> list:

        """ Function that returns column candidates of a DataFrame for presenting
            weather data in the last 48 hours. The function accepts
            the DataFrame as a parameter.

            :param df: DataFrame
            :return column_list: list of column candidates for presenting weather data
       """
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
