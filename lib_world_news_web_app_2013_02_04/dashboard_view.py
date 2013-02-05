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

import bottle
from google.appengine.api import users
from . import render

def dashboard_login_redirect():
    login_url = users.create_login_url(dest_url='%s/dashboard' % bottle.request.environ['app.ROOT'])
    
    bottle.redirect(login_url)

def home_view():
    dashboard_login_redirect()

def dashboard_view():
    user = users.get_current_user()
    if user is None:
        dashboard_login_redirect()
    user_email = user.email()
    
    return render.render(
            'dashboard.mako',
            dashboard__title=bottle.request.environ['app.DEFAULT_TITLE'],
            dashboard__description=bottle.request.environ['app.DEFAULT_DESCRIPTION'],
            dashboard__keywords=bottle.request.environ['app.DEFAULT_KEYWORDS'],
            dashboard__user_email=user_email,
            )
