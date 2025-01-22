from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt
import jdatetime
import json
from PyQt5.QtGui import QFont


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("calendar.ui", self)

        # Widgets
        self.prevMonthButton = self.findChild(QtWidgets.QPushButton, "prevMonthButton")
        self.nextMonthButton = self.findChild(QtWidgets.QPushButton, "nextMonthButton")
        self.monthYearLabel = self.findChild(QtWidgets.QLabel, "monthYearLabel")
        self.calendarTable = self.findChild(QtWidgets.QTableWidget, "calendarTable")
        self.tabWidget = self.findChild(QtWidgets.QTabWidget, "tabWidget")


        self.shamsiLabel = QtWidgets.QLabel("Shamsi Date: ", self.tabWidget)
        self.gregorianLabel = QtWidgets.QLabel("Gregorian Date: ", self.tabWidget)
        self.dayOfWeekLabel = QtWidgets.QLabel("Day of Week: ", self.tabWidget)
        layout = QtWidgets.QVBoxLayout(self.tabWidget.widget(0))
        layout_2 = QtWidgets.QVBoxLayout(self.tabWidget.widget(1))
        layout.addWidget(self.shamsiLabel)
        layout.addWidget(self.gregorianLabel)
        layout.addWidget(self.dayOfWeekLabel)
        layout_2.addWidget (self.label)




        self.prevMonthButton.clicked.connect(self.show_prev_month)
        self.nextMonthButton.clicked.connect(self.show_next_month)

        self.current_date = jdatetime.date.today()
        self.update_calendar()
        self.events = self.load_events(r"shamsi.json")
    def load_events(self, filename):
            try:
                with open (filename, "r", encoding="utf-8") as file:
                    return json.load(file)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load events: {e}")
                return {}

    def update_calendar( self ):
            shamsi_month_year = f"{self.current_date.strftime ( '%B' )} {self.current_date.year}"
            gregorian_date = self.current_date.togregorian ()
            gregorian_month_year = f"{gregorian_date.strftime ( '%b' )} {gregorian_date.year}"
            self.monthYearLabel.setText(f"{shamsi_month_year} / {gregorian_month_year}" )


            self.calendarTable.setHorizontalHeaderLabels (
                ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"] )
            self.calendarTable.horizontalHeader().setStyleSheet("QHeaderView::section {color:green;}")

            first_day_of_month = self.current_date.replace (day=1)
            next_month = self.current_date.month % 12 + 1
            next_month_year = self.current_date.year + (self.current_date.month // 12)

            first_day_of_next_month = (
                self.current_date.replace(month=next_month, day=1)
                if next_month != 1
                else jdatetime.date(next_month_year, 1, 1)
            )
            days_in_month = (first_day_of_next_month - jdatetime.timedelta(days=1)).day

            start_day_of_week = first_day_of_month.weekday ()


            self.calendarTable.clearContents ()
            self.calendarTable.setRowCount (6)
            self.calendarTable.setColumnCount (7)

            row, col = 0, start_day_of_week
            for day in range (1, days_in_month + 1):
                shamsi_date = jdatetime.date(self.current_date.year, self.current_date.month, day)
                gregorian_date = shamsi_date.togregorian()




                cell_widget = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout (cell_widget )
                layout.setAlignment(Qt.AlignCenter)
                layout.setContentsMargins( 0 , 0 , 0 , 0 )

                shamsi_label = QtWidgets.QLabel (str(day))
                shamsi_label.setAlignment(Qt.AlignCenter )
                shamsi_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))

                gregorian_label = QtWidgets.QLabel(str(gregorian_date.day))
                gregorian_label.setAlignment(Qt.AlignCenter)
                gregorian_label.setFont(QFont("", 8))
                gregorian_label.setStyleSheet("color: blue;")

                layout.addWidget(shamsi_label)
                layout.addWidget(gregorian_label)
                cell_widget.setLayout(layout)

                self.calendarTable.setCellWidget(row, col, cell_widget)
                self.calendarTable.cellClicked.connect(self.handle_date_selection)

                col += 1
                if col > 6:
                    col = 0
                    row += 1



    def handle_date_selection(self, row, col):

        cell_widget = self.calendarTable.cellWidget(row, col)
        if not cell_widget:
            QtWidgets.QMessageBox.warning ( self, "لطفا تاریخ انتخاب کنید" )
            return


        shamsi_label = cell_widget.layout ().itemAt ( 0 ).widget()
        gregorian_label = cell_widget.layout ().itemAt(1).widget()
        if not shamsi_label or not gregorian_label:
            QtWidgets.QMessageBox.warning ( self , "برچسب تاریخ پیدا نشد" )
            return


        selected_day = int (shamsi_label.text())
        shamsi_date = jdatetime.date(self.current_date.year, self.current_date.month, selected_day)


        gregorian_date = shamsi_date.togregorian ()

        days_of_week = ["شنبه" , "یکشنبه" , "دوشنبه" , "سه‌شنبه" , "چهارشنبه" , "پنج‌شنبه" , "جمعه"]
        day_of_week = days_of_week[shamsi_date.weekday ()]


        self.shamsiLabel.setText ( f"Shamsi Date: {shamsi_date.strftime ( '%d %B %Y' )}" )
        self.gregorianLabel.setText ( f"Gregorian Date: {gregorian_date.strftime ( '%d %B %Y' )}")
        self.dayOfWeekLabel.setText(f"Day of Week: {day_of_week}")
        Font = QFont("Perpetua", 14)
        self.shamsiLabel.setFont(Font)
        self.gregorianLabel.setFont(Font)
        self.dayOfWeekLabel.setFont(Font)
        self.shamsiLabel.move(50,100)
        self.gregorianLabel.move(20,50)


        gregorian_key = shamsi_date.strftime ( '%Y-%m-%d' )
        if gregorian_key in self.events:
            self.label.setText ( self.events[gregorian_key] )
        else:
            self.label.setText ( "رویدادی وجود ندارد." )

    def show_prev_month( self ):
        if self.current_date.month == 1:
            self.current_date = jdatetime.date ( self.current_date.year - 1 , 12 , 1 )
        else:
            self.current_date = self.current_date.replace ( month=self.current_date.month - 1 , day=1 )
        self.update_calendar ()

    def show_next_month( self ):
        if self.current_date.month == 12:
            self.current_date = jdatetime.date ( self.current_date.year + 1 , 1 , 1 )
        else:
            self.current_date = self.current_date.replace ( month=self.current_date.month + 1 , day=1 )
        self.update_calendar ()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
