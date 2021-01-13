import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication,\
    QTableWidgetItem


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.db')
        self.pushButton.clicked.connect(self.load_table)
        self.load_table()

    def load_table(self):
        res = self.con.cursor().execute('select * from sorts').fetchall()
        self.tableWidget.setColumnCount(7)
        titles = [d[0] for d in self.con.execute('select * from sorts').description]
        self.tableWidget.setHorizontalHeaderLabels(titles)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.con.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())