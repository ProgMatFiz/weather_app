from abc import ABC, abstractmethod


class IWeatherSource(ABC):
    @abstractmethod
    def fetch_data(self):
        pass

    @abstractmethod
    def fetch_city_data(self, url):
        pass

    @abstractmethod
    def combine_all_data(self):
        pass
