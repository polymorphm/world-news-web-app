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

import hashlib, time
from google.appengine.api import memcache, urlfetch

FETCH_DATA_BY_URL_MEMCACHE_NS = 'P7gznlyTXa6CNCWZ' # magic
FAIL_CACHING_TIME = 300

def cached_fetch(url, proc_func=None, cache_namespace=None):
    assert proc_func is None or cache_namespace is not None
    
    if cache_namespace is None:
        cache_namespace = FETCH_DATA_BY_URL_MEMCACHE_NS
    
    fetch_data_key = hashlib.sha256(url).hexdigest()
    fetch_data = memcache.get(fetch_data_key, namespace=cache_namespace)
    
    if fetch_data is not None:
        return fetch_data
    
    try:
        resp = urlfetch.fetch(url, validate_certificate=True)
    except:
        resp = None
    if resp is not None and resp.status_code != 200:
        resp = None
    
    if resp is None:
        memcache.add(fetch_data_key, None, time=FAIL_CACHING_TIME, namespace=cache_namespace)
        return
    
    fetch_data = {
            'url': url,
            'fetch_time': time.time(),
            'final_url': resp.final_url or url,
            'status_code': resp.status_code,
            'content': resp.content,
            'headers': resp.headers,
            }
    
    if proc_func is not None:
        proc_func(fetch_data)
    
    memcache.add(fetch_data_key, fetch_data, namespace=cache_namespace)
    
    return fetch_data
