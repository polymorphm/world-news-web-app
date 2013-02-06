#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
#
# Copyright 2013 Andrej A Antonov <polymorphm@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
assert unicode is not str
assert str is bytes

import sys, os.path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'site-packages'))

from wsgiref import simple_server
from lib_world_news_web_app_2013_02_04.app import create_app

app = create_app(
        root='',
        static_root='/static',
        config_file=os.path.join(os.path.dirname(__file__), 'world-news.cfg'),
        )
