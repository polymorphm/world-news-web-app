# -*- mode: html; coding: utf-8 -*-
<!DOCTYPE html>

<html>
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="X-Frame-Options" content="DENY" />
        <meta http-equiv="X-Ua-Compatible" content="chrome=1" />
        <script src="${request.environ['app.STATIC_ROOT'] | h}/js/google_chrome_frame_for_microsoft_ie.js"></script>
        <title>News Not Found | ${request.environ['app.DEFAULT_TITLE'] | h}</title>
        <link rel="shortcut icon" href="${request.environ['app.FAVICON'] | h}" />
        <link rel="stylesheet" href="${request.environ['app.STATIC_ROOT'] | h}/css/default.css" />
        <meta name="app_default_title" content="${request.environ['app.DEFAULT_TITLE'] | h}" />
        <meta name="app_root" content="${request.environ['app.ROOT'] | h}" />
        <meta name="app_static_root" content="${request.environ['app.STATIC_ROOT'] | h}" />
        <script>
            //<![CDATA[
                (function (global) {
                    'use strict'
                    
                    var ROOT = document.querySelector(
                            'html > head > meta[name="app_root"]').content
                    var REDIRECT_DELAY = 500
                    
                    function main () {
                        setTimeout(function () {
                            location.assign(ROOT + '/')
                        }, REDIRECT_DELAY)
                    }
                    
                    document.addEventListener('DOMContentLoaded', function (evt) {
                        main()
                    })
                })(this)
            //]]>
        </script>
    </head>
    <body>
        <div class="page">
            <h1>News Not Found</h1>
            % if news_not_found__info is not None:
            <p>Additional Info: <b>${news_not_found__info | h}</b></p>
            % endif
        </div>
    </body>
</html>
