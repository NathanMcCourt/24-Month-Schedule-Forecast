import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QDialog,
    QCalendarWidget,
    QDesktopWidget,
    QLineEdit,
    QComboBox,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap  # Make sure this line is included
import calendar
from datetime import datetime


class MonthCalendar(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("24 Month Block Calendar")
        self.setupUI()
        self.resize_to_95_percent()

    def setupUI(self):
        layout = QVBoxLayout()

        # Set background color for the main widget
        self.setStyleSheet("background-color: #3b718c;")  # Light gray background

        # Title label with elegant font
        title_label = QLabel("24 Month Schedule Forecast", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; font-family: 'Iowan Old Style';")
        layout.addWidget(title_label)

        # Grid for 24 months
        grid = QGridLayout()
        grid.setSpacing(10)  # Tighter spacing between buttons

        # Get current month and year
        today = datetime.today()
        current_month = today.month
        current_year = today.year

        # Add buttons for months (current month + 23 following months)
        row = 0
        col = 0
        for i in range(24):
            month_index = (current_month - 1 + i) % 12  # Index from 0-11
            year_offset = (current_month - 1 + i) // 12  # Increment year when going over December
            month = calendar.month_name[month_index + 1]  # Month names are 1-indexed

            btn = QPushButton(f"{month} {current_year + year_offset}", self)
            # Button styling for smaller size and rounded corners with elegant font
            btn.setStyleSheet(""" 
                QPushButton {
                    background-color: #89d5fa; 
                    color: white; 
                    padding: 10px; 
                    font-size: 24px; 
                    font-weight: bold;
                    font-family: 'Georgia';  /* Changed font */
                    border-radius: 5px;
                    min-width: 120px;
                    min-height: 60px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            btn.clicked.connect(lambda _, y=current_year + year_offset, m=month_index + 1: self.openCalendar(y, m))  # Pass month as integer
            grid.addWidget(btn, row, col)

            col += 1
            if col > 3:  # 4 columns of months
                col = 0
                row += 1

        # Add the grid to the layout
        layout.addLayout(grid)

        # Stretch to keep grid on upper half
        layout.addStretch(1)
        
        # Load and add image in the lower left corner
        self.image_label = QLabel(self)
        pixmap = QPixmap('C:/Users/natha/OneDrive/Documents/24-Month-Schedule-Forecast/src/pics/linecom_logo_2.png')  # Load the image (ensure the path is correct)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)  # Align to bottom-left corner
        layout.addWidget(self.image_label, alignment=Qt.AlignBottom | Qt.AlignLeft)

        
        self.setLayout(layout)

    def resize_to_95_percent(self):
        # Get the screen size
        screen = QDesktopWidget().screenGeometry()

        # Calculate 95% of the screen size
        width = int(screen.width() * 0.95)
        height = int(screen.height() * 0.95)

        # Set the window size to 95% of the screen
        self.setGeometry(
            (screen.width() - width) // 2,  # Center horizontally
            (screen.height() - height) // 2,  # Center vertically
            width,
            height
        )

    def openCalendar(self, year, month):
        # Create a new dialog to show the calendar
        cal_dialog = CalendarDialog(year, month, self)
        cal_dialog.exec_()

class CalendarDialog(QDialog):
    def __init__(self, year, month, parent=None):
        super().__init__(parent)

        self.setWindowTitle(f"{calendar.month_name[month]} {year}")
        self.setGeometry(100, 100, 600, 600)  # Adjusted size
        self.setupUI(year, month)

    def setupUI(self, year, month):
        layout = QVBoxLayout()

        # Set background color for the dialog
        self.setStyleSheet("background-color: #ffffff;")  # White background for the dialog

        # Top layout for month and year selection
        top_layout = QHBoxLayout()

        # Month selection combo box
        self.month_combo = QComboBox(self)
        self.month_combo.addItems(calendar.month_name[1:])  # Month names
        self.month_combo.setCurrentIndex(month - 1)  # Set the current month
        top_layout.addWidget(self.month_combo)

        # Year selection combo box
        self.year_combo = QComboBox(self)
        self.year_combo.addItems([str(year + i) for i in range(-1, 3)])  # Current year and next 2
        self.year_combo.setCurrentText(str(year))  # Set the current year
        top_layout.addWidget(self.year_combo)

        # Button to update the calendar
        update_btn = QPushButton("Update", self)
        update_btn.clicked.connect(lambda: self.updateCalendar())
        top_layout.addWidget(update_btn)

        layout.addLayout(top_layout)

        # Calendar widget
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.setStyleSheet("font-size: 14px; font-family: 'Georgia';")  # Changed font

        # Set the calendar to the selected year and month
        self.cal.setSelectedDate(datetime(year, month, 1))

        # Connect the date clicked signal to the method to add an event
        self.cal.clicked.connect(lambda date: self.addEvent(date))

        # Connect currentPageChanged signal to update the window title and drop-down menus
        self.cal.currentPageChanged.connect(lambda y, m: self.updateTitle(y, m))
        
        layout.addWidget(self.cal)

        # Close button
        close_btn = QPushButton("Close", self)
        close_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px; font-size: 14px; font-family: 'Georgia';")  # Changed font
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def updateTitle(self, year, month):
        # Update the dialog title to reflect the current month and year
        self.setWindowTitle(f"{calendar.month_name[month]} {year}")

        # Update the drop-down menus to reflect the current month and year
        self.month_combo.setCurrentIndex(month - 1)
        self.year_combo.setCurrentText(str(year))

    def updateCalendar(self):
        # Get selected month and year
        month = self.month_combo.currentIndex() + 1
        year = int(self.year_combo.currentText())

        # Update the calendar display
        self.cal.setCurrentPage(year, month)
        self.cal.setSelectedDate(datetime(year, month, 1))

        # Update the dialog title and drop-down menus to reflect the new month and year
        self.updateTitle(year, month)

    def addEvent(self, date):
        # Create a new dialog for adding an event
        event_dialog = EventDialog(date, self)
        event_dialog.exec_()

class EventDialog(QDialog):
    def __init__(self, date, parent=None):
        super().__init__(parent)
        self.date = date  # The selected date for the event
        self.setWindowTitle("Add Event")
        
        # Set a fixed size for the dialog
        self.setFixedSize(400, 300)  # Width, Height in pixels
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()

        # Display the selected date
        date_label = QLabel(f"Event Date: {self.date.toString(Qt.ISODate)}", self)
        layout.addWidget(date_label)

        # Input for event description
        self.event_description_input = QLineEdit(self)
        self.event_description_input.setPlaceholderText("Event Description")
        layout.addWidget(self.event_description_input)

        # Input for event time
        time_layout = QVBoxLayout()

        self.event_time_input = QLineEdit(self)
        self.event_time_input.setPlaceholderText("Event Time (HH:MM)")
        time_layout.addWidget(self.event_time_input)

        # AM/PM selection
        self.am_pm_combo = QComboBox(self)
        self.am_pm_combo.addItems(["AM", "PM"])
        time_layout.addWidget(self.am_pm_combo)

        layout.addLayout(time_layout)

        # Add button to save the event
        save_btn = QPushButton("Save Event", self)
        save_btn.clicked.connect(self.saveEvent)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def saveEvent(self):
        # Logic to save the event (not implemented yet)
        # You can implement storage logic here.
        event_description = self.event_description_input.text()
        event_time = self.event_time_input.text() + " " + self.am_pm_combo.currentText()  # Combine time and AM/PM
        # For now, just print the event details
        print(f"Event Saved: {self.date.toString(Qt.ISODate)} - Description: {event_description}, Time: {event_time}")
        self.close()  # Close the dialog after saving

def main():
    app = QApplication(sys.argv)
    main_window = MonthCalendar()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
