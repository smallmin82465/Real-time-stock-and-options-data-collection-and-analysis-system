from PyQt5.QtWidgets import QStyleFactory, QApplication

def apply_style():
    app = QApplication([])  # Create a dummy QApplication to set the style

    style_name = 'Fusion'  

    app.setStyle(QStyleFactory.create(style_name))

    # Set stylesheet for QPushButton (button style)
    app.setStyleSheet(
                    "QPushButton {"
                    "    background-color: #4CAF50;"
                    "    color: white;"
                    "    border: none;"
                    "    padding: 10px 20px;"
                    "    font-size: 16px;"
                    "    border-radius: 5px;"
                    "}"
                    "QPushButton:hover {"
                    "    background-color: #45a049;"
                    "}"
                    "QPushButton:pressed {"
                    "    background-color: #3c8e41;"
                    "}")

if __name__ == "__main__":
    apply_style()
