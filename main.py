import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QTableWidgetItem, QWidget, QAbstractItemView


class AddEditCoffee(QWidget):
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
        self.pushButton_3.clicked.connect(self.note_2)
        self.que = ''
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
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tableWidget.resizeColumnsToContents()

    def note(self):
        self.extra = AddEditCoffee()
        self.extra.show()
        self.extra.buttonBox.accepted.connect(self.add)
        self.extra.buttonBox.rejected.connect(self.extra.close)

    def add(self):
        e = AddEditCoffee()
        title, taste = e.lineEdit.text(), e.lineEdit_2.text()
        roast, price, size = e.spinBox.value(), e.spinBox_2.value(), e.spinBox_3.value()
        tipe = e.comboBox.currentText()
        tipe = 0 if tipe == 'в зернах' else 1
        self.extra.close()
        cur = self.con.cursor()
        self.que = 'INSERT INTO sorts(sort, roast, tipe, taste, price, size )' \
              ' VALUES(?, ?, ?, ?, ?, ?)'
        cur.execute(self.que, (title, roast, tipe, taste, price, size))
        self.con.commit()
        self.load_table()

    def note_2(self):
        try:
            row = self.tableWidget.currentRow()
            self.extra = AddEditCoffee()
            e = self.extra
            e.show()
            self.extra.buttonBox.accepted.connect(self.edit)
            self.extra.buttonBox.rejected.connect(self.extra.close)
            wid = [e.lineEdit, e.spinBox, e.comboBox, e.lineEdit_2, e.spinBox_2, e.spinBox_3]
            for el in (1, 4):
                wid[el - 1].setText(self.tableWidget.item(row, el).text())
            for el in (2, 5, 6):
                wid[el - 1].setValue(int(self.tableWidget.item(row, el).text()))
            e.comboBox.setCurrentIndex(1 - int(self.tableWidget.item(row, 3).text()))
        except AttributeError:
            self.extra.close()
            self.statusBar().showMessage('не возможно провести изменения', 5000)



    def edit(self):
        e = self.extra
        title, taste = e.lineEdit.text(), e.lineEdit_2.text()
        roast, price, size = e.spinBox.value(), e.spinBox_2.value(), e.spinBox_3.value()
        tipe = e.comboBox.currentText()
        row = self.tableWidget.currentRow()
        id = self.tableWidget.item(row, 0).text()
        tipe = 0 if tipe == 'в зернах' else 1
        self.extra.close()
        cur = self.con.cursor()
        que = """UPDATE sorts
        SET sort = ?, roast = ?, tipe = ?, taste = ?, price = ?, size = ?
        WHERE ID = ?"""
        cur.execute(que, (title, roast, tipe, taste, price, size, int(id)))
        self.con.commit()
        self.load_table()

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
