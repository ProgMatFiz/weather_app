import pandas as pd
from base.base_classes import IGUI
from gui.df_table_model import DataFrameModel
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QTableView, QApplication

''' Class for presenting the MainWindow for viewing the data (model)
'''


class GUI(IGUI):
    def __init__(self):

        # Application has to be created before widget otherwise it won't run
        self.app = QApplication([])
        self.widget = QWidget()
        self.widget.setWindowTitle("Weather forecast")
        self.widget.resize(1000,1000)

        # Setting the widgets and layout
        button = QPushButton("Refresh data")
        self.btn = button
        self.table = QTableView()
        self.model = DataFrameModel(pd.DataFrame())
        self.table.setModel(self.model)

        layout = QVBoxLayout(self.widget)
        layout.addWidget(self.btn)
        layout.addWidget(self.table)

        self.refresh_handle = None
        self.btn.clicked.connect(self.handle_data_refresh)

    def refresh_data(self, handler):
        self.refresh_handle = handler

    def show_data(self, data: pd.DataFrame):
        self.model.set_df(data)

    def run_app(self):
        self.widget.show()
        self.app.exec_()

    def handle_data_refresh(self):
        if self.refresh_handle:
            self.refresh_handle()
