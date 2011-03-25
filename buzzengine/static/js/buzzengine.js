(function () {
    var FILES_INCLUDED = {};
    var FILES_LOADING  = {}; // for avoiding race conditions
    var REGISTERED_CALLBACKS = {};


    function get_data_domain() {
	var comments = document.getElementById("comments");
	return comments.getAttribute('data-domain');
    }

    function type(obj){
	return Object.prototype.toString.call(obj).match(/^\[object (.*)\]$/)[1]
    }

    function is_iexplorer() { return navigator.userAgent.indexOf('MSIE') !=-1 }

    function get_ie_version()
    // Returns the version of Internet Explorer or a -1
    // (indicating the use of another browser).
    {
	var rv = -1; // Return value assumes failure.
	if (navigator.appName == 'Microsoft Internet Explorer')
	{
	    var ua = navigator.userAgent;
	    var re  = new RegExp("MSIE ([0-9]{1,}[\.0-9]{0,})");
	    if (re.exec(ua) != null)
		rv = parseFloat( RegExp.$1 );
	}
	return rv;
    }

    function by_id(id){ return (type(id) != 'String' ? id : document.getElementById(id)) }
    function show(id) { by_id(id).style.display = 'block' }
    function hide(id) { by_id(id).style.display = 'none' }

    function is_shown(obj)
    {
	obj = by_id(obj);
	if (obj == document) return true;
	
	if (!obj) return false;
	if (!obj.parentNode) return false;
	if (obj.style) {
            if (obj.style.display == 'none') return false;
            if (obj.style.visibility == 'hidden') return false;
	}
	
	//Try the computed style in a standard way
	if (window.getComputedStyle) {
            var style = window.getComputedStyle(obj, "");
            if (style.display == 'none') return false;
            if (style.visibility == 'hidden') return false;
	}
	
	//Or get the computed style using IE's silly proprietary way
	var style = obj.currentStyle;
	if (style) {
            if (style['display'] == 'none') return false;
            if (style['visibility'] == 'hidden') return false;
	}
	
	return isVisible(obj.parentNode);
    }

    function bind(id, name, handler) { 
	var elem = by_id(id);
	if (elem.addEventListener && ! is_iexplorer())
	    elem.addEventListener(name, handler, false);
	else if (elem.addEventListener)
	    elem.addEventListener(name, handler);
	else if (elem.attachEvent) 
	    elem.attachEvent('on'+name, handler);
    }

    function setClass(id, value) { by_id(id).setAttribute('class', value) };

    function get_form_element(options) {
	var elem_name = options['name'];
	var elem_type = options['type'];
	var elem_tag  = options['tag'];

	var comments  = by_id('comments');
	var tag_types = elem_tag ? [elem_tag] : ['input', 'textarea', 'button'];

	for (var i=0; i<tag_types.length; i++) {
	    tag_name = tag_types[i];

	    var inputs = comments.getElementsByTagName(tag_name);
	    if (!inputs) continue;

	    for (var j=0; j<inputs.length; j++) {
		var elem = inputs[j];
		
		var is_valid = 1;
		if (elem_name && elem.getAttribute('name') != elem_name)
		    is_valid = 0;
		if (elem_type && elem.getAttribute('type') != elem_type)
		    is_valid = 0;
		if (is_valid)
		    return elem;
	    }
	}
    }

    function getElementByClassName(parent_id, cls) {
	var parent = by_id(parent_id);
	var elems = parent.getElementsByTagName("*");
	for (var i=0; i<elems.length; i++) {
	    var elem = elems[i];
	    var elem_cls = elem.getAttribute('class');
	    if (elem_cls && (elem_cls == cls || elem_cls.match(/cls/)))
		return elem;
	}
    }

    function get_article_url() {
	return BUZZENGINE_PARAMS.article_url || (window.location + '');
    }

    function get_article_title() {
	var title = document.getElementsByTagName('title').length ? document.getElementsByTagName('title')[0].innerHTML : null
	return BUZZENGINE_PARAMS.article_title || title;
    }

    function get_current_author() {
	var comments = by_id('comments');
	var data = getElementByClassName(comments, 'data');
	var current_author = getElementByClassName(data, 'current_author');
	return current_author.innerHTML;
    }

    function serialize_form() {
	var comments = by_id('comments');
	var form = comments.getElementsByTagName('form')[0];

	var parts = new Array();
	var allinputs = new Array();
	var inputs = form.getElementsByTagName('input');
	var textareas = form.getElementsByTagName('textarea');

	for (var i=0; i<inputs.length; i++)
	    allinputs.push(inputs[i]);
	for (var i=0; i<textareas.length; i++)
	    allinputs.push(textareas[i]);

	for (var i=0; i<allinputs.length; i++) {
	    var name = allinputs[i].getAttribute('name');
	    if (!name) continue;
	    var value = allinputs[i].value || '';
	    parts.push(encodeURI(name) + "=" + encodeURI(value));
	}
	return parts.join('&');
    }

    function createCookie(name,value,days) {
	if (days) {
	    var date = new Date();
	    date.setTime(date.getTime()+(days*24*60*60*1000));
	    var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
    }

    function readCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
	    var c = ca[i];
	    while (c.charAt(0)==' ') c = c.substring(1,c.length);
	    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
    }

    function eraseCookie(name) {
	createCookie(name,"",-1);
    }

    // used by async_load_javascript
    function register_callback(file, callback) {
	if (!REGISTERED_CALLBACKS[file])
	    REGISTERED_CALLBACKS[file] = new Array();
	REGISTERED_CALLBACKS[file].push(callback);
    }

    // used by async_load_javascript
    function execute_callbacks(file) {
	while (REGISTERED_CALLBACKS[file].length > 0) {
	    var callback = REGISTERED_CALLBACKS[file].pop();
	    if (callback) callback();
	}
    }

    //
    // Loads a Javascript file asynchronously, executing a `callback`
    // if/when file gets loaded.
    //
    function async_load_javascript(file, callback) {
	register_callback(file, callback);

	if (FILES_INCLUDED[file]) {
	    execute_callbacks(file);
	    return true;
	}
	if (FILES_LOADING[file]) 
	    return false;

	FILES_LOADING[file] = true;

	var html_doc = document.getElementsByTagName('head')[0];
	js = document.createElement('script');
	js.setAttribute('type', 'text/javascript');
	js.setAttribute('src', file);
	html_doc.appendChild(js);

	js.onreadystatechange = function () {
            if (js.readyState == 'complete' || js.readyState == 'loaded') {
		if (! FILES_INCLUDED[file]) {
		    FILES_INCLUDED[file] = true;
		    execute_callbacks(file);
		}
            }
	};

	js.onload = function () {
	    if (! FILES_INCLUDED[file]) {
		FILES_INCLUDED[file] = true;
		execute_callbacks(file);
	    }
	};

	return false;
    }

    function _ajax_with_flxhr(options) {
	var url = options['url'];
	var type = options['type'] || 'GET';
	var success = options['success'];
	var error = options['error'];
	var data  = options['data'];

	function handle_load(XHRobj) {
	    if (XHRobj.readyState == 4) {
		if (XHRobj.status == 200 && success)
		    success(XHRobj.responseText, XHRobj);
		else
		    error(XHRobj);
	    }
	}

	var flproxy = new flensed.flXHR({ 
	    autoUpdatePlayer:false, 
	    instanceId:"myproxy1", 
	    xmlResponseText:false, 
	    onreadystatechange:handle_load, 
	    loadPolicyURL: "http://" + get_data_domain() + "/static/load-policy.xml"
	});

	flproxy.open(type, url);
	flproxy.send(data);
    }

    function ajax(options) {
	var url = options['url'];
	var type = options['type'] || 'GET';
	var success = options['success'];
	var error = options['error'];
	var data  = options['data'];

	try {
	    var xhr = new XMLHttpRequest();
	} catch(e) {}	
	
	var is_sane = false;

	if (xhr && "withCredentials" in xhr){
	    xhr.open(type, url, true);
	} else if (typeof XDomainRequest != "undefined"){
	    xhr = new XDomainRequest();
	    xhr.open(type, url);
	}
	else
	    xhr = null;

	if (!xhr) {
	    if (typeof flensed == 'undefined') {
		async_load_javascript("http://" + get_data_domain() + "/static/js/flXHR/flXHR.js", function () {
		    _ajax_with_flxhr(options);
		});
	    }
	    else
		_ajax_with_flxhr(options);
	}
	else {
	    var handle_load = function (event_type) {
		return function (XHRobj) {
		    // stupid!!!
		    var XHRobj = is_iexplorer() ? xhr : XHRobj;

		    if (event_type == 'load' && (is_iexplorer() || XHRobj.readyState == 4) && success)
			success(XHRobj.responseText, XHRobj);
		    else if (error)
			error(XHRobj);
		}
	    };

	    try {
		xhr.withCredentials = true;
	    } catch(e) {};

	    xhr.onload  = function (e) { handle_load('load')(is_iexplorer() ? e : e.target) };
	    xhr.onerror = function (e) { handle_load('error')(is_iexplorer() ? e : e.target) };
	    xhr.send(data);
	}
    }

    function decorate_form(html) {
	if (html)
	    document.getElementById("comments").innerHTML = html;

	if (is_iexplorer() && get_ie_version() < 8) {
	    // form is not allowed on older IExplorer versions
	    // suck it up
	    hide(document.getElementById('comments').getElementsByTagName('form')[0]);
	    return;
	}

	setTimeout(function () {
	    get_form_element({name:'article_url'}).setAttribute('value', get_article_url());
	    get_form_element({name:'article_title'}).setAttribute('value', get_article_title());

	    var author = get_current_author();
	    if (author) 
		createCookie("author", author, 365);

	    var form = by_id('comments').getElementsByTagName('form')[0];

	    bind(form, 'submit', function (e) {
		if (is_iexplorer())
		    e.returnValue = false;
		else if (e.preventDefault)
		    e.preventDefault();

		show( getElementByClassName('comments', 'loader') );
		hide( getElementByClassName('comments', 'button') );

		ajax({
		    url: form.getAttribute('action'),
		    type: 'POST',
		    data: serialize_form(),
		    success: function (data) {
			decorate_form(data);
		    },
		    error: function (resp) {
			getElementByClassName('comments', 'errornote').remove();
			form.innerHTML = "<div class='errornote'>Something wrong happened, please try again later!</div>" + form.innerHTML;
		    }
		});

		return false;
	    });
	}, 0);
    }

    function execute_on_load() {
	var author = readCookie("author");
	author = author ? encodeURI(author) : null;

	var url = "http://" + get_data_domain() + "/api/comments/";
	url += "?article_url=" + encodeURI(window.location + '');
	if (author) url += "&author=" + encodeURI(author);

	ajax({
	    url: url,
	    type: 'GET',
	    success: function (data) {
		decorate_form(data);
	    }
	});
    }
    
    execute_on_load();
})();