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

import base64, hashlib, hmac, urlparse, urllib
import bottle
from . import render

NEWS_SECRET_KEY_HMAC_MSG = base64.b64decode(u'rBTSl12Y5W4wsvVB') # magic

def get_news_secret_key():
    try:
        return bottle.request.environ['app.NEWS_SECRET_KEY']
    except KeyError:
        pass
    
    initial_secret_key = bottle.request.environ['app.INITIAL_SECRET_KEY']
    news_secret_key = hmac.new(
            initial_secret_key,
            NEWS_SECRET_KEY_HMAC_MSG,
            hashlib.sha256,
            ).digest()
    
    bottle.request.environ['app.NEWS_SECRET_KEY'] = news_secret_key
    return news_secret_key

def get_news_key(original_news_url):
    news_secret_key = get_news_secret_key()
    news_key = hmac.new(news_secret_key, original_news_url, hashlib.sha256).digest()
    
    return news_key[:6]

def get_news_url(original_news_url):
    o_scheme, o_netloc, o_path, o_query, o_fragment = \
            urlparse.urlsplit(original_news_url)
    
    if o_path and not o_path.startswith('/'):
        o_path = '/%s' % o_path
    
    query_kwargs = {
            'netloc': o_netloc or 'localhost',
            'key': base64.b64encode(get_news_key(original_news_url)),
            }
    
    if o_scheme and o_scheme != 'http':
        query_kwargs['scheme'] = o_scheme
    
    if o_query:
        query_kwargs['query'] = o_query
    
    if o_fragment:
        query_kwargs['fragment'] = o_fragment
    
    query = urllib.urlencode(query_kwargs)
    
    news_url = '%s://%s%s/news%s%s' % (
            bottle.request.environ.get('wsgi.url_scheme') or 'http',
            bottle.request.environ.get('HTTP_HOST') or 'localhost',
            bottle.request.environ['app.ROOT'],
            o_path,
            '?%s' % query if query else '',
            )
    
    return news_url

def news_view(path):
    o_scheme = bottle.request.params.get('scheme') or 'http'
    o_netloc = bottle.request.params.get('netloc')
    o_path = path
    o_query = bottle.request.params.get('query')
    o_fragment = bottle.request.params.get('fragment')
    news_key_b64 = bottle.request.params.get('key')
    try:
        news_key = base64.b64decode(news_key_b64)
    except (TypeError, ValueError):
        news_key = None
    
    if not o_netloc:
        raise bottle.HTTPError(404, 'News Not Found')
    
    o_url = urlparse.urlunsplit((o_scheme, o_netloc, o_path, o_query, o_fragment))
    valid_news_key = get_news_key(o_url)
    
    if not news_key or valid_news_key != news_key:
        raise bottle.HTTPError(403, 'Not a Valid News Key')
    
    bottle.response.set_header('Content-Type', 'text/plain;charset=utf-8')
    return u'o_url is <<<%r>>>\n\n%s' % (o_url, bottle.request.environ['app.NEWS_INJECTION_HTML'])

def add_route(app, root):
    app.route('%s/news' % root, callback=lambda: news_view(''))
    app.route('%s/news/' % root, callback=lambda: news_view('/'))
    app.route('%s/news/<path:path>' % root, callback=lambda path: news_view('/%s' % path))
