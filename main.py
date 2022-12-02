import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import threading
import socket
# Lien GitHub : https://github.com/rayane751/controleR3.09
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__host = "localhost"
        self.__port = 10001
        self.__sock = socket.socket()
        self.__thread = None
        arret_thread =  bool(False)

        self.setWindowTitle("Conversion de Température")

        widget = QWidget()
        self.setCentralWidget(widget)

        grid = QGridLayout()
        widget.setLayout(grid)

        self.labTp = QLabel("Compteur : ")
        
        self.text = QLineEdit("0")
        start = QPushButton("Start")
        rst = QPushButton("Reset")
        stop = QPushButton("Stop")
        quit = QPushButton("Quitter")
        connect = QPushButton("Connect")
        self.timer = QTimer()
        
        
        
        
        
        

        grid.addWidget(self.labTp, 0, 0)
        grid.addWidget(self.text, 1, 0,1,0)
        grid.addWidget(quit, 5, 1)
        grid.addWidget(start, 2, 0,1,0)
        grid.addWidget(rst, 3, 0)
        grid.addWidget(stop, 3, 1)
        
        
        grid.addWidget(connect, 5, 0)
        self.text.setEnabled(False)
        self.time = QTime(0, 0, 0)
        quit.clicked.connect(self.__actionQuitter)
        rst.clicked.connect(self.__Reset)
        self.timer.timeout.connect(self.temps)
        self.text.setText(self.time.toString("s"))
        self.show()
        start.clicked.connect(self.start)
        connect.clicked.connect(self.__connect)
        stop.clicked.connect(self.__Stop)
        
        

    def _timer(self):
        msg = QMessageBox()
        msg.setWindowTitle("Help")
        msg.setText("Permet de convertir un nombre soit de Kelvin vers Celcius, soit de Celcuis vers Kelvin")
        msg.exec()

    def __actionQuitter(self):
        
        msg = "Quitter"
        
        try:
            self.__sock.send(msg.encode())
            self.__stop()
            self.__sock.close()
            QCoreApplication.exit(0)
        except BrokenPipeError:
            print ("erreur, socket fermée")
        except OSError:
            QCoreApplication.exit(0)     
        return msg
        

    def __Reset(self):
        self.time = QTime(0, 0, 0)
        self.text.setText(self.time.toString("s"))
        self.timer.stop()
        msg = "Reset"
        try:
            self.__sock.send(msg.encode())
        except BrokenPipeError:
            erreur=QMessageBox() 
            erreur.setText("erreur, socket fermée")
            erreur.exec()
        except OSError:
            pass  
        return msg

    def start(self):
        
        self.timer.start(1000)
        msg = "Start"
        try:
            self.__sock.send(msg.encode())
        except BrokenPipeError:
            erreur=QMessageBox() 
            erreur.setText("erreur, socket fermée")
            erreur.exec()
        except OSError:
            pass  
    def temps(self):
        self.time = self.time.addSecs(1)
        self.text.setText(self.time.toString("s"))    
    def __Stop(self):
        self.timer.stop()
        msg = "Stop"
        try:
            self.__sock.send(msg.encode())
        except BrokenPipeError:
            erreur=QMessageBox() 
            erreur.setText("erreur, socket fermée")
            erreur.exec()
        except OSError:
            pass  


        

    def __connect(self) -> int:
        try :
            self.__sock.connect((self.__host,self.__port))
        except ConnectionRefusedError:
            erreur=QMessageBox() 
            erreur.setText("serveur non lancé ou mauvaise information")
            erreur.exec()
            return -1
        except ConnectionResetError:
            erreur1=QMessageBox() 
            erreur1.setText("serveur mal fermé il faut changer de port")
            erreur1.exec()
             
            return -1    
        except ConnectionError:
            erreur2=QMessageBox() 
            erreur2.setText("Erreur de connection")
            erreur2.exec()
             
            return -1
        else :
            erreur3=QMessageBox() 
            erreur3.setText("connexion réalisée")
            erreur3.exec()
             
            return 0    
    
       



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()