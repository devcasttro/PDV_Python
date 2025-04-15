# themes.py

def tema_escuro():
    return """
        QWidget {
            background-color: #2d2d2d;
            color: #FFFFFF;
            font-family: 'Segoe UI';
        }
        QPushButton {
            background-color: transparent;
            color: white;
            border: none;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #333;
            border-radius: 8px;
        }
        QLabel {
            color: #CCCCCC;
        }
    """

def tema_claro():
    return """
        QWidget {
            background-color: #F5F5F5;
            color: #2d2d2d;
            font-family: 'Segoe UI';
        }
        QPushButton {
            background-color: transparent;
            color: #2d2d2d;
            border: none;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #ddd;
            border-radius: 8px;
        }
        QLabel {
            color: #333333;
        }
    """
