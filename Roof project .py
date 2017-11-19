import RPi.GPIO as GPIO
import time
import sys
import threading


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#GPIO.setup(10, GPIO.IN) #, pull_up_down=GPIO.PUD_DOWN )
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )      # light
GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )

GPIO.setup(14, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import uic


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.is_open = True
        self.sound = False
        self.last_time = 0
        
        uic.loadUi("GUIRoof.ui", self)
        
        self.closeButton.clicked.connect(self.on_close)
        self.openButton.clicked.connect(self.on_open)
        self.haltButton.clicked.connect(self.on_halt)
        threading.Thread(target=self.sound).start()
        #threading.Thread(target=self.light).start()
        
            
    def on_close(self):
        self.close()
        
    def close(self):
        print("closing")
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(14, GPIO.OUT)
        GPIO.output(13, False)
        GPIO.output(14, False)
        time.sleep(0.2)       #this number shows how many seconds before the motor turns on. 
        GPIO.output(14, True)
        time.sleep(1)      #this number shows how many seconds the motor is on.
        GPIO.output(14, False)
        self.is_open = False
        
        
    def on_open(self):
        
        if not self.is_open:
            self.last_time = time.time()
            threading.Thread(target=self.open).start()
    def open(self):
        GPIO.output(14, False)
        GPIO.output(13, True)
        print("open")
        t0 = time.time()
        while GPIO.input(10) and (time.time() - t0) < 5:
           time.sleep(0.02)
            
                    
            #time.sleep(1)       #this number shows how many seconds before the motor turns on. 
        GPIO.output(13, False)
                 #this number shows how many seconds the motor is on.
        self.is_open=False
    #def light():
     #   while
       #     GPIO.input(11, True)
   # self.open()
    
    def sound():
        previous_time = 0
        while True:
            thunderDetected=GPIO.input(11)
            if thunderDetected and (time.time()-previous_time) > 0.5 and (time.time() - self.last_time) > 10:
                print("thunder")
                self.close()
                previous_time = time.time()
            time.sleep(0.0001)
            
        
    def on_halt(self):
        print("Halt")
        GPIO.output(14, False)
        GPIO.output(13, False)
        GPIO.cleanup()
        
    def closeEvent(self, event):
        self.on_halt()
    
        
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
    
    
        

