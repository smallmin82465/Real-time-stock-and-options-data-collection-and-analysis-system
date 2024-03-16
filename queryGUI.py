import sys
from style import apply_style  # Import the apply_style function

apply_style()  # Apply the chosen style
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressDialog, QFileDialog, QMessageBox, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from OptionStockGet_min import optionget_min
from threading import Thread
import io
import contextlib
import yfinance as yf

class OptionStockGUI(QWidget):
   query_completed = pyqtSignal()

   def __init__(self):
        super().__init__()

        self.ticker_list = []
        self.folder_path = None
        self.progress_dialog = None

        self.init_ui()

   def init_ui(self):
       # Widgets
       # Set the background image for the main window
       background_label = QLabel(self)
       background_pixmap = QPixmap('GIO.jpg')  # Replace 'GIO.jpg' with the actual path to your image file
       background_label.setPixmap(background_pixmap)
       background_label.setGeometry(0, 0, background_pixmap.width(), background_pixmap.height())
       self.label = QLabel(self.tr('Enter Ticker:'))
       self.ticker_input = QLineEdit()
       
       button_layout = QHBoxLayout()       
       self.add_button = QPushButton(self.tr('Add Ticker'))
       self.add_button.setStyleSheet("background-color: red; color: white;")  # Set red background and white text
       self.add_button.clicked.connect(self.add_ticker)
       button_layout.addWidget(self.add_button)

       self.clear_button = QPushButton(self.tr('Clear'))  # New clear button
       self.clear_button.setStyleSheet("background-color: black; color: white;")  # Set black background and white text
       self.clear_button.clicked.connect(self.clear_tickers)  # Connect the clear button to the clear_tickers method
       button_layout.addWidget(self.clear_button)
       
       self.choose_file_button = QPushButton(self.tr('Choose Folder Location'))
       self.choose_file_button.clicked.connect(self.choose_file_location)
       self.path_label = QLabel(self.tr('Selected Folder Path:'))
       self.selected_path_display = QLabel()
       self.interval_label = QLabel(self.tr('Interval:'))
       self.interval_combobox = QComboBox(self)
       self.interval_combobox.addItems(["1m", "1d", "1mo"])
       self.interval_combobox.currentTextChanged.connect(self.update_period_combobox)

       self.period_label = QLabel(self.tr('Period:'))
       self.period_combobox = QComboBox(self)
       self.period_combobox.addItems(["1d", "2d", "3d", "4d", "5d", "6d", "7d", "1mo", "3mo", "6mo", "1y", "max"])
       self.update_period_combobox()
       self.query_button = QPushButton(self.tr('Query Data'))
       self.query_button.clicked.connect(self.query_data)

       self.ticker_display = QLabel()
       # Layout
       layout = QVBoxLayout()
       layout.addWidget(self.label)
       layout.addWidget(self.ticker_input)
       layout.addLayout(button_layout)  # Add the button layout
       layout.addWidget(self.ticker_display)
       layout.addWidget(self.choose_file_button)
       layout.addWidget(self.path_label)
       layout.addWidget(self.selected_path_display)
       layout.addWidget(self.interval_label)
       layout.addWidget(self.interval_combobox)
       layout.addWidget(self.period_label)
       layout.addWidget(self.period_combobox)
       layout.addWidget(self.query_button)
       self.setLayout(layout)

       # Window settings
       self.setWindowTitle(self.tr('Option Stock Data Query'))
       self.setGeometry(300, 300, 300, 200)

   def update_period_combobox(self):
       current_interval = self.interval_combobox.currentText()
       available_periods = []

       if current_interval == "1m":
           available_periods = ["1d", "2d", "3d", "4d", "5d", "6d", "7d"]
       elif current_interval == "1d":
           available_periods = ["1d", "2d", "3d", "4d", "5d", "6d", "7d", "1mo", "3mo", "6mo", "1y", "max"]
       elif current_interval == "1mo":
           available_periods = ["1mo", "3mo", "6mo", "1y", "max"]
           
       self.period_combobox.clear()
       self.period_combobox.addItems(available_periods)

       
   def add_ticker(self):
       ticker = self.ticker_input.text().strip().upper()
       if ticker:
           if self.check_ticker_exist(ticker):
               self.ticker_list.append(ticker)
               self.ticker_input.clear()
               self.update_ticker_display()
           else:
               QMessageBox.warning(self, self.tr('Invalid Ticker'), self.tr(f'Ticker "{ticker}" does not exist or no data update now.'), QMessageBox.Ok)
   
   def clear_tickers(self):  # New method to clear the ticker list
       self.ticker_list = []
       self.ticker_input.clear()
       self.update_ticker_display()
       
   def choose_file_location(self):
       options = QFileDialog.Options()
       options |= QFileDialog.DontUseNativeDialog
       self.folder_path = QFileDialog.getExistingDirectory(self, self.tr("Choose Folder Location"), "", options=options)
       self.selected_path_display.setText(self.folder_path)
       
   def check_ticker_exist(self, ticker):
       try:
           options = yf.Ticker(ticker).options
           return bool(options)  # Returns True if options are available, False otherwise
       except Exception as e:
           print(self.tr(f"Error checking ticker existence: {e}"))
           return False

   def update_ticker_display(self):
       self.ticker_display.setText(self.tr(f'Added Tickers: {", ".join(self.ticker_list)}'))

   def query_data(self):
       if not self.folder_path:
           QMessageBox.warning(self, self.tr('Folder Location Not Chosen'), self.tr('Please choose a folder location before querying data.'), QMessageBox.Ok)
           return

       if self.ticker_list:
           self.progress_dialog = QProgressDialog(self.tr("Querying Data..."), self.tr("Cancel"), 0, 0, self)
           self.progress_dialog.setWindowModality(Qt.WindowModal)
           self.progress_dialog.canceled.connect(self.cancel_query)
           self.progress_dialog.show()

           interval = self.interval_combobox.currentText()
           period = self.period_combobox.currentText()

           def query_thread():
               with contextlib.redirect_stdout(io.StringIO()) as new_stdout:
                   optionget_min(symbols=self.ticker_list, folder_path=self.folder_path, progress_dialog=self.progress_dialog,
                                 DataInterval=interval, DataPeriod=period)

               self.query_completed.emit()

           thread = Thread(target=query_thread)
           thread.start()

   def cancel_query(self):
       if self.progress_dialog:
           self.progress_dialog.cancel()

   def handle_query_completed(self):
       if self.progress_dialog:
           self.progress_dialog.accept()
           
           QMessageBox.information(self, self.tr('Data Collection Completed'), self.tr('Data collection has been completed.'), QMessageBox.Ok)

       self.ticker_list = []
       self.update_ticker_display()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = OptionStockGUI()
   window.query_completed.connect(window.handle_query_completed)  # Connect the signal to the slot
   window.show()
   sys.exit(app.exec_())