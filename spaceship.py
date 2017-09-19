import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.location = 3
        self.eta = 0
        self.stop_button_pressed = False
        
        uic.loadUi("spaceship.ui", self)
        self.launchButton.clicked.connect(self.on_launch_click)
        
        self.radioButton.toggled.connect(self.on_p0_click)
        self.radioButton_2.toggled.connect(self.on_p0_click)
        self.radioButton_3.toggled.connect(self.on_p0_click)
        self.radioButton_4.toggled.connect(self.on_p0_click)
        self.radioButton_5.toggled.connect(self.on_p0_click)
        self.radioButton_6.toggled.connect(self.on_p0_click)
        self.radioButton_7.toggled.connect(self.on_p0_click)
        self.radioButton_8.toggled.connect(self.on_p0_click)
        self.radioButton_9.toggled.connect(self.on_p0_click)
        self.radioButton_10.toggled.connect(self.on_p0_click)
        
    def go_to(self, destination):
        self.desination = destination
        self.eta = abs(self.destination - self.location)**2 / 2
        self.dial.setMaximum(int(self.eta))
        
        
        
    def on_launch_click(self):
        spaceship_name = self.lineEdit.text()
        captain_name = self.lineEdit_2.text()
        QMessageBox.information(self, "Info", "Welcome aboard {}, Captian {}.".format(spaceship_name, captain_name))
        
        


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
