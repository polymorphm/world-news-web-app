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

import base64
import bottle
from google.appengine.api import users
from . import render, news_views

def dashboard_login_redirect():
    login_url = users.create_login_url(dest_url='%s/dashboard' % bottle.request.environ['app.ROOT'])
    
    bottle.redirect(login_url)

def logout_redirect():
    logout_url = users.create_logout_url(dest_url='%s/' % bottle.request.environ['app.ROOT'])
    
    bottle.redirect(logout_url)

def denied_view():
    bottle.response.status = 403
    
    user = users.get_current_user()
    if user is not None:
        user_email = user.email()
    else:
        user_email = None
    
    return render.render(
            'denied.mako',
            denied__title='Access Denied',
            denied__user_email=user_email,
            )

def check_user():
    user = users.get_current_user()
    
    if user is None:
        dashboard_login_redirect()
    
    user_email = user.email()
    
    if user_email not in bottle.request.environ['app.ALLOW_ACCESS_LIST']:
        bottle.redirect('%s/denied' % bottle.request.environ['app.ROOT'])
    
    return user_email

def check_user_for_ajax():
    if bottle.request.get_header('X-Requested-With') != 'XMLHttpRequest':
        raise bottle.HTTPError(403)
    
    user = users.get_current_user()
    
    if user is None:
        raise bottle.HTTPError(403)
    
    user_email = user.email()
    
    if user_email not in bottle.request.environ['app.ALLOW_ACCESS_LIST']:
        raise bottle.HTTPError(403)
    
    return user_email

def dashboard_view():
    user_email = check_user()
    
    news_secret_key = news_views.get_news_secret_key()
    news_secret_key_b64 = base64.b64encode(news_secret_key)
    key_example_for = lambda url: base64.b64encode(news_views.get_news_key(url))
    
    return render.render(
            'dashboard.mako',
            dashboard__title=bottle.request.environ['app.DEFAULT_TITLE'],
            dashboard__description=bottle.request.environ['app.DEFAULT_DESCRIPTION'],
            dashboard__keywords=bottle.request.environ['app.DEFAULT_KEYWORDS'],
            dashboard__user_email=user_email,
            dashboard__news_secret_key_b64=news_secret_key_b64,
            dashboard__key_example_for=key_example_for,
            )

def get_news_url_ajax():
    check_user_for_ajax()
    
    return '123123123123123'

def add_route(app, root):
    app.route('%s/' % root, callback=dashboard_login_redirect)
    app.route('%s/login' % root, callback=dashboard_login_redirect)
    app.route('%s/logout' % root, callback=logout_redirect)
    app.route('%s/denied' % root, callback=denied_view)
    app.route('%s/dashboard' % root, callback=dashboard_view)
    
    app.post('%s/ajax/get-news-url' % root, callback=get_news_url_ajax)
