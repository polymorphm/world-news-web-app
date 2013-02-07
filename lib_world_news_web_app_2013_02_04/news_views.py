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

import base64, hashlib, hmac, urlparse, urllib, re
import bottle
from . import render, html_escape, cached_fetch

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

def fetch_data_content_type(fetch_data):
    return fetch_data['headers'].get('content-type')

def fetch_data_is_html(fetch_data):
    ct = fetch_data_content_type(fetch_data)
    
    if ct is None:
        return False
    
    if ct == 'text/html' or ct.startswith('text/html;'):
        return True
    
    return False

def news_injection_proc(original_news_url, fetch_data):
    if not fetch_data_is_html(fetch_data):
        return
    
    inj = bottle.request.environ['app.NEWS_INJECTION_HTML']
    
    def delete_base(content):
        def repl(m):
            return '%s%s%s' % (
                    m.group('prefix'),
                    'DISABLED__%s' % m.group('tag_name'),
                    m.group('postfix'),
                    )
        
        return re.sub(r'(?P<prefix>\<)(?P<tag_name>base)(?P<postfix>(\s.*?)?(\/\>|\>))',
                repl, content, flags=re.S | re.I)
    
    def replace_url(content):
        def repl(m):
            o_url = urlparse.urljoin(original_news_url, html_escape.html_unescape(m.group('url')))
            
            news_url = get_news_url(o_url)
            
            if isinstance(news_url, unicode):
                news_url = news_url.encode('utf-8', 'replace')
            
            return '%s%s%s' % (
                    m.group('prefix'),
                    html_escape.html_escape(news_url),
                    m.group('postfix'),
                    )
        
        return re.sub(r'(?P<prefix>href\s*?\=\s*?(?P<q>\"|\x27))(?P<url>.+?)(?P<postfix>\x22)',
                repl, content, flags=re.S | re.I)
    
    def insert_base(content):
        def repl(m):
            return '%s%s' % (
                    m.group('tag'),
                    '<base href="%s" />' % html_escape.html_escape(original_news_url),
                    )
        
        return re.sub(r'(?P<tag>\<head(\s.*?)?(\/\>|\>))',
                repl, content, count=1, flags=re.S | re.I)
    
    def insert_inj(content):
        def repl(m):
            return '%s%s' % (
                    inj.encode('utf-8', 'replace'),
                    m.group(0),
                    )
        
        return re.sub(r'(?P<tag>\</body(\s.*?)?(\/\>|\>))',
                repl, content, count=1, flags=re.S | re.I)
    
    fetch_data['content'] = delete_base(fetch_data['content'])
    fetch_data['content'] = replace_url(fetch_data['content'])
    fetch_data['content'] = insert_base(fetch_data['content'])
    fetch_data['content'] = insert_inj(fetch_data['content'])

def news_injection_cache_ns():
    hmac_key = base64.b64decode(u'dGCSLyFIaOOHzITh') # magic
    hmac_msg = bottle.request.environ['app.NEWS_INJECTION_HTML']
    
    cache_ns = base64.b64encode(
            hmac.new(
                    hmac_key,
                    hmac_msg,
                    hashlib.sha256,
                    ).digest(),
            )
    
    return cache_ns

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
        raise bottle.HTTPError(404, 'News Not Found (no netloc)')
    
    o_url = urlparse.urlunsplit((o_scheme, o_netloc, o_path, o_query, o_fragment))
    valid_news_key = get_news_key(o_url)
    
    if not news_key or valid_news_key != news_key:
        raise bottle.HTTPError(403, 'Not a Valid News Key')
    
    fetch_data = cached_fetch.cached_fetch(
            o_url,
            proc_func=lambda cached_fetch: news_injection_proc(o_url, cached_fetch),
            cache_namespace=news_injection_cache_ns()
            )
    
    if fetch_data is None:
        raise bottle.HTTPError(404, 'News Not Found (no data)')
    
    if not fetch_data_is_html(fetch_data):
        bottle.redirect(o_url, code=301)
    
    content_type = fetch_data_content_type(fetch_data)
    content = fetch_data['content']
    
    bottle.response.set_header('Content-Type', content_type)
    return content

def add_route(app, root):
    app.route('%s/news' % root, callback=lambda: news_view(''))
    app.route('%s/news/' % root, callback=lambda: news_view('/'))
    app.route('%s/news/<path:path>' % root, callback=lambda path: news_view('/%s' % path))
