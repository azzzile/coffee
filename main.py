import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication,\
    QTableWidgetItem, QDialog


class AddEditCoffee(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.pushButton.clicked.connect(self.load_table)
        self.pushButton_2.clicked.connect(self.note)
        self.pushButton_3.clicked.connect(self.edit)
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

    def add(self):
        pass

    def edit(self):
        pass

    def closeEvent(self, event):
        self.con.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Example()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())