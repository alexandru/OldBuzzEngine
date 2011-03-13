(function () {
    var files_included = {};

    function include_js(file, callback) {
	if (files_included[file])
	    return callback();

	var html_doc = document.getElementsByTagName('head')[0];
	js = document.createElement('script');
	js.setAttribute('type', 'text/javascript');
	js.setAttribute('src', file);
	html_doc.appendChild(js);

	js.onreadystatechange = function () {
            if (js.readyState == 'complete' || js.readyState == 'loaded') {
		if (! files_included[file]) {
		    files_included[file] = true;
		    callback();
		}
            }
	};

	js.onload = function () {
	    if (! files_included[file]) {
		files_included[file] = true;
		callback();
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
	    loadPolicyURL: "http://" + jQuery('#comments').attr('data-domain') + "/static/load-policy.xml"
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

	if (xhr && "withCredentials" in xhr){
	    // does nothing else
	} else if (typeof XDomainRequest != "undefined"){
	    xhr = new XDomainRequest();
	}
	else
	    xhr = null;

	if (!xhr) {
	    if (typeof flensed == 'undefined') {
		include_js("http://" + jQuery('#comments').attr('data-domain') + "/static/js/flXHR/flXHR.js", function () {
		    _ajax_with_flxhr(options);
		});
	    }
	    else
		_ajax_with_flxhr(options);
	}
	else {
	    var handle_load = function (XHRobj) {
		if (XHRobj.readyState == 4) {
		    if (XHRobj.status == 200 && success)
			success(XHRobj.responseText, XHRobj);
		    else if (error)
			error(XHRobj);
		}
	    }

	    xhr.open(type, url, true);
	    try {
		xhr.withCredentials = true;
	    } catch(e) {};
	    xhr.onload  = function (e) { handle_load(e.target) };
	    xhr.onerror = function (e) { handle_load(e.target) };
	    xhr.send(data);
	}
    }

    function decorate_form(html) {
	if (html)
	    document.getElementById("comments").innerHTML = html;

	setTimeout(function () {
	    jQuery('#comments form input[name=article_url]').attr('value', window.location + '');
	    jQuery('#comments form input[name=article_title]').attr('value', "Lorem Ipsum");

	    jQuery('#comments form').submit(function (e) {
		e.preventDefault();

		jQuery('#comments .loader').show();
		jQuery('#comments .button').hide();

		ajax({
		    url: jQuery(this).attr('action'),
		    type: 'POST',
		    data: jQuery('#comments form').serialize(),
		    success: function (data) {
			decorate_form(data);
		    },
		    error: function (resp) {
			jQuery('#comments form .errornote').remove();
			jQuery('#comments form').prepend("<div class='errornote'>Something wrong happened, please try again later!</div>");
		    }
		});
	    });
	}, 0);
    }

    function execute_on_load() {
	ajax({
	    url: "http://" + jQuery('#comments').attr('data-domain') + "/api/comments/",
	    type: 'GET',
	    success: function (data) {
		decorate_form(data);
	    }
	});
    }
    
    if (typeof jQuery == 'undefined') 
	include_js("http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js", function () {
	    execute_on_load();
	});
    else	    
	execute_on_load();
})();