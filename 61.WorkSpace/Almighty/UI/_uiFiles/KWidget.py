from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys

pgm_id = None

class KWidget() :
    pgm_id = None

    def __init__(self):
        self.setupUi(self)
        self.pgm_id = pgm_id

