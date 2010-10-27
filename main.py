#!/usr/bin/env python

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

import subprocess
import sys
import os
from time import sleep

from PyQt4.Qt import QApplication
from PyQt4.QtGui import QPushButton

from django.conf import settings
import src.db.settings as my_settings
settings.configure(
    DATABASE_ENGINE=my_settings.DATABASE_ENGINE,
    DATABASE_NAME=my_settings.DATABASE_NAME,
    INSTALLED_APPS=my_settings.INSTALLED_APPS
)

from src.window import Window

if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    if subprocess.check_call(['python', dirname + '/src/db/manage.py',
                              'syncdb']) != 0:
        print "Could not create the database."
        sys.exit(-1)

    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec_())

