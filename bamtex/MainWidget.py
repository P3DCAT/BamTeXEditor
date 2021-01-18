from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QAction, QMenuBar, QVBoxLayout, QHBoxLayout, QListView, QLabel, QSpacerItem, QSizePolicy, QLineEdit, QFormLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from p3bamboo.BamFile import BamFile
from .Texture import Texture
import traceback, webbrowser

class MainWidget(QWidget):

    def __init__(self, base):
        QWidget.__init__(self)
        self.base = base
        self.bam = None
        self.textures = []

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

        self.baseWidget = QWidget()
        self.baseWidget.setContentsMargins(0, 0, 0, 0)

        self.listView = QListView()

        self.settingsWidget = QWidget()
        self.settingsWidget.setContentsMargins(0, 0, 0, 0)

        font = QFont('Helvetica', 13)
        self.settingsLayout = QFormLayout(self.settingsWidget)

        self.textureNameBox = QLineEdit(self.settingsWidget)
        self.colorFilenameBox = QLineEdit(self.settingsWidget)
        self.alphaFilenameBox = QLineEdit(self.settingsWidget)
        self.colorChannelsBox = QLineEdit(self.settingsWidget)
        self.alphaFileChannelBox = QLineEdit(self.settingsWidget)

        self.textureNameBox.setFont(font)
        self.colorFilenameBox.setFont(font)
        self.alphaFilenameBox.setFont(font)
        self.colorChannelsBox.setFont(font)
        self.alphaFileChannelBox.setFont(font)

        self.textureNameBox.textChanged.connect(self.changedName)
        self.colorFilenameBox.textChanged.connect(self.changedColorFilename)
        self.alphaFilenameBox.textChanged.connect(self.changedAlphaFilename)
        self.colorChannelsBox.textChanged.connect(self.changedColorChannels)
        self.alphaFileChannelBox.textChanged.connect(self.changedAlphaFileChannel)

        self.textureNameLabel = QLabel('Texture name:')
        self.colorFilenameLabel = QLabel('Color filename:')
        self.alphaFilenameLabel = QLabel('Alpha filename:')
        self.colorChannelsLabel = QLabel('Color channels:')
        self.alphaFileChannelLabel = QLabel('Alpha file channel:')

        self.textureNameLabel.setFont(font)
        self.colorFilenameLabel.setFont(font)
        self.alphaFilenameLabel.setFont(font)
        self.colorChannelsLabel.setFont(font)
        self.alphaFileChannelLabel.setFont(font)

        self.settingsLayout.addRow(self.textureNameLabel, self.textureNameBox)
        self.settingsLayout.addRow(self.colorFilenameLabel, self.colorFilenameBox)
        self.settingsLayout.addRow(self.alphaFilenameLabel, self.alphaFilenameBox)
        self.settingsLayout.addRow(self.colorChannelsLabel, self.colorChannelsBox)
        self.settingsLayout.addRow(self.alphaFileChannelLabel, self.alphaFileChannelBox)

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

    def showError(self, error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error)
        msg.setWindowTitle('Error!')
        msg.exec_()

    def clear(self):
        for box in (self.textureNameBox, self.colorFilenameBox, self.alphaFilenameBox, self.colorChannelsBox, self.alphaFileChannelBox):
            box.clear()
            box.setEnabled(False)

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
            self.showError('Unfortunately, we could not load this model.\n\n{0}'.format(traceback.format_exc()))
            return

        self.clear()
        self.saveAction.setEnabled(True)
        self.textures = [(tex_id, texture) for tex_id, texture in self.bam.object_map.items() if isinstance(texture, Texture)]
        self.textures.sort(key=lambda pair: pair[1].filename or pair[1].name)
        self.listModel = QStandardItemModel(self.listView)

        for texPair in self.textures:
            tex_id, texture = texPair
            item = QStandardItem(texture.filename or texture.name)
            item.setEditable(False)
            self.listModel.appendRow(item)

        self.listView.setModel(self.listModel)
        self.listView.selectionModel().selectionChanged.connect(self.textureSelected)

        if self.textures:
            self.openTexture(0)

    def saveBamFile(self):
        with open(self.filename, 'wb') as f:
            self.bam.write(f)

    def openTexture(self, index):
        self.index = index
        tex_id, texture = self.textures[index]

        for box in (self.textureNameBox, self.colorFilenameBox, self.alphaFilenameBox, self.colorChannelsBox, self.alphaFileChannelBox):
            box.setEnabled(True)

        self.textureNameBox.setText(texture.name)
        self.colorFilenameBox.setText(texture.filename)
        self.alphaFilenameBox.setText(texture.alpha_filename)
        self.colorChannelsBox.setText(str(texture.primary_file_num_channels))
        self.alphaFileChannelBox.setText(str(texture.alpha_file_channel))

    def textureSelected(self, selection):
        index = selection.indexes()[0].row()
        self.openTexture(index)

    def changedName(self, value):
        tex_id, texture = self.textures[self.index]
        texture.name = value

    def changedColorFilename(self, value):
        tex_id, texture = self.textures[self.index]
        texture.filename = value

    def changedAlphaFilename(self, value):
        tex_id, texture = self.textures[self.index]
        texture.alpha_filename = value

    def changedColorChannels(self, value):
        tex_id, texture = self.textures[self.index]

        try:
            texture.primary_file_num_channels = int(value)
        except:
            pass # NO I don't care right now

    def changedAlphaFileChannel(self, value):
        tex_id, texture = self.textures[self.index]

        try:
            texture.alpha_file_channel = int(value)
        except:
            pass # NO I don't care right now
