# -*- mode: html; coding: utf-8 -*-
<!DOCTYPE html>

<html>
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="X-Frame-Options" content="SAMEORIGIN" />
        <meta http-equiv="X-Ua-Compatible" content="chrome=1" />
        <script src="${request.environ['app.STATIC_ROOT'] | h}/js/google_chrome_frame_for_microsoft_ie.js"></script>
        <title>${dashboard__title | h}</title>
        <link rel="shortcut icon" href="${request.environ['app.FAVICON'] | h}" />
        <link rel="stylesheet" href="${request.environ['app.STATIC_ROOT'] | h}/css/default.css" />
        <meta name="keywords" content="${dashboard__keywords | h}" />
        <meta name="description" content="${dashboard__description | h}" />
        <meta name="app_default_title" content="${request.environ['app.DEFAULT_TITLE'] | h}" />
        <meta name="app_root" content="${request.environ['app.ROOT'] | h}" />
        <meta name="app_static_root" content="${request.environ['app.STATIC_ROOT'] | h}" />
    </head>
    <body>
        <div class="page">
            <h1>Welcome to ${request.environ['app.DEFAULT_TITLE'] | h}!</h1>
            <p><a href="${'%s/logout' % request.environ['app.ROOT'] | h}">Logout</a></p>
            <pre>user_email is <b>${dashboard__user_email | h}</b></pre>
            <pre>base64(news_secret_key) is <b>${dashboard__news_secret_key_b64 | h}</b></pre>
            <pre><b>news_key = hmap_sha256( news_secret_key , original_news_url )</b></pre>
            <pre>Example for "http://ya.ru/":</pre>
            <div style="margin-left: 4em; font-size: 0.7em">
                <pre>base64(example_news_key) = hmap_sha256( base64_decode("${dashboard__news_secret_key_b64 | h}"), "http://ya.ru/")</pre>
                <pre>base64(example_news_key) = "${dashboard__key_example_for('http://ya.ru/') | h}"</pre>
            </div>
        </div>
    </body>
</html>
