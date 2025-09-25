from base.base_classes import IGUI

'''Class that defines the controller (connects the model - data and view - GUI)
'''


class Controller:
    def __init__(self, view: IGUI, source):
        self.view = view
        self.source = source
        self.view.refresh_data(self.on_refresh)

    def on_refresh(self):
        df = self.source.combine_all_data()
        self.view.show_data(df)
