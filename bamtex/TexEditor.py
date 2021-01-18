from PyQt5.QtWidgets import QApplication
from p3bamboo.BamFactory import BamFactory
from .Texture import Texture
from .MainWidget import MainWidget
import sys

class TexEditor(object):

    def __init__(self):
        self.app = QApplication(sys.argv)

    def run(self):
        self.main = MainWidget(self)
        self.main.resize(1200, 400)
        self.main.show()
        BamFactory.register_type('Texture', Texture)
        self.app.exec_()
