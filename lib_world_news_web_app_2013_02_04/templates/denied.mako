# -*- mode: html; coding: utf-8 -*-
<!DOCTYPE html>

<html>
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="X-Frame-Options" content="SAMEORIGIN" />
        <meta http-equiv="X-Ua-Compatible" content="chrome=1" />
        <script src="${request.environ['app.STATIC_ROOT'] | h}/js/google_chrome_frame_for_microsoft_ie.js"></script>
        <title>${denied__title | h}</title>
        <link rel="shortcut icon" href="${request.environ['app.FAVICON'] | h}" />
        <link rel="stylesheet" href="${request.environ['app.STATIC_ROOT'] | h}/css/default.css" />
        <meta name="app_default_title" content="${request.environ['app.DEFAULT_TITLE'] | h}" />
        <meta name="app_root" content="${request.environ['app.ROOT'] | h}" />
        <meta name="app_static_root" content="${request.environ['app.STATIC_ROOT'] | h}" />
    </head>
    <body>
        <div class="page">
            <h1>Access Denied</h1>
            % if denied__user_email is not None:
            <p>Logged as <b>${denied__user_email | h}</b></p>
            <p><a href="${'%s/logout' % request.environ['app.ROOT'] | h}">Logout</a></p>
            % else:
            <p><a href="${'%s/login' % request.environ['app.ROOT'] | h}">Login</a></p>
            % endif
        </div>
    </body>
</html>
