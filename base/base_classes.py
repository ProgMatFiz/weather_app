from abc import ABC, abstractmethod
import pandas as pd

''' Abstract class for the model (data)
'''


class IWeatherSource(ABC):
    @abstractmethod
    def fetch_data(self):
        pass

    @abstractmethod
    def fetch_city_data(self, url: str):
        pass

    @abstractmethod
    def combine_all_data(self):
        pass


''' Abstract class for the view (GUI)
'''


class IGUI(ABC):
    @abstractmethod
    def show_data(self, data: pd.DataFrame):
        pass

    @abstractmethod
    def refresh_data(self, reader):
        pass

    @abstractmethod
    def run_app(self):
        pass
