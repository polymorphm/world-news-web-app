// -*- mode: javascript; coding: utf-8 -*-

(function () {
    'use strict'
    
    var MSIE_DETECT_BEFORE_VERSION = [10, 0]
    
    function undefined_safe_new (factory) {
        if (factory !== undefined) {
            var obj = new factory()
            
            return obj
        }
    }
    
    function event_msie_test () {
        // детектирование версий 'Microsoft IE': [6, 0], [7, 0], [8, 0]
        
        if (window.addEventListener === undefined &&
                window.attachEvent !== undefined) {
            return true
        }
        
        return false
    }
    
    function xhr_msie_test () {
        // детектирование версий 'Microsoft IE': [9, 0], <..и..может..чуть..выше..>
        
        var xhr = undefined_safe_new(window.XMLHttpRequest)
        var xdr = undefined_safe_new(window.XDomainRequest)
        
        if ((xhr === undefined || xhr.responseType === undefined) &&
                xdr !== undefined) {
            return true
        }
        
        return false
    }
    
    function msie_detect () {
        // детектирование 'Microsoft IE' по характерным несоответствиям стандартам
        
        if (MSIE_DETECT_BEFORE_VERSION[0] > 6 && event_msie_test()) {
            return true
        }
        
        if (MSIE_DETECT_BEFORE_VERSION[0] > 9 && xhr_msie_test()) {
            return true
        }
        
        // <ЗДЕСЬ> в будущем возможно будет детектирование других версий
        
        return false
    }
    
    function add_event_listener (element, type, listener, use_capture) {
        // потомучто 'Microsoft IE' не поддерживает addEventListener()
        
        if (element.addEventListener !== undefined) {
            element.addEventListener(type, listener, use_capture)
        } else if (element.attachEvent !== undefined) {
            element.attachEvent('on' + type, listener)
        } else {
            throw 'addEventListener() not implemented'
        }
    }
    
    function make_clear_both_div () {
        var clear_both_div = document.createElement('div')
        clear_both_div.style.clear = 'both'
        
        return clear_both_div
    }
    
    function make_google_chrome_frame_notify () {
        var install = document.createElement('input')
        install.type = 'button'
        install.value = 'Установить'
        install.style.cssFloat = 'right' // 'Microsoft IE' не поддерживает это
        install.style.styleFloat = 'right' // специально для 'Microsoft IE'
        add_event_listener(install, 'click', function (event) {
            location.assign('http://www.google.com/chromeframe/eula.html', '_blank')
        }, false)
        
        var google_chrome_frame = document.createElement('span')
        google_chrome_frame.style.fontWeight = 'bold'
        google_chrome_frame.appendChild(
            document.createTextNode(
                'Chrome Frame'
            )
        )
        
        var learn_more = document.createElement('span')
        learn_more.style.cursor = 'pointer'
        learn_more.style.color = 'rgb(0,0,255)'
        learn_more.appendChild(
            document.createTextNode(
                'Узнать больше'
            )
        )
        add_event_listener(learn_more, 'click', function (event) {
            location.assign('http://www.google.com/chromeframe/', '_blank')
        }, false)
        
        var text = document.createElement('div')
        text.style.padding = '5px'
        text.appendChild(
            document.createTextNode(
                'У Вас не установлен или отключен компонент '
            )
        )
        text.appendChild(google_chrome_frame)
        text.appendChild(
            document.createTextNode(
                ', необходимый для корректной работы Вашего браузера ('
            )
        )
        text.appendChild(learn_more)
        text.appendChild(
            document.createTextNode(')')
        )
        
        var notify = document.createElement('div')
        notify.style.padding = '3px'
        notify.style.font = '12px "DejaVu Sans", sans-serif'
        notify.style.border = '1px rgb(245,245,181) outset'
        notify.style.background = 'rgb(245,245,181)'
        notify.style.color = 'rgb(0,0,0)'
        notify.appendChild(install)
        notify.appendChild(text)
        notify.appendChild(make_clear_both_div())
        
        return notify
    }
    
    function show_notify (notify) {
        document.body.style.margin = '0'
        if (document.body.firstChild) {
            document.body.insertBefore(notify, document.body.firstChild)
        } else {
            document.body.appendChild(notify)
        }
    }
    
    function main (event) {
        if (msie_detect()) {
            var notify = make_google_chrome_frame_notify()
            
            show_notify(notify)
        }
    }
    
    add_event_listener(window, 'load', main, false)
})()
