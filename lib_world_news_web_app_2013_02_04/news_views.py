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

import base64, hashlib, hmac
import bottle
from . import render

NEWS_SECRET_KEY_HMAC_MSG = base64.b64decode(u'rBTSl12Y5W4wsvVB')

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
    
    return news_key

def news_view(path):
    # TEST TEST TEST
    assert 2 > 9
    return u'фигня, %r!! [bottle.request.environ is %r]' % (path, bottle.request.environ)
