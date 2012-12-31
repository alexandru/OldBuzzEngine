About
=======

TheBuzzEngine is a simple commenting system, designed for Google App
Engine, as a replacement for DISQUS and similar services.

Install
=======

1. download the [Google App Engine - Python SDK](http://code.google.com/appengine/downloads.html#Google_App_Engine_SDK_for_Python)
2. create an instance on Google App Engine - check out their docs on [Getting Started](http://code.google.com/appengine/docs/python/gettingstarted) with Python
3. fork this repo or download [an archive](https://github.com/alexandru/TheBuzzEngine/zipball/master)
4. in [appcfg.yml](https://github.com/alexandru/TheBuzzEngine/blob/master/app.yaml) change the "application" (first line) to point to whatever App ID you created
5. in [settings.py](https://github.com/alexandru/TheBuzzEngine/blob/master/buzzengine/settings.py) change ADMIN_EMAIL + EMAIL_SENDER (see comments)
6. deploy and go to the homepage, which should look like [this one](http://thebuzzengine.appspot.com/) -- check out this doc on how to [Upload an Application](http://code.google.com/appengine/docs/python/gettingstarted/uploading.html) to GAE
7. follow the instructions in your app's homepage (you just need to copy a Javascript widget in whatever page you want comments)

Details
=======

I tried to use [Disqus](http://disqus.com) for adding commenting to my
blog pages; but Disqus is too complex and I needed something simpler:

- 4 fields: Name, Email, URL + Comment
- Those 3 author-related fields should be tracked with a cookie and
  auto-completed
- Gravatar for user images
- Moderation (editing or removing) by email
- Fast, light

TheBuzzEngine is an implementation for the above and it runs on
Google's App Engine.

Roadmap
-------

The following features are planned:

- email subscriptions to replies in a thread
- threaded replies to comments (only 1 level)
- Askimet integration for spam filtering
- better admin (email moderation is OK for low traffic, but better control and filtering required)

Cross-domain, Cross-browser requests
------------------------------------

What I did is described in this article:
[http://alexn.org/blog/2011/03/24/cross-domain-requests.html](http://alexn.org/blog/2011/03/24/cross-domain-requests.html)

Browsers supported
------------------

Tested with Chrome 5, Firefox 3.5, Opera 11, IExplorer 8, IExplorer 6.

In IExplorer &lt; 8 the commenting form is disabled (meaning only
comments are shown). I may fix this, but incentive for me to fix it
for IExplorer 6 is pretty low. If you want IExplorer 6, send me a note
and I'll reconsider.

Google App Engine
-----------------

It's OK for simple stuff like this -- just one problem for this app --
unfortunately if there are no warm instances active, request can take
10 seconds.

Facilities used thus far:

- datastore
- memcached
- tasks queue
- sending email

License
-------

MIT Licensed. See the LICENSE file for details.

