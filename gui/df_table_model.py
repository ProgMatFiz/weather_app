from PyQt5 import QtCore
from PyQt5.QtCore import Qt

''' Class for defining the data (model) to be presented for the GUI (viewer)
'''


class DataFrameModel(QtCore.QAbstractTableModel):
    def __init__(self, df):
        super().__init__()
        self._df = df

    ''' Function for presenting data for given locations in the table.
        This function is called by Qt views (in this case QTableView)
        whenever a cell is being drawn.
    
        :param index: specification of the cell (row,column)
        :param role: the role requested by the view
        :return value: string value to be displayed in the cell
    '''

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._df.iloc[index.row(), index.column()]
            return str(value)

    ''' Function for retrieving row count of the model.
        The function tells the Qt view how many rows should be drawn,
        which is the number of rows the DataFrame has.
        
        :param index: not used (required by Qt signature)
        :return: row count
    '''
    def rowCount(self, index):
        return self._df.shape[0]

    ''' Function for retrieving column count of the model.
        The function tells the Qt view how many columns should be drawn,
        which is the number of columns the DataFrame has.
    
        :param index: not used (required by Qt signature)
        :return: column count
    '''

    def columnCount(self, index):
        return self._df.shape[1]

    ''' Function that returns the header text for a given row or column.
        The function is called by Qt views to display labels for the horizontal
        and vertical headers.
    
        :param section: index of the column (for orientation that is horizontal) or row 
        (for orientation that is vertical)
        :param orientation: specifies whether the header is horizontal or vertical
        :param role: display role requested by the view
        
        :return: text for display in the header or None 
    '''

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._df.columns[section])

        if orientation == Qt.Vertical:
            return str(self._df.index[section])

    ''' Function that replaces the current DataFrame with a new one
        and refreshes the model.
        
        The function updates the internal DataFrame used by the model.
        Calling beginResetModel() and endResetModel() notify QTableView 
        that the data has been changed, so that the table display is
        refreshed.
        
        :param df: new DataFrame to be displayed in the table model
    '''

    def set_df(self, df):
        self.beginResetModel()
        self._df = df
        self.endResetModel()
