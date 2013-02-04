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

def render(tpl_name, **kwargs):
    template = bottle.request.settings['template_lookup'].get_template(tpl_name)
    tpl_kwargs = {
            'request': bottle.request,
            }
    tpl_kwargs.update(kwargs)
    
    bottle.response.set_header('Content-Type', 'text/html;charset=utf-8')
    bottle.response.set_header('X-Frame-Options', 'SAMEORIGIN')
    bottle.response.set_header('X-Ua-Compatible', 'chrome=1')
    
    return template.render(**tpl_kwargs)
