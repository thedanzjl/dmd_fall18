import sys
from interface import *
from PyQt5 import Qt
from PyQt5 import uic


class DbApp(Qt.QMainWindow):

    db = Database('db.sqlite')

    def __init__(self, name):
        super().__init__()
        self.setWindowTitle(name)
        self.init_ui()

    def init_ui(self):
        self.resize(700, 900)
        uic.loadUi('db.ui', self)
        names = self.db.get_tables_names()
        self.table_name.addItems(names)
        self.display_table(names[0])
        self.table_name.currentTextChanged.connect(self.display_table)
        self.query_field.returnPressed.connect(self.query_result)

    def display_table(self, text):
        columns = self.db.get_table_info(text)
        columns = list(map(lambda x: x[1], columns))
        values = self.db.query('''SELECT * FROM {}'''.format(text))
        self.tableWidget.setRowCount(len(values))
        self.tableWidget.setColumnCount(len(columns))

        for i, row in enumerate(values):
            for j, col in enumerate(row):
                self.tableWidget.setItem(i, j, Qt.QTableWidgetItem(str(values[i][j])))

        self.tableWidget.setHorizontalHeaderLabels(columns)

    def query_result(self):
        query = self.query_field.text()
        try:
            values = self.db.query(query)
        except Exception as e:
            Qt.QMessageBox.critical(self, 'query error', "can't parse such query")
            return
        self.tableWidget.setRowCount(len(values))
        self.tableWidget.setColumnCount(len(values[0]))
        table = [word for i, word in enumerate(query.split()) if i > 0 and query.split()[i - 1] == 'from'][0]  # parse
        # query and find the name of the table
        columns = self.db.get_table_info(table)
        columns = list(map(lambda x: x[1], columns))

        for i, row in enumerate(values):
            for j, col in enumerate(row):
                self.tableWidget.setItem(i, j, Qt.QTableWidgetItem(str(values[i][j])))

        self.tableWidget.setHorizontalHeaderLabels(columns)


if __name__ == '__main__':
    # run program
    app = Qt.QApplication([])
    mw = DbApp('DbApp')
    mw.show()
    sys.exit(app.exec_())
