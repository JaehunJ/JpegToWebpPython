from cProfile import run
from lib2to3.pytree import convert
from math import fabs
from re import S
from xmlrpc.client import Boolean
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PIL import Image
from PIL import ImageCms
import ntpath
import piexif
import webbrowser
import asyncio
import sys
import time
import io
import os

imageList = []
useExif = True
extern = "webp"

def convert_to_sRGB(img):
        icc = img.info.get('icc_profile', '')
        if icc:
            io_handle = io.BytesIO(icc)
            src_profile = ImageCms.ImageCmsProfile(io_handle)
            dst_profile = ImageCms.createProfile('sRGB')
            img2 = ImageCms.profileToProfile(img, src_profile, dst_profile)
        
        return img2

class WebpApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
    
    def setupUi(self):
        self.resize(410, 500)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 100, 24))
        self.pushButton.setObjectName("pushButton")
        
        self.pushButtonGall = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonGall.setGeometry(QtCore.QRect(120, 10, 100, 24))
        # self.pushButtonGall.setGeometry(QtCore.QRect(300, 10, 100, 24))
        self.pushButtonGall.setObjectName("pushButtonGall")
        
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 80, 281, 51))
        self.groupBox.setObjectName("groupBox")
        self.laQauli = QtWidgets.QLabel(self.groupBox)
        self.laQauli.setGeometry(QtCore.QRect(10, 20, 48, 16))
        self.laQauli.setObjectName("laQauli")
        self.horizontalSlider = QtWidgets.QSlider(self.groupBox)
        self.horizontalSlider.setGeometry(QtCore.QRect(40, 20, 160, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.laNumQ = QtWidgets.QLabel(self.groupBox)
        self.laNumQ.setGeometry(QtCore.QRect(210, 20, 48, 16))
        self.laNumQ.setObjectName("laNumQ")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton_2.setGeometry(QtCore.QRect(160, 10, 131, 24))
        self.pushButton_2.setGeometry(QtCore.QRect(270, 10, 131, 24))
        self.pushButton_2.setObjectName("pushButton_2")
        # self.pushButton_2.setStyleSheet("background-color: rgb(58, 134, 255);color:white;")
        self.listView = QtWidgets.QListWidget(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 140, 390, 292))
        self.listView.setObjectName("listView")
        self.laFileNum = QtWidgets.QLabel(self.centralwidget)
        self.laFileNum.setGeometry(QtCore.QRect(10, 440, 108, 16))
        self.laFileNum.setObjectName("laFileNum")

        self.pushButton_2.setEnabled(False)
        
        self.pushButton_export = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_export.setGeometry(QtCore.QRect(10, 45, 100, 24))
        self.pushButton_export.setObjectName("pushButton_export")
        self.laExport = QtWidgets.QLabel(self.centralwidget)
        self.laExport.setGeometry(QtCore.QRect(115, 48, 48, 16))
        self.laExport.setObjectName("laExport")
        
        self.laExportValue = QtWidgets.QLabel(self.centralwidget)
        self.laExportValue.setGeometry(QtCore.QRect(145, 48, 350, 16))
        self.laExportValue.setObjectName("laExportValue")
        
        self.progress = QtWidgets.QProgressBar(self.centralwidget)
        self.progress.setGeometry(QtCore.QRect(10, 460, 395, 30))
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        # self.progress.setValue(50)
        
        ##event add
        
        self.horizontalSlider.valueChanged.connect(self.setSliderEvent)
        self.pushButton.clicked.connect(self.showFileDialog)
        self.pushButton_2.clicked.connect(self.convert)
        self.pushButtonGall.clicked.connect(self.openGall)
        self.pushButton_export.clicked.connect(self.showDirectoryDialog)
        # self.textBrowser.setDrag
        self.setAcceptDrops(True)
        
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.retranslateUi()
        self.show()
        
    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) :
        if(event.mimeData().hasUrls()):
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event: QtGui.QDropEvent) :
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        
        if len(files) != 0:
            for file in files:
                self.listView.addItem(file)
                imageList.append(file)
                
            self.pushButton_2.setEnabled(True)
            self.laFileNum.setText("파일수 : "+str(len(imageList)))
        else:
            print("file null")

    def openGall(self):
        imageList.clear()
        self.listView.clear()
        self.pushButton_2.setEnabled(True)
        self.pushButton.setEnabled(True)
        self.horizontalSlider.setEnabled(True)
        self.listView.setEnabled(True)

    def retranslateUi(self):
        self.setWindowTitle("Jpeg->Webp v1.1.0")
        self.pushButton.setText("파일선택")
        self.pushButtonGall.setText("파일 초기화")
        self.groupBox.setTitle("설정")
        self.laQauli.setText("품질")
        self.laNumQ.setText("0")
        self.pushButton_2.setText("변환")
        self.laFileNum.setText("파일수 : 0")
        self.horizontalSlider.setValue(100)
        self.horizontalSlider.setMinimum(50)
        self.exportPath = ""
        print(self.exportPath)
        self.laExportValue.setText(self.exportPath)
        self.pushButton_export.setText("저장 경로 설정")
        self.laExport.setText("경로- ")
        self.q = 100
        self.progress.setValue(0)
        self.progress.setEnabled(False)
 
    def setSliderEvent(self):
        self.laNumQ.setText(str(self.horizontalSlider.value()))
        self.q = self.horizontalSlider.value()
        
        
    def showDirectoryDialog(self):
        self.exportPath = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.laExportValue.setText(self.exportPath)
        
    def showFileDialog(self):        
        fname = QtWidgets.QFileDialog.getOpenFileNames(self, "open", ".", "JPEG (*.jpg *.jpeg)")
        
        if fname[0]:
            for file in fname[0]:
                self.listView.addItem(file)
                imageList.append(file)
            
            self.pushButton_2.setEnabled(True)
            self.laFileNum.setText("파일수 : "+str(len(imageList)))

    def convert(self):
        self.setWindowTitle("변환 중...")
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.horizontalSlider.setEnabled(False)
        self.listView.setEnabled(False)
        self.progress.setEnabled(True)
        t = Thread1(self, self.exportPath, self.q)
        t.progress.connect(self.progress_emitted)
        t.signal_end.connect(self.signal_end_emitted)
        t.start()
        
    @pyqtSlot()
    def signal_end_emitted(self):
        self.pushButton_2.setEnabled(True)
        self.pushButton.setEnabled(True)
        self.setWindowTitle("Jpeg->Webp v1.1.0")
        self.horizontalSlider.setEnabled(True)
        self.listView.setEnabled(True)
        self.progress.setEnabled(False)
        
    @pyqtSlot(int)
    def progress_emitted(self, progress):
        print(progress)
        self.progress.setValue(progress)
        
class Thread1(QThread):
    progress = pyqtSignal(int)
    signal_end = pyqtSignal()
    
    #parent = MainWidget을 상속 받음.
    def __init__(self, parent, path, q):
        super().__init__(parent)
        self.path = path
        self.q = q
        
    def run(self):
        count = len(imageList)
        iter = 0
        for i in imageList:
            file_name = ntpath.basename(i)
            k = file_name.rfind(".")
            lm = Image.open(i)
            lmRgb = lm.convert("RGB")
            
            outputPath = ""
            if len(self.path) != 0:
                outputPath = self.path+"/"+ file_name[:k]+"." + extern
            else:
                outputPath = file_name[:k]+"." + extern
            
            
            lmRgb.save(outputPath,extern, quality = self.q, subsampling=0)
            iter = iter+1
            self.ratio = (iter/count)*100
            # print(self.ratio)
            self.progress.emit(int(self.ratio))
            
        self.signal_end.emit()
            
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = WebpApp()
    sys.exit(app.exec())
