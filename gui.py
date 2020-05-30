from PyQt5 import QtCore, QtGui, QtWidgets
from work import GetTagPosition
import pandas as pd
import sys

class Widget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)

        self.setWindowTitle("Etsy")
        self.resize(1000, 600)

        central_widget = QtWidgets.QWidget(self)                  
        self.setCentralWidget(central_widget)

        self.gLayout = QtWidgets.QGridLayout()
        central_widget.setLayout(self.gLayout)

        self.labelText = QtWidgets.QLabel(self)
        self.labelText.setText('<font size=5> Input url: </font>')
        self.gLayout.addWidget(self.labelText, 0, 0)

        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.move(20, 30)
        self.textEdit.resize(1160, 30)
        font = QtGui.QFont("Times", 14)
        self.textEdit.setFont(font)
        self.gLayout.addWidget(self.textEdit, 1, 0, 2, 0)

       
        buttonClear = QtWidgets.QPushButton(self)
        buttonClear.setText("Clear")
        buttonClear.clicked.connect(self.textEdit.clear)
        self.gLayout.addWidget(buttonClear,4,4)

        self.buttonFind = QtWidgets.QPushButton(self)
        
        self.buttonFind.setText("Find")
        self.gLayout.addWidget(self.buttonFind, 4,5)

        self.pandasTv = QtWidgets.QTableView(self)

        self.gLayout.addWidget(self.pandasTv, 5, 0, 6, 0)
        
        self.buttonFind.clicked.connect(self.loadFile)
        self.pandasTv.setSortingEnabled(True)

    def loadFile(self):
        print(self.textEdit.toPlainText())
        text = self.textEdit.toPlainText()

        with open("file.csv", 'w') as f:
            pass
            
        try:
            GetTagPosition(text)
        except Exception as e:
            print(e)
        df = pd.read_csv("file.csv", names=[
                    "Tag", 
                    "Title",
                    "Position",
                    "Page",
                    "Total_page"
                     ])
        print("==================================================")
        model = PandasModel(df)
        
        self.pandasTv.setModel(model)
        
        header = self.pandasTv.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)

class PandasModel(QtCore.QAbstractTableModel): 
    def __init__(self, df = pd.DataFrame(), parent=None): 
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df
        self.rows_nr, self.columns_nr = df.shape
        self.hheaders = ["Head-{}".format(i) for i in range(self.columns_nr)]
        self.vheaders = ["Row-{}".format(i) for i in range(self.rows_nr)]
        
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
                # return ["Начальная форма глагола", "\n1 и 2 форма наст.вр.", "\n3 форма", "\nокончание -ing","прошедш. время окончание -ed \nили 2-3 форма неправильн. глагола","Характеристика найденого глагола"][section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]

        if role == QtCore.Qt.EditRole:
            # interprete values
            self.table_data[row,col] = str(value)

        return True

    def flags(self, index):
        r_ = index.row()
        c_ = index.column()

        return QtCore.Qt.ItemIsEnabled

    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.columns)


if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())