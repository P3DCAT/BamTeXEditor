from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QShortcut, QTabWidget, QWidget, QAction, QMenuBar, QVBoxLayout, QHBoxLayout, QListView, QLabel, QFormLayout, QFileDialog
from PyQt5.QtGui import QIcon, QKeySequence, QStandardItemModel, QStandardItem, QFont
from p3bamboo.BamFile import BamFile
from .Texture import Texture
from . import Globals
import traceback, webbrowser, os

class MainWidget(QWidget):

    def __init__(self, base):
        QWidget.__init__(self)
        self.base = base
        self.bam = None
        self.textures = []

        self.setWindowIcon(QIcon('icon.ico'))
        self.setWindowTitle('BamTeXEditor')
        self.setBackgroundColor(Qt.white)

        self.menuBar = QMenuBar()
        self.fileMenu = self.menuBar.addMenu('File')

        self.openAction = QAction('Open', self)
        self.saveAction = QAction('Save', self)
        self.saveAction.setEnabled(False)
        self.gitHubAction = QAction('GitHub', self)

        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.gitHubAction)

        self.openAction.triggered.connect(self.openBamFile)
        self.saveAction.triggered.connect(self.saveBamFile)
        self.gitHubAction.triggered.connect(self.openGitHubPage)

        self.saveShortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.saveShortcut.activated.connect(self.saveBamFile)

        self.baseWidget = QWidget()
        self.baseWidget.setContentsMargins(0, 0, 0, 0)

        self.listView = QListView()

        self.settingsWidget = QTabWidget()
        self.settingsWidget.setContentsMargins(0, 0, 0, 0)

        font = QFont('Helvetica', 13)
        self.options = []

        for name, options in Globals.TextureFields:
            tab = QWidget()
            tabLayout = QFormLayout(tab)

            for option in options:
                optionLabel = QLabel(f'{option.getName()}:')
                optionWidget = option.createWidget(tab)

                optionLabel.setFont(font)
                tabLayout.addRow(optionLabel, optionWidget)
                self.options.append(option)

            self.settingsWidget.addTab(tab, name)

        self.horizontalLayout = QHBoxLayout(self.baseWidget)
        self.horizontalLayout.addWidget(self.listView)
        self.horizontalLayout.addWidget(self.settingsWidget)

        self.baseLayout = QVBoxLayout(self)
        self.baseLayout.setContentsMargins(0, 0, 0, 0)
        self.baseLayout.addWidget(self.menuBar)
        self.baseLayout.addWidget(self.baseWidget)

        self.clear()

    def setBackgroundColor(self, color):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)

    def clear(self):
        for option in self.options:
            option.clear()
            option.disable()

    def openGitHubPage(self):
        webbrowser.open('https://github.com/P3DCAT/BamTeXEditor')

    def openBamFile(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, "Open a Panda3D model!", "", "Panda3D BAM models (*.bam)")

        if not self.filename:
            return

        self.bam = BamFile()

        try:
            with open(self.filename, 'rb') as f:
                self.bam.load(f)
        except:
            Globals.showError('Unfortunately, we could not load this model.\n\n{0}'.format(traceback.format_exc()))
            return

        self.clear()
        self.saveAction.setEnabled(True)
        self.textures = [texture for texture in self.bam.object_map.values() if isinstance(texture, Texture)]
        self.textures.sort(key=lambda tex: tex.filename or tex.name)
        self.listModel = QStandardItemModel(self.listView)

        for texture in self.textures:
            item = QStandardItem(texture.filename or texture.name)
            item.setEditable(False)
            self.listModel.appendRow(item)

        self.listView.setModel(self.listModel)
        self.listView.selectionModel().selectionChanged.connect(self.textureSelected)

        self.setWindowTitle(f'BamTeXEditor - {os.path.basename(self.filename)}')

        if self.textures:
            self.openTexture(0)

    def saveBamFile(self):
        if not self.saveAction.isEnabled():
            return

        if QMessageBox.question(self, 'BamTeXEditor', 'Are you sure you want to save your changes?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) != QMessageBox.Yes:
            return

        with open(self.filename, 'wb') as f:
            self.bam.write(f)

    def openTexture(self, index):
        self.index = index
        texture = self.textures[index]

        for option in self.options:
            option.setObject(texture)
            option.enable(self.bam.version)
            option.loadValue()

    def textureSelected(self, selection):
        index = selection.indexes()[0].row()
        self.openTexture(index)
