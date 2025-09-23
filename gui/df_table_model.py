import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from data_collection.html_data_collection import HtmlDataCollection

class DataFrameModel(QtCore.QAbstractTableModel):
    def __init__(self, df):
        super().__init__()
        self._df = df

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._df.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._df.shape[0]

    def columnCount(self, index):
        return self._df.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._df.columns[section])

        if orientation == Qt.Vertical:
            return str(self._df.index[section])

    def set_df(self, df):
        self.beginResetModel()
        self._df = df
        self.endResetModel()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.table = QtWidgets.QTableView()
        self.model = DataFrameModel(data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)


app = QtWidgets.QApplication(sys.argv)
reader = HtmlDataCollection()
data_all = reader.combine_all_data()
window = MainWindow(data_all)
window.show()
app.exec_()
