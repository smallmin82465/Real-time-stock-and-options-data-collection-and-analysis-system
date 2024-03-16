from style import apply_style  # Import the apply_style function
apply_style()  # Apply the chosen style
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QProgressDialog, QListWidget, QListWidgetItem, QHBoxLayout
from PyQt5.QtGui import QPixmap
from Volatility import calculate_volatility
from BlackSchole_calculate import  calculate_blackscholes
from merge_csv_file import merge_csv_files 
from csv_to_db import csv_to_sqlite

class DataProcessGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.tr('Data Processing GUI'))
        self.setGeometry(300, 300, 400, 200)
        background_label = QLabel(self)
        background_pixmap = QPixmap('GIO.jpg')  # Replace 'GIO.jpg' with the actual path to your image file
        background_label.setPixmap(background_pixmap)
        background_label.setGeometry(0, 0, background_pixmap.width(), background_pixmap.height())
        # Create widgets
        self.file_list_widget = QListWidget()  # Widget to display selected files
        self.clear_button = QPushButton(self.tr('Clear'))
        self.clear_button.setStyleSheet("background-color: black; color: white;")  # Change clear button style
        self.merge_data_button = QPushButton(self.tr('Merge Data'))
        self.merge_data_button.setStyleSheet("background-color: red; color: white;")  # Change merge data button style
        self.convert_to_db_button = QPushButton(self.tr('Convert to SQLite DB'))  # New convert to SQLite DB button
        self.calculate_button = QPushButton(self.tr('Calculate Volatility'))
        self.calculate_blackscholes_button = QPushButton(self.tr('Calculate Black-Scholes')) 
        self.browse_button = QPushButton(self.tr('Browse'))

        # Connect button signals
        self.browse_button.clicked.connect(self.browse_file)
        self.clear_button.clicked.connect(self.clear_file_list)  # Connect clear button signal
        self.convert_to_db_button.clicked.connect(self.convert_to_sqlite_db)  # Connect convert to SQLite DB button signal
        self.merge_data_button.clicked.connect(self.merge_data)
        
        self.calculate_button.clicked.connect(self.calculate_volatility)
        self.calculate_blackscholes_button.clicked.connect(self.calculate_blackscholes) 
        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.browse_button)
        layout.addWidget(self.file_list_widget)  # Add file list widget
        
        # Add merge data and clear buttons in a horizontal layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.merge_data_button)
        button_layout.addWidget(self.clear_button)
        layout.addLayout(button_layout)

        layout.addWidget(self.convert_to_db_button)  # Add convert to SQLite DB button

        layout.addWidget(self.calculate_button)
        layout.addWidget(self.calculate_blackscholes_button) 

        self.setLayout(layout)

        self.selected_files = []
    def browse_file(self):
        options = QFileDialog.Options()
        file_paths, _ = QFileDialog.getOpenFileNames(self, self.tr('Open Files'), '', self.tr('CSV Files (*.csv);;All Files (*)'), options=options)

        if file_paths:
            self.selected_files = file_paths
            
            # Clear and update the file list widget
            #self.file_list_widget.clear() 
            for file_path in file_paths:
                item = QListWidgetItem(file_path)
                self.file_list_widget.addItem(item)
    def clear_file_list(self):
        self.file_list_widget.clear()  # Clear the file list widget
        self.selected_files.clear()  # Clear the selected files list                
    def merge_data(self):
            try:
                if len(self.selected_files) > 1:  # Check if there are multiple files selected
                    output_file, _ = QFileDialog.getSaveFileName(self, self.tr('Save As'), '', self.tr('CSV Files (*.csv);;All Files (*)'))

                    if output_file:
                        # Call the merge_csv_files function to merge the selected CSV files
                        merge_csv_files(self.selected_files, output_file)

                        QMessageBox.information(self, self.tr('Merge Data'), self.tr('Data merge completed!'), QMessageBox.Ok)
                    else:
                        QMessageBox.information(self, self.tr('Merge Data'), self.tr('Please provide a valid output file path.'), QMessageBox.Ok)
                else:
                    QMessageBox.information(self, self.tr('Merge Data'), self.tr('Please select more than one CSV file for merging.'), QMessageBox.Ok)
            except Exception as e:
                QMessageBox.critical(self, self.tr('Error'), self.tr(f'Error during data merge: {str(e)}'), QMessageBox.Ok)

    def convert_to_sqlite_db(self):
        try:
            if self.selected_files:
                output_file, _ = QFileDialog.getSaveFileName(self, self.tr('Save As'), '', self.tr('SQLite Database Files (*.db);;All Files (*)'))

                if output_file:
                    csv_to_sqlite(self.selected_files, output_file)
                    QMessageBox.information(self, self.tr('Convert to SQLite DB'), self.tr('CSV files have been converted to SQLite DB successfully!'), QMessageBox.Ok)
                else:
                    QMessageBox.information(self, self.tr('Convert to SQLite DB'), self.tr('Please provide a valid output file path.'), QMessageBox.Ok)
            else:
                QMessageBox.information(self, self.tr('Convert to SQLite DB'), self.tr('Please select CSV files to convert.'), QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, self.tr('Error'), self.tr(f'Error during conversion to SQLite DB: {str(e)}'), QMessageBox.Ok)


    def calculate_volatility(self):
        try:
            if len(self.selected_files) == 1:  # Check if only one file is selected
                file_path = self.selected_files[0]
                progress_dialog = QProgressDialog(self.tr("Calculating Volatility..."), self.tr("Cancel"), 0, 100, self)
                progress_dialog.setWindowModality(2)
                progress_dialog.show()

                def progress_callback(progress):
                    progress_dialog.setValue(progress)
                    QApplication.processEvents()

                calculate_volatility(file_path, progress_callback=progress_callback)
                progress_dialog.close()

                QMessageBox.information(self, self.tr('Volatility'), self.tr('Volatility calculation completed!'), QMessageBox.Ok)
            else:
                QMessageBox.information(self, self.tr('Error'), self.tr('Please select only one CSV file for data calculation.'), QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, self.tr('Error'), self.tr(f'Error during volatility calculation: {str(e)}'), QMessageBox.Ok)
            progress_dialog.close()
            
    def calculate_blackscholes(self):
        try:
            if len(self.selected_files) == 1:  # Check if only one file is selected
                file_path = self.selected_files[0]
                progress_dialog = QProgressDialog(self.tr("Calculating Black-Scholes..."), self.tr("Cancel"), 0, 100, self)
                progress_dialog.setWindowModality(2)
                progress_dialog.show()

                def progress_callback(progress):
                    progress_dialog.setValue(progress)
                    QApplication.processEvents()

                calculate_blackscholes(file_path, progress_callback=progress_callback)
                progress_dialog.close()

                QMessageBox.information(self, self.tr('Black-Scholes'), self.tr('Black-Scholes calculation completed!'), QMessageBox.Ok)
            else:
                QMessageBox.information(self, self.tr('Error'), self.tr('Please select only one CSV file for data calculation.'), QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, self.tr('Error'), self.tr(f'Error during Black-Scholes calculation: {str(e)}'), QMessageBox.Ok)
            progress_dialog.close()


if __name__ == '__main__':
    app = QApplication(sys.argv) 
    window = DataProcessGUI()
    window.show()
    sys.exit(app.exec_())