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

import base64, json
import bottle
from google.appengine.api import users
from . import access, render, sh_views, news_views

def denied_view():
    bottle.response.status = 403
    
    user = users.get_current_user()
    if user is not None:
        user_email = user.email()
    else:
        user_email = None
    
    return render.render(
            'denied.mako',
            denied__user_email=user_email,
            )

def dashboard_view():
    user_email = access.check_user()
    
    news_secret_key = news_views.get_news_secret_key()
    news_secret_key_b64 = base64.b64encode(news_secret_key)
    key_example_for = lambda url: base64.b64encode(news_views.get_news_key(url))
    
    return render.render(
            'dashboard.mako',
            dashboard__user_email=user_email,
            dashboard__news_secret_key_b64=news_secret_key_b64,
            dashboard__key_example_for=key_example_for,
            )

def get_news_url_info_ajax():
    access.check_user_for_ajax()
    
    o_url = unicode(bottle.request.json.get('original_news_url'))
    news_url = news_views.get_news_url(o_url)
    news_key = base64.b64encode(news_views.get_news_key(o_url))
    
    micro_news_url = sh_views.new_micro_news_url(o_url)
    
    bottle.response.set_header('Content-Type', 'application/json;charset=utf-8')
    return json.dumps({
            'news_url': news_url,
            'micro_news_url': micro_news_url,
            'news_key': news_key,
            })

def add_route(app, root):
    app.post('%s/ajax/get-news-url-info' % root, callback=get_news_url_info_ajax)
    app.route('%s/' % root, callback=access.dashboard_login_redirect)
    app.route('%s/denied' % root, callback=denied_view)
    app.route('%s/dashboard' % root, callback=dashboard_view)
