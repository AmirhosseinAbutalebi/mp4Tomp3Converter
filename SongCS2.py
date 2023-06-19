# add needed library

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from moviepy.editor import *
import os, shutil, platform
import eyed3

class Ui_MainWindow(object):
    currentPath = "" #path for save item or check for sort
    pathWin = "" #path win
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 170)
        icon = QtGui.QIcon('Song2CV.png')
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.lineVertical = QtWidgets.QFrame(self.centralwidget)
        self.lineVertical.setGeometry(QtCore.QRect(225, 0, 20, 151))
        self.lineVertical.setFrameShape(QtWidgets.QFrame.VLine)
        self.lineVertical.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineVertical.setObjectName("lineVertical")

        self.labelConvert = QtWidgets.QLabel(self.centralwidget)
        self.labelConvert.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.labelConvert.setObjectName("labelConvert")

        self.labelSort = QtWidgets.QLabel(self.centralwidget)
        self.labelSort.setGeometry(QtCore.QRect(245, 10, 71, 16))
        self.labelSort.setObjectName("labelSort")

        self.labelOpenDialogConvert = QtWidgets.QLabel(self.centralwidget)
        self.labelOpenDialogConvert.setGeometry(QtCore.QRect(10, 40, 195, 21))
        self.labelOpenDialogConvert.setObjectName("labelOpenDialogConvert")

        self.labelOpendialogSort = QtWidgets.QLabel(self.centralwidget)
        self.labelOpendialogSort.setGeometry(QtCore.QRect(245, 40, 175, 16))
        self.labelOpendialogSort.setObjectName("labelOpendialogSort")

        self.pushButtonDialogConvert = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDialogConvert.setGeometry(QtCore.QRect(200, 40, 31, 23))
        self.pushButtonDialogConvert.setObjectName("pushButtonDialogConvert")
        self.pushButtonDialogConvert.clicked.connect(self.useDialogConvert)

        self.pushButtonOpenDialog = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonOpenDialog.setGeometry(QtCore.QRect(405, 40, 31, 23))
        self.pushButtonOpenDialog.setObjectName("pushButtonOpemDialog")
        self.pushButtonOpenDialog.clicked.connect(self.useDialogSort)

        self.textEditConvert = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditConvert.setGeometry(QtCore.QRect(10, 70, 215, 21))
        self.textEditConvert.setObjectName("textEdit")

        self.textEditSort = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditSort.setGeometry(QtCore.QRect(245, 70, 191, 21))
        self.textEditSort.setObjectName("textEdit_2")

        self.pushButtonConvert = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonConvert.setGeometry(QtCore.QRect(10, 102, 215, 31))
        self.pushButtonConvert.setObjectName("pushButtonConvert")
        self.pushButtonConvert.clicked.connect(self.convertMp4ToMp3)

        self.pushButtonSort = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSort.setGeometry(QtCore.QRect(245, 100, 191, 31))
        self.pushButtonSort.setObjectName("pushButtonSort")
        self.pushButtonSort.clicked.connect(self.sortSong)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SongCS2"))
        self.labelConvert.setText(_translate("MainWindow", "Convert To Mp3 :"))
        self.labelSort.setText(_translate("MainWindow", "Sort Song :"))
        self.labelOpenDialogConvert.setText(_translate("MainWindow", "Select File mp4 Till Convert mp3 :"))
        self.labelOpendialogSort.setText(_translate("MainWindow", "Select Folder For Sort Song:"))
        self.pushButtonDialogConvert.setText(_translate("MainWindow", "..."))
        self.pushButtonOpenDialog.setText(_translate("MainWindow", "..."))
        self.pushButtonConvert.setText(_translate("MainWindow", "Convert"))
        self.pushButtonSort.setText(_translate("MainWindow", "Sort"))

    '''
    def for convert to mp3 and use multi thread
    and use try except
    '''
    def convertMp4ToMp3(self):
        try:
            if self.currentPath is not None:
                string = self.currentPath.split("/")[-1]
                size = len(string)
                nameMusic = string.replace(string[size-1], "3")
                self.worker = WorkerThread()
                self.worker.getItem(self.currentPath, nameMusic)
                self.messageBoxWait()
                self.worker.start()
                self.worker.finished.connect(self.messageBoxDone)
        except:
           self.messageBoxError("Please Choose Mp4 For Convert \nNot Another Type Of Video Or Anything...") 
            
    '''
    def for message box done when convert complete
    '''
    def messageBoxDone(self):
        icon = QtGui.QIcon('Song2CV.png')
        msgBox = QMessageBox()
        msgBox.setWindowIcon(icon)
        msgBox.setWindowTitle("Done")
        msgBox.setText("Convert Compelete")
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    '''
    def for message box when start the convert
    '''
    def messageBoxWait(self):
        icon = QtGui.QIcon('Song2CV.png')
        msgBox = QMessageBox()
        msgBox.setWindowIcon(icon)
        msgBox.setWindowTitle("Done")
        msgBox.setText("Press Ok Till Start Converting And Waiting Till Convert Compelete \n Then You Get Message Convert Compelete.")
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()
     
    '''
    def for message box when editbox is empty
    '''   
    def messageBoxError(self, message):
        icon = QtGui.QIcon('Song2CV.png')
        msgBox = QMessageBox()
        msgBox.setWindowIcon(icon)
        msgBox.setWindowTitle("Error")
        msgBox.setText(message)
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    # def for check os system
    def checkOs(self):
        system = platform.system()
        return system

    #open dialog convert and select item mp4 for convert
    def useDialogConvert(self):
        file, _= QFileDialog.getOpenFileName()
        self.currentPath = file
        self.pathWin = self.currentPath.replace("/", "\\")
        mp4 = file[-3:]
        if mp4 == "mp4":
            if self.currentPath:
                if self.checkOs == "Windows":
                    self.textEditConvert.setText(self.pathWin)
                self.textEditConvert.setText(self.currentPath)
        else:
            file = ""
            self.currentPath = ""
            self.path = ""
            self.messageBoxError("Please Choose Mp4 For Convert \nNot Another Type Of Video Or Anything...")
            
    #use dialog and select directory for sort
    def useDialogSort(self):
        self.currentPath = QFileDialog.getExistingDirectory()
        self.pathWin = self.currentPath.replace("/", "\\")
        if self.currentPath:
            if self.checkOs == "Windows":
                self.textEditSort.setText(self.pathWin)
            self.textEditSort.setText(self.currentPath)
    #sort song with eyed3 and           
    def sortSong(self):
        try:
            pathSongFind = self.textEditSort.toPlainText()
            for directory, dirs, files in os.walk(pathSongFind):
                for file in files:
                    if file.endswith('.mp3' or '.wav' or '.flac' or '.m4a'):
                        audio = eyed3.load(file)
                        nameAudio = str(file).replace(".mp3", "")
                        artist = audio.tag.artist
                        if artist == None:
                            artist = nameAudio
                        destination = pathSongFind + "/" + str(artist)
                        if not(os.path.exists(destination)):
                            os.mkdir(destination)
                        songFile = pathSongFind + "/" + file
                        shutil.move(songFile, destination)
        except:
            pass
#class theard when start convert we need to dont stop and freeze program
class WorkerThread(QThread):
    path = ""
    nameMusic = ""
    # get item path and name music that need for convert
    def getItem(self, path, nameMusic):
        self.path = path
        self.nameMusic = nameMusic
    #start convert with VideoFileClip
    def run(self):
        video = VideoFileClip(self.path)
        video.audio.write_audiofile(self.nameMusic)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
