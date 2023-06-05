from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTextBrowser, QLineEdit, QPushButton, \
    QWidget, QLabel

from Connect import ConnectTCP

class UsernameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Username Input")
        self.layout = QVBoxLayout()

        # Username
        self.label = QLabel("Введите имя пользователя:")
        self.username_input = QLineEdit()
        self.username_layout = QHBoxLayout()
        self.username_layout.addWidget(self.label)
        self.username_layout.addWidget(self.username_input)


        # Ip
        self.label_host = QLabel("Введите ip хоста:")
        self.input_host = QLineEdit("127.0.0.1")
        self.host_layout = QHBoxLayout()
        self.host_layout.addWidget(self.label_host)
        self.host_layout.addWidget(self.input_host)

        self.label_port = QLabel("Введите порт:")
        self.input_port = QLineEdit("3000")
        self.port_layout = QHBoxLayout()
        self.port_layout.addWidget(self.label_port)
        self.port_layout.addWidget(self.input_port)

        self.submit_button = QPushButton("Submit")
        self.layout.addLayout(self.username_layout)
        self.layout.addLayout(self.host_layout)
        self.layout.addLayout(self.port_layout)
        # self.layout.addWidget(self.username_layout)
        # self.layout.addWidget(self.host_layout)
        # self.layout.addWidget(self.port_layout)
        self.layout.addWidget(self.submit_button)

        self.submit_button.clicked.connect(self.open_chat_window)

        self.setLayout(self.layout)

    def open_chat_window(self):
        username = self.username_input.text().strip()
        host = self.input_host.text().strip()
        port = self.input_port.text().strip()
        if username:
            self.hide()

            mainWindow = MainWindow(username, host, port)
            mainWindow.show()

class MainWindow(QMainWindow):

    username = "No name"

    def __init__(self, username, host, port):
        super().__init__()

        self.username = username
        self.host = host
        self.port = port

        self.connectTCP = ConnectTCP(self.receive_message)
        self.connectTCP.connect(nickName=username, host=host, port=int(port))
        self.setWindowTitle(f"TCP : {username}")

        # Создаем виджеты
        self.textBrowser = QTextBrowser()
        self.lineEdit = QLineEdit()
        self.buttonSend = QPushButton("Отправить")

        # Создаем главный вертикальный слой и добавляем виджеты в него
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.textBrowser)

        # Создаем горизонтальный слой для lineEdit и кнопки
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.lineEdit)
        horizontal_layout.addWidget(self.buttonSend)

        # Добавляем горизонтальный слой в вертикальный слой
        main_layout.addLayout(horizontal_layout)

        # Создаем виджет для размещения главного вертикального слоя
        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        # Устанавливаем виджет с вертикальным слоем в качестве центрального виджета окна
        self.setCentralWidget(central_widget)

        self.buttonSend.clicked.connect(self.buttonSendClicked)
        self.lineEdit.returnPressed.connect(self.buttonSendClicked)


    def buttonSendClicked(self):
        try:
            text = self.lineEdit.text().strip()
            text = f"{self.username}: {text}"
            if text:
                self.textBrowser.append(text)
                self.connectTCP.send(text)
            self.lineEdit.clear()
        except ConnectionResetError:
            print("Ошибка: Удаленный хост принудительно разорвал существующее подключение")

    def receive_message(self, message):
        self.textBrowser.append(message)

    def closeEvent(self, event):
        print("Форма закрывается...")
        self.connectTCP.close()

        super().closeEvent(event)




if __name__ == '__main__':
    app = QApplication([])
    window = UsernameWindow()
    window.show()
    app.exec_()
