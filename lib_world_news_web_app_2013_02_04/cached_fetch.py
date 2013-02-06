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

FETCH_DATA_MEMCACHE_NS = 'KCwgwkO1GubMHh9t' # magic

class CacheFetchError(Exception):
    pass

def cached_fetch(url, proc_func=None):
    fetch_data_key = hashlib.sha256(url).hexdigest()
    fetch_data = memcache.get(fetch_data_key, namespace=FETCH_DATA_MEMCACHE_NS)
    
    if fetch_data is not None:
        return fetch_data
    
    try:
        fetch_client = urlfetch.fetch(url, validate_certificate=True)
    except Exception as e:
        raise CacheFetchError('%r: %s' % (type(e), e))
    if fetch_client.status_code != 200:
        raise CacheFetchError('status_code != 200')
    
    fetch_data = {
            'fetch_time': time.time(),
            'final_url': fetch_client.final_url,
            'status_code': fetch_client.status_code,
            'content': fetch_client.content,
            'headers': fetch_client.headers,
            }
    
    if proc_func is not None:
        proc_func(fetch_data)
    
    memcache.add(fetch_data_key, fetch_data, namespace=FETCH_DATA_MEMCACHE_NS)
    
    return fetch_data
