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

import os.path, ConfigParser, base64
import bottle
from mako import lookup as mako_lookup
from . import access, dashboard_views, news_views

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def static_view(filename):
    return bottle.static_file(
            filename,
            root=bottle.request.environ['app.STATIC_DIR'],
            )

def favicon_view():
    bottle.redirect(bottle.request.environ['app.FAVICON'])

class Config(object):
    pass

def get_config_allow_list(conf_parser, config_file):
    if conf_parser.has_option('core', 'allow_access_list'):
        allow_access_list = \
                conf_parser.get('core', 'allow_access_list').decode('utf-8', 'replace')
    else:
        allow_access_list = u''
    
    allow_access_list = tuple(x.strip() for x in allow_access_list.split(','))
    
    return allow_access_list

def get_config_initial_secret_key(conf_parser, config_file):
    initial_secret_key = conf_parser.get('core', 'initial_secret_key').decode('utf-8', 'replace')
    
    initial_secret_key = base64.b64decode(initial_secret_key)
    
    return initial_secret_key

def get_news_injection_html(conf_parser, config_file):
    if not conf_parser.has_option('core', 'news_injection_file'):
        return u''
    
    news_injection_file = \
            conf_parser.get('core', 'news_injection_file').decode('utf-8', 'replace')
    
    news_injection_file = os.path.join(
            os.path.dirname(config_file),
            news_injection_file,
            )
    
    with open(news_injection_file, 'rb') as fd:
        news_injection_html = fd.read().decode('utf-8', 'replace')
    
    return news_injection_html

def create_app(root=None, static_root=None, config_file=None):
    assert root is not None
    assert static_root is not None
    assert config_file is not None
    
    conf_parser = ConfigParser.SafeConfigParser()
    conf_parser.read(config_file)
    
    allow_access_list = get_config_allow_list(conf_parser, config_file)
    initial_secret_key = get_config_initial_secret_key(conf_parser, config_file)
    news_injection_html = get_news_injection_html(conf_parser, config_file)
    
    template_lookup = mako_lookup.TemplateLookup(directories=(TEMPLATES_DIR, ))
    
    def init_settings():
        bottle.request.environ.update({
                'app.ROOT': root,
                'app.STATIC_ROOT': static_root,
                'app.ALLOW_ACCESS_LIST': allow_access_list,
                'app.INITIAL_SECRET_KEY': initial_secret_key,
                'app.NEWS_INJECTION_HTML': news_injection_html,
                })
        
        bottle.request.environ.update({
                'app.STATIC_DIR': STATIC_DIR,
                'app.TEMPLATES_DIR': TEMPLATES_DIR,
                'app.template_lookup': template_lookup,
                'app.DEFAULT_TITLE': u'World News',
                'app.DEFAULT_DESCRIPTION': u'World News',
                'app.DEFAULT_KEYWORDS': u'news, world',
                'app.FAVICON': '%s/favicon.png' % bottle.request.environ['app.STATIC_ROOT'],
                })
    
    app = bottle.Bottle()
    
    app.hooks.add('before_request', init_settings)
    
    app.route('%s/<filename:path>' % static_root, callback=static_view)
    app.route('%s/favicon.ico' % root, callback=favicon_view)
    
    access.add_route(app, root)
    dashboard_views.add_route(app, root)
    news_views.add_route(app, root)
    
    return app
