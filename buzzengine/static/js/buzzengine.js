window.THEBUZZENGINE = {
    get_data_domain: function () {
	var comments = document.getElementById("comments");
	var domain = comments.getAttribute('data-domain');
	
	if (!domain)
	    throw "Cannot detect <div id='comments' data-domain='...'> tag inside document!";
	return domain;
    },
    get_script_dir: function () {
	return "http://" + THEBUZZENGINE.get_data_domain() + "/static/js/";
    }
};

window.CROSSDOMAINJS_PATH = THEBUZZENGINE.get_script_dir();

window.crossdomainjs = (function () {
    //
    // Detecting absolute path of this script, if not set in the
    // external document.
    //
    if (!CROSSDOMAINJS_PATH) {
	var scripts = document.getElementsByTagName("script")
	for (var i=0; i<scripts.length; i++) {
	    var src = scripts[i].getAttribute('src');
	    if (src && src.match(/crossdomain-ajax.js/)) {
		CROSSDOMAINJS_PATH = src.replace("crossdomain-ajax.js", '');
		break;
	    }
	}
	
	// is the path relative to our document?
	if (CROSSDOMAINJS_PATH && ! CROSSDOMAINJS_PATH.match(/^(https?|HTTPS?):\/\//) && CROSSDOMAINJS_PATH.substring(0,1) != '/') 
	    CROSSDOMAINJS_PATH = (window.location + '').replace(/[^\/]*$/, '') + CROSSDOMAINJS_PATH;
	
	// we cannot go on without it
	if (!CROSSDOMAINJS_PATH) 
	    throw "crossdomain-ajax.js cannot work without CROSSDOMAINJS_PATH. Please set it before loading this script.";
    }


    // used by async_load_javascript
    var FILES_INCLUDED = {};
    var FILES_LOADING  = {}; // for avoiding race conditions
    var REGISTERED_CALLBACKS = {};

    //
    // Used to test if an object is a primitive or an Object.
    //
    function type(obj){
	return Object.prototype.toString.call(obj).match(/^\[object (.*)\]$/)[1]
    }

    function is_iexplorer() { 
	return navigator.userAgent.indexOf('MSIE') !=-1 
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

    //
    // Does a request using flXHR (the Flash module).
    // Assumes flXHR.js is already loaded.
    //
    function _ajax_with_flxhr(options) {
	var url     = options['url'];
	var type    = options['type'] || 'GET';
	var success = options['success'];
	var error   = options['error'];
	var data    = options['data'];

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
	    loadPolicyURL: CROSSDOMAINJS_PATH + "load-policy.xml"
	});

	flproxy.open(type, url, true);
	flproxy.send(data);
    }

    //
    // Does an ajax request.
    //
    // For browsers that do not support CORS, it fallbacks to a flXHR
    // request.
    //
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
	    async_load_javascript(CROSSDOMAINJS_PATH + "flXHR/flXHR.js", function () {
		_ajax_with_flxhr(options);
	    });
	}
	else {
	    var handle_load = function (event_type) {
		return function (XHRobj) {
		    // stupid IExplorer!!!
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

    return {
	ajax: ajax,
	async_load_javascript: async_load_javascript
    }
})();


(function () {

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

    function get_comments_url() {
	var author = readCookie("author");
	author = author ? encodeURI(author) : null;

	var url = "http://" + THEBUZZENGINE.get_data_domain() + "/api/comments/";

	url += "?article_url=" + encodeURI(get_article_url());
	if (author) url += "&author=" + encodeURI(author);
	return url;
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

    function with_jquery(executefn) {
	var is_loaded = (typeof jQuery != 'undefined');
	if (is_loaded) return executefn();	
	crossdomainjs.async_load_javascript("http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js", executefn);
    }

    function execute_on_load() {
	var url = get_comments_url();

	crossdomainjs.ajax({
	    url: url,
	    type: 'GET',
	    success: function (data) {
		document.getElementById('comments').innerHTML = data;
		enable_reply();
	    }
	});
    }

    function enable_reply() {
	with_jquery(function () {
	    var form = jQuery('#comments form');

	    form.submit(function (e) {
		var url = get_comments_url();

		jQuery('input[type=submit]', form).hide();
		jQuery('.loader', form).show();

		crossdomainjs.ajax({
		    url:  get_comments_url(),
		    type: 'POST',
		    data: form.serialize(),
		    success: function (data) {
			jQuery('#comments').html(data);
			enable_reply();
		    }
		});

		e.preventDefault();
		return false;
	    });

	    form.show();
	});
    }
    
    execute_on_load();
})();