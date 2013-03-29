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

import random, base64, json, urllib
import bottle
from google.appengine.ext import ndb
from google.appengine.api import memcache
from . import news_views

SH_ENTITY_KIND_NS = 'bjE4fVnYcryOs3Ro' # magic
USE_MEMCACHE = True

if USE_MEMCACHE:
    SH_O_URL_BY_NAME_MEMCACHE_NS = 's8m6LBqjDkoVZCAk' # magic

class ShEntity(ndb.Model):
    sh_name = ndb.StringProperty()
    o_url = ndb.StringProperty()
    
    @classmethod
    def _get_kind(cls):
        return '%s__%s' % (cls.__name__, SH_ENTITY_KIND_NS)

def new_sh_name(o_url):
    assert isinstance(o_url, unicode)
    
    for other_sh in ShEntity.query(ShEntity.o_url == o_url).fetch(1):
        sh_name = other_sh.sh_name
        
        return sh_name
    
    SH_NAME_CH_TABLE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    sh_name = ''
    for ch in xrange(6):
        sh_name = '%s%s' % (sh_name, random.choice(SH_NAME_CH_TABLE))
    sh = ShEntity(sh_name=sh_name, o_url=o_url)
    sh.put()
    
    while True:
        for other_sh in ShEntity.query(
                ShEntity.sh_name == sh_name,
                ShEntity.o_url != o_url,
                ).fetch(1):
            break
        else:
            break
        
        for ch in xrange(2):
            sh_name = '%s%s' % (sh_name, random.choice(SH_NAME_CH_TABLE))
        
        sh.sh_name = sh_name
        sh.put()
    
    if USE_MEMCACHE:
        memcache.add(sh_name, o_url, namespace=SH_O_URL_BY_NAME_MEMCACHE_NS)
    
    return sh_name

def new_micro_news_url(o_url):
    sh_name = new_sh_name(o_url)
    micro_news_url = '%s://%s%s/sh/%s' % (
            bottle.request.environ.get('wsgi.url_scheme') or 'http',
            bottle.request.environ.get('HTTP_HOST') or 'localhost',
            bottle.request.environ['app.ROOT'],
            urllib.quote_plus(sh_name),
            )
    
    return micro_news_url

def api_sh_new_view():
    if bottle.request.json is None:
        raise bottle.HTTPError(403)
        return
    
    o_url = unicode(bottle.request.json.get('original_news_url'))
    news_key_b64 = unicode(bottle.request.json.get('news_key'))
    
    try:
        news_key = base64.b64decode(news_key_b64)
    except ValueError:
        news_key = None
    valid_news_key = news_views.get_news_key(o_url)
    
    if valid_news_key != news_key:
        raise bottle.HTTPError(403, 'Not a Valid News Key')
    
    micro_news_url = new_micro_news_url(o_url)
    
    bottle.response.set_header('Content-Type', 'application/json;charset=utf-8')
    return json.dumps({
            'micro_news_url': micro_news_url,
            })

def sh_view(sh_name):
    if not isinstance(sh_name, unicode):
        sh_name = sh_name.decode('utf-8', 'replace')
    
    def do_redirect(o_url):
        news_url = news_views.get_news_url(o_url)
        
        bottle.redirect(news_url, code=301)
    
    if USE_MEMCACHE:
        o_url = memcache.get(sh_name, namespace=SH_O_URL_BY_NAME_MEMCACHE_NS)
        
        if o_url is not None:
            do_redirect(o_url)
    
    for sh in ShEntity.query(ShEntity.sh_name == sh_name).fetch(1):
        o_url = sh.o_url
        
        if USE_MEMCACHE:
            memcache.add(sh_name, o_url, namespace=SH_O_URL_BY_NAME_MEMCACHE_NS)
        
        do_redirect(o_url)
    
    raise bottle.HTTPError(404, 'Page Not Found')

def add_route(app, root):
    app.post('%s/api/sh/new' % root, callback=api_sh_new_view)
    app.route('%s/sh/<sh_name>' % root, callback=sh_view)
