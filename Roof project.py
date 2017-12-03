import RPi.GPIO as GPIO
import time
import sys
import threading

# Pins
STOP_OPENING_LIMIT_SWITCH = 10 
STOP_CLOSING_LIMIT_SWITCH = 11
sound = 9
light = 15

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(STOP_OPENING_LIMIT_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
GPIO.setup(STOP_CLOSING_LIMIT_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )      
GPIO.setup(sound, GPIO.IN)
GPIO.setup(light, GPIO.IN)




GPIO.setup(14, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import uic


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.is_open = False  #starts closed
        self.stop_button_pressed = False
        self.timeDoorWasOpened = 0
        
        uic.loadUi("GUIRoof.ui", self)
        threading.Thread(target=self.sensor).start()
        
        self.closeButton.clicked.connect(self.on_close)
        self.openButton.clicked.connect(self.on_open)
       
        self.haltButton.clicked.connect(self.on_halt)
        
        
    def sensor(self):
        prevLightStatus = True 
        while not self.stop_button_pressed:
            soundCurrent= GPIO.input(sound) and self.is_open and (time.time() - self.timeDoorWasOpened) > 10
            sensorStatus = GPIO.input(light)
            lightCurrent= (not sensorStatus) and self.is_open and prevLightStatus == True and (time.time() - self.timeDoorWasOpened) > 10
            if lightCurrent:
                self.logLabelStatus.setText("Dark")
            elif soundCurrent:
                self.logLabelStatus.setText("Thunder")
        
            if lightCurrent or soundCurrent:
                self.close()
            prevLightStatus = sensorStatus
            time.sleep(0.001)
            
                
    def on_close(self):
        if self.is_open: #checks to see if it is open, if it is open it will close.
            self.close() #calls the close function.
    
    def close(self):
        
         
        print("closing")
        
        GPIO.output(13, False)
        GPIO.output(14, False)
        GPIO.output(14, True)           #starts motor.
                       
        timeElapsed = 5
        while not GPIO.input(STOP_CLOSING_LIMIT_SWITCH): #while the swich input for closing is not true it keeps running.
                                       #once the swich is input is true it turns the motor off.
            
            time.sleep(0.1)
            timeElapsed = timeElapsed -0.1 
            self.progressBar.setValue(max (int((timeElapsed/5)*100), 0))
        GPIO.output(14, False)
        self.is_open = False  
       
        self.logLabelClosed.setText("Closed")
    def on_open(self):
        
        if not self.is_open:
            
            self.open()
           
    def open(self):
        print("Opening")
        GPIO.output(14, False)
        GPIO.output(13, False)
        GPIO.output(13, True)
        timeElapsed = 0
        while not GPIO.input(STOP_OPENING_LIMIT_SWITCH):
            
            
            time.sleep(0.1)
            timeElapsed = timeElapsed +0.1
            self.progressBar.setValue(min (int((timeElapsed/5)*100), 100))
            
        GPIO.output(13, False)   
        print("Open")
        
        
        self.is_open=True #sets roof var to open.
        self.timeDoorWasOpened = time.time()
        self.logLabelClosed.setText("Open")
        
            
        
    def on_halt(self):
        if self.is_open:
            self.logLabelStatus.setText("Rain")
            self.close()
        
    def closeEvent(self, event):
        self.stop_button_pressed = True
        event.accept()  # Tell Qt it is OK to quit the program
   
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

    
    
        

