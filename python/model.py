from PySide2 import QtGui, QtCore, QtWidgets


class TextureModel(QtCore.QAbstractTableModel):
    """ Class to hold the model of the Table

    In this table we show two columns of [node, location] the location column
    cells are highlighted red if the location is not found and green if the
    location is found and applied.

    """
    data_changed = QtCore.Signal(QtCore.QModelIndex, QtCore.QModelIndex)

    def __init__(self, texture_data=None):
        """ Sets up the initial texture data

        :param texture_data:
        """
        super(TextureModel, self).__init__()
        self._original_textures = texture_data or []
        self._texture_data = [row[:] for row in self._original_textures]
        self.headers = ["Node", "Location"]

    def rowCount(self, index):
        return len(self._texture_data)

    def columnCount(self, index):
        return len(self.headers)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """ Sets various attributes to do with the individual data

        Currently, sets the data in each cell.
        Sets the text color to black.
        Sets the background color of each cell in the last column to red if
        unchanged and green if changed.

        """
        if role == QtCore.Qt.DisplayRole:
            return self._texture_data[index.row()][index.column()]

        if role == QtCore.Qt.ForegroundRole and index.column() == 1:
            return QtGui.QBrush(QtCore.Qt.black)

        if role == QtCore.Qt.BackgroundRole and index.column() == 1:
            original = self._original_textures[index.row()][index.column()]
            current = self._texture_data[index.row()][index.column()]
            if current != original:
                return QtGui.QBrush(QtCore.Qt.green)
            return QtGui.QBrush(QtCore.Qt.red)
        return None

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if (role == QtCore.Qt.DisplayRole and
                orientation == QtCore.Qt.Horizontal):
            return self.headers[section]

        return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole and index.column() == 1:
            if self._texture_data[index.row()][index.column()] != value:
                self._texture_data[index.row()][index.column()] = value
                self.dataChanged.emit(index, index)
                return True
        return False

    def set_all_data(self, new_data):
        """ Sets a new list of lists as the data for the model

        :param new_data: New list of data to use
        """
        self._texture_data = new_data
        top_left = self.index(0, 0)
        bottom_right = self.index(self.rowCount(0) - 1, self.columnCount(0) - 1)
        self.dataChanged.emit(top_left, bottom_right)
