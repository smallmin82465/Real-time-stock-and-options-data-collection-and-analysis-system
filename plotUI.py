from style import apply_style  # Import the apply_style function
apply_style()  # Apply the chosen style
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QComboBox, QVBoxLayout, QWidget, QMessageBox

class StockAnalysisApp(QMainWindow):
   def __init__(self):
       super().__init__()
       background_label = QLabel(self)
       background_pixmap = QPixmap('GIO.jpg')  # Replace 'GIO.jpg' with the actual path to your image file
       background_label.setPixmap(background_pixmap)
       background_label.setGeometry(0, 0, background_pixmap.width(), background_pixmap.height())
       self.setWindowTitle(self.tr("Stock analysis drawing application"))
       self.setGeometry(100, 100, 600, 400)

       self.central_widget = QWidget(self)
       self.setCentralWidget(self.central_widget)

       self.layout = QVBoxLayout()

       self.file_label = QLabel(self.tr("CSV File:"))
       self.layout.addWidget(self.file_label)

       self.file_button = QPushButton(self.tr("Select CSV file"), self)
       self.file_button.clicked.connect(self.load_csv)
       self.layout.addWidget(self.file_button)

       self.ticker_label = QLabel(self.tr("Select Ticker:"))
       self.layout.addWidget(self.ticker_label)

       self.ticker_combobox = QComboBox(self)
       self.ticker_combobox.currentIndexChanged.connect(self.update_symbols)
       self.layout.addWidget(self.ticker_combobox)

       self.symbol_label = QLabel(self.tr("Select Contract Symbol:"))
       self.layout.addWidget(self.symbol_label)

       self.symbol_combobox = QComboBox(self)
       self.layout.addWidget(self.symbol_combobox)

       self.plot_button = QPushButton(self.tr("Create plot"), self)
       self.plot_button.clicked.connect(self.plot_graph)
       self.layout.addWidget(self.plot_button)

       self.central_widget.setLayout(self.layout)

   def load_csv(self):
       file_dialog = QFileDialog()
       file_path, _ = file_dialog.getOpenFileName(self, self.tr("Open CSV File"), "", self.tr("CSV Files (*.csv)"))

       if file_path:
           try:
               self.file_label.setText(self.tr(f"CSV File: {file_path}"))
               self.df = pd.read_csv(file_path)

               required_columns = ['Ticker', 'contractSymbol', 'Datetime', 'Close', 'Black_Scholes_Value']
               missing_columns = [col for col in required_columns if col not in self.df.columns]

               if missing_columns:
                   raise ValueError(self.tr(f"The required fields are missing from the CSV file: {', '.join(missing_columns)}"))

               tickers = self.df['Ticker'].unique()
               self.ticker_combobox.addItems(tickers)

           except Exception as e:
               error_message = self.tr(f"An error occurred while loading the CSV file:\n{str(e)}")
               QMessageBox.critical(self, self.tr("Error"), error_message)
               return

   def update_symbols(self):
       selected_ticker = self.ticker_combobox.currentText()
       if selected_ticker:
           ticker_symbols = sorted(self.df.loc[self.df['Ticker'] == selected_ticker, 'contractSymbol'].unique())
           self.symbol_combobox.clear()
           self.symbol_combobox.addItems(ticker_symbols)

   def plot_graph(self):
       selected_symbol = self.symbol_combobox.currentText()
       if selected_symbol:
           contract_df = self.df[self.df['contractSymbol'] == selected_symbol]

           # Plotting the graph
           contract_df.set_index('Datetime', inplace=True)
           contract_df.plot(y=['Close', 'Black_Scholes_Value'], figsize=(10, 6))
           plt.grid(True)
           plt.show()


if __name__ == '__main__':
   app = QApplication([])
   window = StockAnalysisApp()
   window.show()
   app.exec_()