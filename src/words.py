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

from PyQt4.QtGui import (QWidget, QTableWidget, QPushButton, QVBoxLayout,
                         QHBoxLayout, QComboBox, QTableWidgetItem, QLabel)
from PyQt4.QtCore import Qt, SIGNAL

from django.core.paginator import Paginator, InvalidPage

from addword import AddWordWidget
from db.bangladict.models import Dictionary, Word

class WordsWidget(QWidget):

    def __init__(self):
        super(WordsWidget, self).__init__()

        self.page_number = 1
        self.row = 20

        self.create_layout()
        self.create_connections()
        self.load_words()

    def create_layout(self):
        self.words_table = QTableWidget(0, 8)

        self.dictionaries = Dictionary.objects.all()
        self.dict_combo = QComboBox()
        self.dict_combo.addItems([d.name for d in self.dictionaries])

        self.refresh_button = QPushButton("Refresh")
        self.next_button = QPushButton("Next")
        self.previous_button = QPushButton("Previous")

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('Dictionary'))
        hbox.addWidget(self.dict_combo)
        hbox.addWidget(self.refresh_button)
        hbox.addStretch()
        hbox.addWidget(self.previous_button)
        hbox.addWidget(self.next_button)

        vbox = QVBoxLayout()
        vbox.addWidget(self.words_table)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def create_connections(self):
        self.connect(self.dict_combo, SIGNAL("currentIndexChanged(int)"),
                     self.change_dictionary)
        self.connect(self.refresh_button, SIGNAL("clicked()"), self.load_words)
        self.connect(self.next_button, SIGNAL("clicked()"), self.next_words)
        self.connect(self.previous_button, SIGNAL("clicked()"),
                     self.previous_words)
        self.connect(self.words_table,
                     SIGNAL("itemDoubleClicked(QTableWidgetItem*)"),
                     self.edit_word)

    def next_words(self):
        self.page_number += 1
        self.load_words()

    def previous_words(self):
        self.page_number -= 1
        self.load_words()

    def change_dictionary(self):
        self.page_number = 1
        self.load_words()

    def load_words(self):
        dictionary = self.dictionaries[self.dict_combo.currentIndex()]
        words = Word.objects.filter(dictionary=dictionary.abbrev) \
                    .order_by('original')
        paginator = Paginator(words, self.row, allow_empty_first_page=True)
        try:
            page_obj = paginator.page(self.page_number)
        except InvalidPage:
            return

        self.words_table.clear()
        self.words_table.setRowCount(len(page_obj.object_list))

        self.words_table.setHorizontalHeaderLabels(['Original',
                                                    'Translation',
                                                    'Parts of Speech',
                                                    'Phoneme',
                                                    'Synonyms',
                                                    'Antonyms',
                                                    'Added at',
                                                    'Status'
                                                   ])

        for i, word in enumerate(page_obj.object_list):
            for j, cell in enumerate([word.original, word.translation, word.pos,
                                     word.phoneme, word.synonyms, word.antonyms,
                                     word.added_at.strftime("%Y-%m-%d %H:%M"),
                                      "exported" if word.exported else "new"]):
                item = QTableWidgetItem(cell)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.words_table.setItem(i, j, item)

        self.next_button.setEnabled(page_obj.has_next())
        self.previous_button.setEnabled(page_obj.has_previous())

    def edit_word(self):
        index = self.words_table.currentRow() + self.row * (self.page_number - 1)
        dictionary = self.dictionaries[self.dict_combo.currentIndex()]
        word = Word.objects.filter(dictionary=dictionary.abbrev) \
                    .order_by('original')[index]
        edit_word = AddWordWidget(self)
        edit_word.word = word
        edit_word.show()

