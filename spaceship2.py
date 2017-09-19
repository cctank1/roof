import sys
import threading
import time

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
        self.radioButton_2.toggled.connect(self.on_p1_click)
        self.radioButton_3.toggled.connect(self.on_p2_click)
        self.radioButton_4.toggled.connect(self.on_p3_click)
        self.radioButton_5.toggled.connect(self.on_p4_click)
        self.radioButton_6.toggled.connect(self.on_p5_click)
        self.radioButton_7.toggled.connect(self.on_p6_click)
        self.radioButton_8.toggled.connect(self.on_p7_click)
        self.radioButton_9.toggled.connect(self.on_p8_click)
        self.radioButton_10.toggled.connect(self.on_p9_click)
    
    def go_to(self, destination):
        self.destination = destination
        self.eta = abs(self.destination - self.location)**2 / 2
        self.dial.setMaximum(int(self.eta))  # Set the proper range for ETA
        threading.Thread(target=self.travel).start()
    
    def travel(self):
        self.groupBox.setEnabled(False)
        while not self.stop_button_pressed:
            self.dial.setValue(int(self.eta))  # Update the ETA value on the dial
            self.label_4.setText("ETA: {}s".format(self.eta))
            if self.eta <= 0:
                break
            self.eta = round(self.eta - 0.1, 1)
            time.sleep(0.1)
        
        self.location = self.destination
        self.label_3.setText("Location: {}".format(self.location))
        self.groupBox.setEnabled(True)

    def on_launch_click(self):
        spaceship_name = self.lineEdit.text()
        captain_name = self.lineEdit_2.text()
        QMessageBox.information(self, "Info",
                                "Welcome aboard {}, Captain {}.".format(
                                spaceship_name, captain_name))
    
    def on_p0_click(self):
        if self.radioButton.isChecked():
            self.go_to(0)
    
    def on_p1_click(self):
        if self.radioButton_2.isChecked():
            self.go_to(1)
    
    def on_p2_click(self):
        if self.radioButton_3.isChecked():
            self.go_to(2)
    
    def on_p3_click(self):
        if self.radioButton_4.isChecked():
            self.go_to(3)
    
    def on_p4_click(self):
        if self.radioButton_5.isChecked():
            self.go_to(4)
    
    def on_p5_click(self):
        if self.radioButton_6.isChecked():
            self.go_to(5)
    
    def on_p6_click(self):
        if self.radioButton_7.isChecked():
            self.go_to(6)
    
    def on_p7_click(self):
        if self.radioButton_8.isChecked():
            self.go_to(7)
    
    def on_p8_click(self):
        if self.radioButton_9.isChecked():
            self.go_to(8)
    
    def on_p9_click(self):
        if self.radioButton_10.isChecked():
            self.go_to(9)
    
    def closeEvent(self, event):
        self.stop_button_pressed = True
        event.accept()  # Tell Qt it is OK to quit the program


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
