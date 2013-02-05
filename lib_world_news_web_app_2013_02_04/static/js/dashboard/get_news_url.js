// -*- mode: js; coding: utf-8 -*-

(function (global) {
    'use strict'
    
    var ROOT = document.querySelector('html > head > meta[name="app_root"]').content
    
    function create_tpl_elem (el_name, html) {
        var elem = document.createElement(el_name)
        elem.innerHTML = html
        return elem
    }
    
    function create_button_elem (text) {
        var elem = document.createElement('a')
        elem.href = '#'
        elem.appendChild(document.createTextNode(text))
        return elem
    }
    
    function replace_elem (new_elem, old_elem) {
        old_elem.parentNode.replaceChild(new_elem, old_elem)
    }
    
    function insert_elem (elem, parent_elem, stub_sel) {
        var stub_elem = parent_elem.querySelector(stub_sel)
        replace_elem(elem, stub_elem)
    }
    
    function create_form () {
        var form = {}
        
        form.busy = false
        form.busy_id = {}
        
        form.query_form_elem = create_tpl_elem(
                'div',
                '<p>Original News URL</p>' +
                '<p><span class="original_news_url_input_stub"></span></p>' +
                '<p><span class="get_news_url_button_stub"></span></p>')
        
        form.original_news_url_input_elem = document.createElement('input')
        form.get_news_url_button_elem = create_button_elem('Get News URL')
        form.get_news_url_button_elem.addEventListener(
                'click', function (event) {
                    event.preventDefault()
                    
                    if (form.busy) {
                        return
                    }
                    
                    form_get_news_url(form)
                })
        
        insert_elem(form.original_news_url_input_elem, form.query_form_elem, '.original_news_url_input_stub')
        insert_elem(form.get_news_url_button_elem, form.query_form_elem, '.get_news_url_button_stub')
        
        form.result_form_elem = create_tpl_elem(
                'div',
                '<p>Original News URL: <b><span class="original_news_url_stub"></span></b></p>' +
                '<p>Status: <b><span class="status_stub"></span></b></p>' +
                '<p>News URL: <b><span class="news_url_stub"></span></b></p>' +
                '<p>Micro News URL: <b><span class="micro_news_url_stub"></span></b></p>' +
                '<p>News Key (in Base64): <b><span class="news_key_stub"></span></b></p>' +
                '<p><span class="close_info_button_stub"></span></p>')
        
        form.original_news_url_elem = document.createElement('span')
        form.status_elem = document.createElement('span')
        form.news_url_elem = document.createElement('span')
        form.micro_news_url_elem = document.createElement('span')
        form.news_key_elem = document.createElement('span')
        form.close_info_button_elem = create_button_elem('Close Info (Enter Another URL)')
        
        insert_elem(form.original_news_url_elem, form.result_form_elem, '.original_news_url_stub')
        insert_elem(form.status_elem, form.result_form_elem, '.status_stub')
        insert_elem(form.news_url_elem, form.result_form_elem, '.news_url_stub')
        insert_elem(form.micro_news_url_elem, form.result_form_elem, '.micro_news_url_stub')
        insert_elem(form.news_key_elem, form.result_form_elem, '.news_key_stub')
        insert_elem(form.close_info_button_elem, form.result_form_elem, '.close_info_button_stub')
        
        form.close_info_button_elem.addEventListener(
                'click', function (event) {
                    event.preventDefault()
                    
                    form_close_info(form)
                })
        
        form.elem = create_tpl_elem(
                'div', '<div class="current_stub"></div>')
        
        form.current_elem = form.query_form_elem
        insert_elem(form.current_elem, form.elem, '.current_stub')
        
        return form
    }
    
    function form_get_news_url(form) {
        if (!form.original_news_url_input_elem.value) {
            return
        }
        
        form.busy = true
        var busy_id = form.busy_id = {}
        form.original_news_url = form.original_news_url_input_elem.value
        
        form.original_news_url_elem.textContent = form.original_news_url
        form.status_elem.textContent = 'Working'
        form.news_url_elem.textContent = '...'
        form.micro_news_url_elem.textContent = '...'
        form.news_key_elem.textContent = '...'
        
        replace_elem(form.result_form_elem, form.current_elem)
        form.current_elem = form.result_form_elem
        
        var req = new XMLHttpRequest()
        
        req.addEventListener('load', function (event) {
            if (!form.busy || form.busy_id != busy_id) {
                return
            }
            
            form.busy = false
            form.busy_id = {}
            
            if (req.status != 200) {
                form.status_elem.textContent = 'Error (req.status != 200)'
                return
            }
            
            var data = JSON.parse(req.responseText)
            form.news_url_elem.textContent = data.news_url
            form.micro_news_url_elem.textContent = data.micro_news_url
            form.news_key_elem.textContent = data.news_key
            
            form.status_elem.textContent = 'Ready'
        })
        
        req.open('POST', ROOT + '/ajax/get-news-url-info', true)
        req.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
        req.setRequestHeader('Content-Type', 'application/json;charset=utf-8')
        req.send(JSON.stringify({
                'original_news_url': form.original_news_url
                }))
    }
    
    function form_close_info(form) {
        form.busy = false
        form.busy_id = {}
        
        replace_elem(form.query_form_elem, form.current_elem)
        form.current_elem = form.query_form_elem
    }
    
    document.addEventListener('DOMContentLoaded', function(event) {
        var form = create_form()
        
        insert_elem(form.elem, document, '.get_news_url_stub')
    })
})(this)
