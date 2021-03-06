from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys
import logging

from plyer import notification 

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.time = 25 * 60
        self.running = False
        self.num_pomodoros = 0
        self.mode = "Pomodoro"
        self.minute_length = 60 #In Seconds

        self.title = "Pomodoro"
        self.left = 20
        self.top = 30
        self.width = 300
        self.height = 200

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        
        
        self.label = QLabel()
        self.label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel {font-family: Lucida Console; font-size:25px;}")

        self.mode_label = QLabel()
        self.mode_label.setAlignment(Qt.AlignCenter)
        self.mode_label.setStyleSheet("QLabel {font-size:20px;}")
        self.mode_label.setText(self.mode)

        self.num_pomodoros_label = QLabel()
        self.num_pomodoros_label.setAlignment(Qt.AlignCenter)
        self.num_pomodoros_label.setStyleSheet("QLabel {font-size:20px;}")
        self.num_pomodoros_label.setText(str(self.num_pomodoros))

        self.set_label()
        start_button = QPushButton("Start", self)

        stop_button = QPushButton("Stop", self)

        pomodoro_button = QPushButton("Pomodoro", self)
        short_break_button = QPushButton("Short Break", self)
        long_break_button = QPushButton("Long Break", self)

        start_button.pressed.connect(self.Start)
        stop_button.pressed.connect(self.Stop)
        pomodoro_button.pressed.connect(self.Pomodoro)
        long_break_button.pressed.connect(self.Long_break)
        short_break_button.pressed.connect(self.Short_break)

        layout_outer = QVBoxLayout()
        layout_outer.addWidget(self.mode_label)
        layout_outer.addWidget(self.num_pomodoros_label)
        layout_outer.addWidget(self.label)

        layout_start_stop = QHBoxLayout()
        layout_start_stop.addWidget(start_button)
        layout_start_stop.addWidget(stop_button)
        layout_outer.addLayout(layout_start_stop)

        layout_buttons = QVBoxLayout()
        layout_buttons.addWidget(pomodoro_button)
        layout_buttons.addWidget(short_break_button)
        layout_buttons.addWidget(long_break_button)

        layout_outer.addLayout(layout_buttons)
        self.setLayout(layout_outer)

        self.timer.start(1000)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def set_label(self):
        seconds = (str(self.time % 60)
                    if len(str(self.time % 60)) == 2 
                    else "0" + str(self.time % 60))
        self.label.setText(str(int(self.time / 60)) + " : " + seconds)

        self.num_pomodoros_label.setText(str(self.num_pomodoros))
    def update_time(self):
        if self.running:
            self.time -= 1
            self.set_label()
            if self.time <= 0:
                if self.mode == "Pomodoro":
                    if self.num_pomodoros % 3 == 0 and self.num_pomodoros != 0:
                        notification.notify(
                            title = "Take a Long Break!",
                            message = "Pomodoro is over. Take a long break.",
                            timeout = 5,
                        )
                        self.Long_break()
                    else:
                        notification.notify(
                            title = "Take a Shiort Break!",
                            message = "Pomodoro is over. Take a short break.",
                            timeout = 5,
                        )
                        self.Short_break()
                    self.num_pomodoros += 1

                elif self.mode == "Short Break":

                    notification.notify(
                        title = "Beginning Pomodoro",
                        message = "Short break is over",
                        timeout = 5,
                    )
                    self.Pomodoro()

                elif self.mode == "Long Break":
                    notification.notify(
                        title = "Beginning Pomodoro",
                        message = "Long break is over",
                        timeout = 5,
                    )
                    self.Pomodoro()
                    self.num_pomodoros += 1
                self.Start()

    def Start(self):
        if self.running:
            return
        else:
            self.running = True

    def Stop(self):
        if not self.running:
            return
        else:
            self.running = False
    # Variable is here for testing purposes.
    # Makes it much easier to shorten times

    def Pomodoro(self):
        logging.info("Starting Pomodoro %s", str(self.num_pomodoros))
        self.running = False
        self.time = 25 * self.minute_length
        self.mode = "Pomodoro"
        self.set_label()
        self.mode_label.setText(self.mode)

    def Short_break(self):
        logging.info("Starting Short Break")
        self.running = False
        self.time = 5 * self.minute_length
        self.mode = "Short Break"
        self.mode_label.setText(self.mode)
        self.set_label()

    def Long_break(self):
        logging.info("Starting Long Break")
        self.running = False
        self.time = 15 * self.minute_length
        self.mode = "Long Break"
        self.mode_label.setText(self.mode)
        self.set_label()


if __name__ == "__main__":
    logging.basicConfig(
        filename='pomo_error.log',
        format = '%(asctime)s %(levelname)s:%(message)s',
        datefmt='%M:%S',
        level=logging.DEBUG)
    logging.info("Started Pomodoro")

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
