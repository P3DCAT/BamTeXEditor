from PyQt5.QtGui import QDoubleValidator, QFont, QIntValidator
from PyQt5.QtWidgets import QComboBox, QLineEdit, QCheckBox
from .ColorWidget import ColorWidget
from .OptionGlobals import *
from . import Globals

MIN_UINT8 = 0
MAX_UINT8 = (1 << 8) - 1

MIN_UINT32 = 0
MAX_UINT32 = (1 << 32) - 1

MIN_INT16 = -(1 << 15)
MAX_INT16 = (1 << 15) - 1

class Option(object):

    def __init__(self, field, name, field_type, enum_type=None, bam_version=None):
        self.field = field
        self.name = name
        self.field_type = field_type
        self.enum_type = enum_type
        self.bam_version = bam_version
        self.widget = None
        self.obj = None
        self.originalValue = None

    def getName(self):
        return self.name

    def getWidget(self):
        return self.widget

    def getObject(self):
        return self.obj

    def setObject(self, obj):
        self.obj = obj

    def getValue(self):
        return getattr(self.obj, self.field)

    def setValue(self, value):
        if self.obj is not None:
            setattr(self.obj, self.field, value)

    def createWidget(self, parent):
        font = QFont('Helvetica', 13)

        if self.field_type == BOOL:
            self.widget = QCheckBox(parent)
            self.widget.stateChanged.connect(self.checkboxChecked)
            self.checkboxChecked(False)
        elif self.field_type == COLOR:
            self.widget = ColorWidget(parent)
            self.widget.connect(self.colorSet)
        elif self.field_type == ENUM:
            self.widget = QComboBox(parent)
            self.widget.addItems(Globals.Enums[self.enum_type])
            self.widget.currentIndexChanged.connect(self.setValue)
        else:
            self.widget = QLineEdit(parent)
            self.widget.editingFinished.connect(self.textChanged)

            if self.field_type == UINT8:
                self.widget.setValidator(QIntValidator(MIN_UINT8, MAX_UINT8))
            elif self.field_type == UINT32:
                self.widget.setValidator(QDoubleValidator(MIN_UINT32, MAX_UINT32, 0))
            elif self.field_type == INT16:
                self.widget.setValidator(QIntValidator(MIN_INT16, MAX_INT16))
            elif self.field_type == FLOAT:
                self.widget.setValidator(QDoubleValidator())

        self.widget.setFont(font)
        return self.widget

    def clear(self):
        if self.field_type == BOOL:
            self.widget.setChecked(False)
        elif self.field_type == ENUM:
            self.widget.setCurrentIndex(0)
        else:
            self.widget.clear()

    def enable(self, bam_version):
        if self.bam_version is None or bam_version >= self.bam_version:
            self.widget.setEnabled(True)
        else:
            self.widget.setEnabled(False)

    def disable(self):
        self.widget.setEnabled(False)

    def loadValue(self):
        value = self.getValue()

        if self.field_type == BOOL:
            self.widget.setChecked(value)
        elif self.field_type == COLOR:
            self.widget.loadPandaColor(value)
        elif self.field_type == ENUM:
            self.widget.setCurrentIndex(value)
        else:
            self.originalValue = str(value)
            self.widget.setText(self.originalValue)

    def checkboxChecked(self, checked):
        checked = bool(checked)
        self.setValue(checked)
        self.widget.setText('Enabled' if checked else 'Disabled')

    def colorSet(self, color):
        color = Globals.qtColorToPanda(color)
        self.setValue(color)

    def restoreText(self):
        self.widget.setText(self.originalValue)

    def isOutOfBounds(self, value):
        return (
            (self.field_type == UINT8 and (value < MIN_UINT8 or value > MAX_UINT8)) or
            (self.field_type == UINT32 and (value < MIN_UINT32 or value > MAX_UINT32)) or
            (self.field_type == INT16 and (value < MIN_INT16 or value > MAX_INT16))
        )

    def textChanged(self):
        value = self.widget.text()

        if self.field_type == FLOAT:
            value = float(value)
        elif self.field_type != STRING:
            value = int(value)

        if self.isOutOfBounds(value):
            Globals.showError(f'This value is out of bounds.\n\nThe original value {self.originalValue} has been restored.')
            self.restoreText()
            return

        self.setValue(value)
