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

import os.path
import bottle
from mako import lookup as mako_lookup
from . import home_view, news_view

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def send_static(filename):
    return bottle.static_file(
            filename,
            root=bottle.request.settings['STATIC_DIR'],
            )

def create_app(root=None, static_root=None):
    assert root is not None
    assert static_root is not None
    
    template_lookup = mako_lookup.TemplateLookup(directories=(TEMPLATES_DIR, ))
    
    def init_settings(callback):
        def wrapper(*args, **kwargs):
            bottle.request.settings = {
                    'DEFAULT_TITLE': 'World News',
                    'DEFAULT_DESCRIPTION': 'World News',
                    'DEFAULT_KEYWORDS': 'news, world',
                    'ROOT': root,
                    'STATIC_ROOT': static_root,
                    'STATIC_DIR': STATIC_DIR,
                    'TEMPLATES_DIR': TEMPLATES_DIR,
                    'template_lookup': template_lookup,
                    }
            
            return callback(*args, **kwargs)
        return wrapper
    
    app = bottle.Bottle()
    
    app.install(init_settings)
    
    app.route('%s/<filename:path>' % static_root, callback=send_static)
    app.route('%s/' % root, callback=home_view.home_view)
    app.route('%s/<path:path>' % root, callback=news_view.news_view)
    
    return app
