from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QColorDialog, QHBoxLayout, QLineEdit, QWidget, QPushButton
from . import Globals

class ColorWidget(QWidget):

    def __init__(self, parent, *args, **kwargs):
        QWidget.__init__(self, parent, *args, **kwargs)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setFont(QFont('Helvetica', 13))
        self.lineEdit.editingFinished.connect(self.textChanged)

        self.colorButton = QPushButton(self)
        self.colorButton.setText('Colors')
        self.colorButton.clicked.connect(self.pickColor)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.colorButton)

        self.color = None
        self.callback = None

    def clear(self):
        self.lineEdit.clear()

    def setColor(self, color):
        self.color = color

        if self.callback:
            self.callback(color)

    def connect(self, callback):
        self.callback = callback

    def loadColor(self, color):
        if not color.isValid():
            return

        text = color.name(QColor.HexArgb)

        if self.lineEdit.text() != text:
            self.lineEdit.setText(text)

        self.setColor(color)

    def loadPandaColor(self, color):
        r = int(color.getX() * 255.0)
        g = int(color.getY() * 255.0)
        b = int(color.getZ() * 255.0)
        a = int(color.getW() * 255.0)
        self.loadColor(QColor(r, g, b, a))

    def pickColor(self):
        self.loadColor(QColorDialog.getColor(self.color, options=QColorDialog.ShowAlphaChannel))

    def textChanged(self):
        value = self.lineEdit.text()
        color = Globals.hexToColor(value)

        if color is None:
            self.loadColor(self.color)
            Globals.showError(f'The original value {self.lineEdit.text()} has been restored.')
            return

        self.setColor(color)
