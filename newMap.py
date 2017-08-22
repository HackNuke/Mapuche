from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIntValidator
from Pytes import pytes
import sys

class newMapWindow(QtWidgets.QDialog):
    def __init__(self):
        super(newMapWindow,self).__init__()
        uic.loadUi('UI/newMap.ui', self)
        self.sizeEdit.setValidator(QIntValidator(1,950))
        self.label_2.setText("Layers: " + str(self.horizontalSlider.value()))
        self.saveBox.accepted.connect(self.save)
        self.saveBox.rejected.connect(self.cancel)
        self.horizontalSlider.valueChanged.connect(self.updateLabel)
        self.items = ["Mapache v1"]
        for i in self.items:
            self.listWidget.addItem(i)
    
    def writefile(self):
        mapfile = open(self.archivo, "w")
        self.header = self.formats + str(self.layer) + str(self.tiles) + " "
        mapfile.write(self.header)
        mapfile.close()
        mapfile = pytes.Pyte(self.archivo)
        for l in range(self.layer):
            mapfile.op.read()
            for i in range((self.tiles*(10**self.counter))**2):
                mapfile.write(0b00000000)
        mapfile.stapit()
        self.close()
        
    
    @pyqtSlot()
    def save(self):
        if self.listWidget.currentItem().text() == "Mapache v1":
            self.formats = "MA1"
        self.layer = self.horizontalSlider.value()
        self.counter = 0
        try:
            self.tiles = int(self.sizeEdit.text())
        except:
            return QtWidgets.QMessageBox.about(self, 'Error','Size can only be a number')
        if self.nameEdit.text() == "":
            QtWidgets.QMessageBox.about(self, 'Error','You didn\'t wrote a name to your file!')
        else:
            while len(str(self.tiles))>1:
                self.tiles = int(self.tiles/10)
                self.counter += 1
            self.archivo = QtWidgets.QFileDialog(self).getExistingDirectory() + '/' + self.nameEdit.text() + "." + self.formats.lower()
            self.writefile()


    def cancel(self):
        self.close()
    
    def updateLabel(self):
        self.label_2.setText("Layers: " + str(self.horizontalSlider.value()))
