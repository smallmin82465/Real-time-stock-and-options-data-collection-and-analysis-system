import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QFileDialog, QProgressBar, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread
from Stock_get import get_stock_price
from datetime import date, datetime
import yfinance as yf

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, symbols, folder_path, data_interval, data_period):
        super().__init__()

        self.symbols = symbols
        self.folder_path = folder_path
        self.data_interval = data_interval
        self.data_period = data_period

    def run_query(self):
        try:
            get_stock_price(self.symbols, self.folder_path, self.data_interval, self.data_period, self.update_progress)
            self.finished.emit()  # Signal that the work is finished
        except Exception as e:
            self.error_message = str(e)
            self.finished.emit()  # Signal that the work is finished with an error

    def update_progress(self, progress):
        self.progress.emit(progress)  # Signal the progress

class StockGetGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.tickers = []
        self.init_ui()
    def init_ui(self):
        # Widgets
        background_label = QLabel(self)
        background_pixmap = QPixmap('GIO.jpg')  # Replace 'GIO.jpg' with the actual path to your image file
        background_label.setPixmap(background_pixmap)
        background_label.setGeometry(0, 0, background_pixmap.width(), background_pixmap.height())

        self.label = QLabel(self.tr('Enter Ticker:'))
        self.ticker_input = QLineEdit()
        
        self.add_button = QPushButton(self.tr('Add Ticker'))
        self.add_button.setStyleSheet("background-color: red; color: white;")  # Set red background and white text
        self.add_button.clicked.connect(self.add_ticker)

        self.clear_button = QPushButton(self.tr('Clear'))
        self.clear_button.setStyleSheet("background-color: black; color: white;")  # Set black background and white text
        self.clear_button.clicked.connect(self.clear_tickers)

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

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(10, 290, 480, 20)
        self.progress_bar.setValue(0)
        
        self.ticker_display = QLabel()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.ticker_input)
        
        # Add add_button and clear_button in a horizontal layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.clear_button)
        layout.addLayout(button_layout)
        
        layout.addWidget(self.ticker_display)
        layout.addWidget(self.choose_file_button)
        layout.addWidget(self.path_label)
        layout.addWidget(self.selected_path_display)
        layout.addWidget(self.interval_label)
        layout.addWidget(self.interval_combobox)
        layout.addWidget(self.period_label)
        layout.addWidget(self.period_combobox)
        layout.addWidget(self.query_button)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        # Window settings
        self.setWindowTitle(self.tr('Option Stock Data Query'))
        self.setGeometry(300, 300, 500, 300)

    def add_ticker(self):
        current_ticker = self.ticker_input.text()

        # Check if the ticker can be queried successfully
        if self.is_valid_ticker(current_ticker):
            self.tickers.append(current_ticker)
            self.ticker_display.setText(self.tr(f"Tickers added: {', '.join(self.tickers)}"))
            self.ticker_input.clear()  # Clear the input field
        else:
            self.show_message_box(self.tr("Invalid Ticker"), self.tr(f"The ticker {current_ticker} does not exist. Please enter a valid ticker."))
            self.ticker_input.clear()
            
    def clear_tickers(self):
        self.tickers.clear()  # Clear the tickers list
        self.ticker_display.setText(self.tr("Tickers added: "))  # Clear the ticker display

    def is_valid_ticker(self, ticker):
        try:
            # Attempt to get information for the ticker
            ticker_info = yf.Ticker(ticker).info
            # Check if the required key exists in the info dictionary
            if 'regularMarketOpen' in ticker_info:
                return True
            else:
                return False
        except Exception as e:
            return False

    def choose_file_location(self):
        folder_path = QFileDialog.getExistingDirectory(self, self.tr('Choose Folder'))
        self.selected_path_display.setText(folder_path)

    def update_period_combobox(self):
        current_interval = self.interval_combobox.currentText()
        if current_interval == "1m":
            self.period_combobox.clear()
            self.period_combobox.addItems(["1d", "2d", "3d", "4d", "5d", "6d", "7d"])
        elif current_interval == "1d":
            self.period_combobox.clear()
            self.period_combobox.addItems(["1d", "2d", "3d", "4d", "5d", "6d", "7d", "1mo", "3mo", "6mo", "1y", "max"])
        elif current_interval == "1mo":
            self.period_combobox.clear()
            self.period_combobox.addItems(["1mo", "3mo", "6mo", "1y", "max"])

    def query_data(self):
        folder_path = self.selected_path_display.text()
        data_interval = self.interval_combobox.currentText()
        data_period = self.period_combobox.currentText()

        self.worker = Worker(self.tickers, folder_path, data_interval, data_period)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)

        self.worker.finished.connect(self.query_completed)
        self.worker.progress.connect(self.update_progress_bar)

        self.worker_thread.started.connect(self.worker.run_query)
        self.worker_thread.start()
        
    def update_progress_bar(self, progress):
        self.progress_bar.setValue(progress)

    def query_completed(self):
        self.worker_thread.quit()
        self.worker_thread.wait()
        if hasattr(self.worker, 'error_message'):
            self.show_message_box(self.tr("Query Error"), self.tr(f"An error occurred during the query:\n\n{self.worker.error_message}"))
        else:
            self.show_message_box(self.tr("Query Success"), self.tr("Data query completed successfully"))

    def show_message_box(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StockGetGUI()
    window.show()
    sys.exit(app.exec_())