#
# Copyright 2010 BengDict Project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import datetime

from PyQt4.QtGui import (QMainWindow, QAction, QApplication, QMessageBox)
from PyQt4.QtCore import SIGNAL, SLOT

from django.core import serializers

from words import WordsWidget
from addword import AddWordWidget

from db.bangladict.models import Word

class Window(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('Bangla Dictionary')

        self.create_layout()
        self.create_actions()
        self.create_menus()
        self.create_connections()

    def create_layout(self):
        self.words_widget = WordsWidget()
        self.setCentralWidget(self.words_widget)
        self.words_widget.show()

    def create_actions(self):
        self.new_action = QAction("&New", self)
        self.export_action = QAction("&Export", self)
        self.quit_action = QAction("&Quit", self)

    def create_menus(self):
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.export_action)
        file_menu.addAction(self.quit_action)

    def create_connections(self):
        self.connect(self.new_action, SIGNAL("triggered()"), self.new_word)
        self.connect(self.export_action, SIGNAL("triggered()"),
                     self.export_words)
        self.connect(self.quit_action, SIGNAL("triggered()"),
                     QApplication.instance(), SLOT("closeAllWindows()"))

    def new_word(self):
        add = AddWordWidget(self)
        add.words_widget = self.words_widget
        add.show()

    def export_words(self):
        words = Word.objects.filter(exported=False)
        if words.count() == 0:
            QMessageBox.information(self, 'BengDict',
                                    'No word found to be exported')
            return

        json_str = serializers.serialize("json", words, fields=['dictionary',
                                                                'original',
                                                                'translation',
                                                                'phoneme',
                                                                'pos',
                                                                'description',
                                                                'synonyms',
                                                                'antonyms', ])

        try:
            root_dir = os.path.dirname(os.path.dirname(__file__))
            exports_dir = os.path.join(root_dir, 'exports')
            os.mkdir(exports_dir)
        except OSError:
            pass

        time_format = datetime.datetime.now().isoformat().replace(':', '-')
        fname = os.path.join(exports_dir, 'export-' + time_format + '.json')

        with open(fname, 'w') as f:
            f.write(json_str)

        for word in words:
            word.exported = True
            word.save()

        self.words_widget.load_words()
        QMessageBox.information(self, 'BengDict',
                                'The exported file is saved in ' + fname)

