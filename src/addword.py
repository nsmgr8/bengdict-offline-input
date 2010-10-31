# -*- coding: utf-8 -*-

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

from PyQt4.QtGui import (QDialog, QPushButton, QLabel, QLineEdit, QComboBox,
                         QVBoxLayout, QHBoxLayout, QTextEdit, QMessageBox)
from PyQt4.QtCore import SIGNAL

from db.bangladict.models import Dictionary, Word

class AddWordWidget(QDialog):

    def __init__(self, parent=None):
        super(AddWordWidget, self).__init__(parent=parent)
        self.setWindowTitle('Add word')

        self.create_layout()
        self.create_connections()

    def create_layout(self):
        hbox = QHBoxLayout()

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Dictionary"))
        vbox.addWidget(QLabel("Original"))
        vbox.addWidget(QLabel("Translation"))
        vbox.addWidget(QLabel("Phoneme"))
        vbox.addWidget(QLabel("Parts of Speech"))
        vbox.addWidget(QLabel("Synonyms"))
        vbox.addWidget(QLabel("Antonyms"))
        hbox.addLayout(vbox)

        vbox = QVBoxLayout()

        self.dictionaries = Dictionary.objects.all()
        self.dictionary = QComboBox()
        self.dictionary.addItems([d.name for d in self.dictionaries])
        vbox.addWidget(self.dictionary)

        self.original = QLineEdit()
        vbox.addWidget(self.original)

        self.translation = QLineEdit()
        vbox.addWidget(self.translation)

        self.phoneme = QLineEdit()
        vbox.addWidget(self.phoneme)

        self.pos = QComboBox()
        self.pos.addItems([p.strip() for p in
                           self.dictionaries[0].pos.split(',') if len(p) > 0])
        vbox.addWidget(self.pos)

        self.synonyms = QLineEdit()
        vbox.addWidget(self.synonyms)

        self.antonyms = QLineEdit()
        vbox.addWidget(self.antonyms)

        hbox.addLayout(vbox)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        vbox.addWidget(QLabel("Description"))
        self.description = QTextEdit()
        vbox.addWidget(self.description)

        self.add_button = QPushButton("&Add")
        self.close_button = QPushButton("&Close")
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.add_button)
        hbox.addWidget(self.close_button)
        vbox.addLayout(hbox)

        self.status = QLabel()
        vbox.addWidget(self.status)

        self.setLayout(vbox)

    def create_connections(self):
        self.connect(self.dictionary, SIGNAL("currentIndexChanged(int)"),
                     self.change_pos)
        self.connect(self.close_button, SIGNAL("clicked()"), self.close)
        self.connect(self.add_button, SIGNAL("clicked()"), self.add_word)

    def change_pos(self, index):
        current_dict = self.dictionaries[index]
        self.pos.clear()
        self.pos.addItems([p.strip() for p in
                           current_dict.pos.split(',') if len(p) > 0])

    def get_texts(self):
        current_dict = self.dictionaries[self.dictionary.currentIndex()].abbrev
        original = unicode(self.original.text()).strip()
        translation = unicode(self.translation.text()).strip()
        phoneme = unicode(self.phoneme.text()).strip()
        pos = unicode(self.pos.currentText()).strip()
        synonyms = unicode(self.synonyms.text()).strip()
        antonyms = unicode(self.antonyms.text()).strip()
        description = unicode(self.description.toPlainText()).strip()

        if not all([original, translation, pos]):
            self.status.setText('There was an error inserting the word. Please'
                                ' try again.')
            QMessageBox.critical(self, "Error", "You must enter at least "
                                 "'Original', 'Translation' and 'Parts of "
                                 "Speech'.")
            return None

        return dict(dictionary=current_dict, original=original,
                    translation=translation, phoneme=phoneme, pos=pos,
                    synonyms=synonyms, antonyms=antonyms,
                    description=description)

    def clear_texts(self):
        self.translation.clear()
        self.phoneme.clear()
        self.synonyms.clear()
        self.antonyms.clear()
        self.description.clear()

        self.original.setFocus()

    def add_word(self):
        self.status.clear()

        texts = self.get_texts()
        if not texts:
            return

        word = Word(**texts)
        word.save()

        self.clear_texts()
        self.status.setText('Word %s has been added successfully.' %
                            word.original)

    def save_word(self):
        self.status.clear()

        texts = self.get_texts()
        if not texts:
            return

        word = self.word
        word.dictionary = texts['dictionary']
        word.original = texts['original']
        word.translation = texts['translation']
        word.phoneme = texts['phoneme']
        word.pos = texts['pos']
        word.synonyms = texts['synonyms']
        word.antonyms = texts['antonyms']
        word.description = texts['description']
        word.save()

        self.status.setText('Word %s has been saved successfully' %
                            word.original)

    def get_word(self):
        return self._word

    def set_word(self, word):
        self._word = word
        self.setWindowTitle("Edit %s" % word.original)
        self.add_button.setText("&Save")
        self.disconnect(self.add_button, SIGNAL("clicked()"), self.add_word)

        if word.exported:
            self.add_button.setEnabled(False)
            self.status.setText('This word has been exported already. '
                                'You cannot save the changes to it.')
        else:
            self.connect(self.add_button, SIGNAL("clicked()"), self.save_word)

        for i, d in enumerate(self.dictionaries):
            if d.abbrev == word.dictionary:
                self.dictionary.setCurrentIndex(i)
                break

        self.original.setText(word.original)
        self.translation.setText(word. translation)
        self.phoneme.setText(word.phoneme)
        self.synonyms.setText(word.synonyms)
        self.antonyms.setText(word.antonyms)
        self.description.setText(word.description)

        for i in range(self.pos.count()):
            if self.pos.itemText(i) == word.pos:
                self.pos.setCurrentIndex(i)
                break

    word = property(get_word, set_word)

