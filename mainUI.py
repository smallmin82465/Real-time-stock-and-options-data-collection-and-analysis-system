import sys
from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
from get_stock_GUI import StockGetGUI
from queryGUI import OptionStockGUI
from SQL_GUI_query import SQLQueryApp
from plotUI import StockAnalysisApp
from dataprocessGUI import DataProcessGUI
import os
import locale
import win32gui
import win32con

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.translator = QTranslator()
        # Get the system language
        system_language, _ = locale.getdefaultlocale()
        if system_language.startswith("zh"):
            self.load_translation(os.path.join(os.path.dirname(__file__), "translations", "app_zh.qm"))
        else:
            self.load_translation(os.path.join(os.path.dirname(__file__), "translations", "app_en_US.qm"))
        
        self.setWindowTitle(self.tr("Main UI"))
        self.setGeometry(100, 100, 400, 200)
        self.stock_app = None
        self.option_app = None
        self.data_process_app = None
        self.query_app = None
        self.plot_app = None
        self.init_ui()

    def init_ui(self):
        open_stock_search = QPushButton(self.tr("Stock Data Collection"), self)
        open_stock_search.clicked.connect(self.open_stock_gui)
        open_option_search = QPushButton(self.tr("Option Data Collection"), self)
        open_option_search.clicked.connect(self.open_option_gui)
        open_data_process = QPushButton(self.tr("Open Data Processing"), self)
        open_data_process.clicked.connect(self.open_dataprocess)
        open_query_button = QPushButton(self.tr("Open Data Verification"), self)
        open_query_button.clicked.connect(self.open_query_interface)
        open_plot_button = QPushButton(self.tr("Open Plotting Program"), self)
        open_plot_button.clicked.connect(self.open_plot_interface)
        
        layout = QVBoxLayout()
        layout.addWidget(open_stock_search)
        layout.addWidget(open_option_search)
        layout.addWidget(open_data_process)
        layout.addWidget(open_query_button)
        layout.addWidget(open_plot_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_translation(self, translation_file):
        if self.translator.load(translation_file):
            QApplication.instance().installTranslator(self.translator)

    def open_stock_gui(self):
        if not self.stock_app:
            self.stock_app = StockGetGUI()
        self.stock_app.show()

    def open_option_gui(self):
        if not self.option_app:
            self.option_app = OptionStockGUI()
            self.option_app.query_completed.connect(self.handle_option_query_completed)
        self.option_app.show()

    def open_dataprocess(self):
        if not self.data_process_app:
            self.data_process_app = DataProcessGUI()
        self.data_process_app.show()

    def open_query_interface(self):
        if not self.query_app:
            self.query_app = SQLQueryApp()
        self.query_app.show()

    def open_plot_interface(self):
        if not self.plot_app:
            self.plot_app = StockAnalysisApp()
        self.plot_app.show()

    def handle_option_query_completed(self):
        if self.option_app:
            QMessageBox.information(self, self.tr('Data Collection Completed'), self.tr('Data collection has been completed.'), QMessageBox.Ok)
            self.option_app.progress_dialog.cancel()

def main():
    
    app = QApplication(sys.argv)
    main_ui = MainUI()

    # Style
    app.setStyle('Fusion')
    
    # Global font
    font = app.font()
    font.setPointSize(12)
    
    app.setFont(font)
    main_ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    main()