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

from google.appengine.api import users
import bottle

def dashboard_login_redirect():
    login_url = users.create_login_url(dest_url='%s/dashboard' % bottle.request.environ['app.ROOT'])
    
    bottle.redirect(login_url)

def logout_redirect():
    logout_url = users.create_logout_url(dest_url='%s/' % bottle.request.environ['app.ROOT'])
    
    bottle.redirect(logout_url)

def check_user():
    user = users.get_current_user()
    
    if user is None:
        dashboard_login_redirect()
    
    user_email = user.email()
    
    if user_email not in bottle.request.environ['app.ALLOW_ACCESS_LIST']:
        bottle.redirect('%s/denied' % bottle.request.environ['app.ROOT'])
    
    return user_email

def check_user_for_ajax():
    if not bottle.request.is_xhr:
        raise bottle.HTTPError(403)
    
    user = users.get_current_user()
    
    if user is None:
        raise bottle.HTTPError(403)
    
    user_email = user.email()
    
    if user_email not in bottle.request.environ['app.ALLOW_ACCESS_LIST']:
        raise bottle.HTTPError(403)
    
    return user_email

def add_route(app, root):
    app.route('%s/login' % root, callback=dashboard_login_redirect)
    app.route('%s/logout' % root, callback=logout_redirect)
