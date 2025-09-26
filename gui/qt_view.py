import pandas as pd
from base.base_classes import IGUI
from gui.df_table_model import DataFrameModel
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QTableView, QApplication

''' Class for presenting the GUI for viewing the data (model)
'''


class GUI(IGUI):
    def __init__(self):
        # Application has to be created before widget otherwise it won't run
        self.app = QApplication([])
        self.widget = QWidget()
        self.widget.setWindowTitle("Weather forecast")
        self.widget.resize(500, 500)

        # Setting the widgets and layout
        button = QPushButton("Refresh data")
        self.btn = button
        self.table = QTableView()
        self.model = DataFrameModel(pd.DataFrame())
        self.table.setModel(self.model)

        layout = QVBoxLayout(self.widget)
        layout.addWidget(self.btn)
        layout.addWidget(self.table)

        # handler that is later being set by the Controller
        self.refresh_handle = None
        self.btn.clicked.connect(self.handle_data_refresh)

    ''' Function for binding the refresh handler that was given by the Controller. 
        
        The function stores a reference to a handler (function) that should be 
        called whenever the user requests the refresh of data (by clicking
        the "Refresh data" button). Triggering the handler is done in the 
        handle_data_refresh() function.
        
        :param handler: function to invoke when refresh is triggered (callable)
    '''

    def refresh_data(self, handler):
        self.refresh_handle = handler

    ''' Function for updating the table view with new data.
        This function receives a DataFrame from the Controller 
        and forwards it to the DataFrameModel, which updates
        the QTableView.
        
        :param data: DataFrame with the weather data
    '''

    def show_data(self, data: pd.DataFrame):
        self.model.set_df(data)

    ''' Function for running the Qt application.
        The function shows the main widget and enters the Qt event
        loop, keeping the GUI responsive until the application is closed.
        The function is called once when starting the main program.
    '''

    def run_app(self):
        self.widget.show()
        self.app.exec_()

    ''' Function for refreshing the handler when the user requests data refresh.
        The function is connected to the "Refresh data" button in the GUI.
        If a refresh handler has been bound via refresh_data(), it is
        invoked here to fetch and display new data.
    '''
    def handle_data_refresh(self):
        if self.refresh_handle:
            self.refresh_handle()
