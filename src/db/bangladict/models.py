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

from django.db import models

class Dictionary(models.Model):
    name = models.CharField(max_length=200)
    abbrev = models.CharField(max_length=10)
    pos = models.TextField(verbose_name='Parts of Speech')

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.abbrev)

class Word(models.Model):
    dictionary = models.CharField(max_length=10)
    original = models.CharField(max_length=50)
    translation = models.CharField(max_length=50)
    phoneme = models.CharField(max_length=70, blank=True)
    pos = models.CharField(max_length=50, verbose_name='Parts of Speech')
    description = models.TextField(blank=True)
    synonyms = models.CharField(max_length=500, blank=True)
    antonyms = models.CharField(max_length=500, blank=True)
    exported = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s -> %s' % (self.original, self.translation)

