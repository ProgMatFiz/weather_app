import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QTableView, QMainWindow
from df_table_model import DataFrameModel
from data_collection.html_data_collection import HtmlDataCollection

'''Class for presenting the MainWindow for viewing the data (model)'''
class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.table = QTableView()
        self.model = DataFrameModel(data)
        self.table.setModel(self.model)

        button = QPushButton("Refresh data")
        self.btn = button

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(self.btn)
        layout.addWidget(self.table)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.btn.clicked.connect(self.refresh_data)

    def refresh_data(self):
        self.model.set_df(self.data)


app = QtWidgets.QApplication(sys.argv)
reader = HtmlDataCollection()
data_all = reader.combine_all_data()
window = MainWindow(data_all)
window.show()
app.exec_()
