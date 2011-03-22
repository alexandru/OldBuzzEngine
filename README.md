About
=======

TheBuzzEngine is a simple commenting system, designed for Google App
Engine, as a replacement for DISQUS and similar services.

Working Example
---------------

[http://alexn.org/TheBuzzEngine/#comments](http://alexn.org/TheBuzzEngine/#comments)

Details
=======

I tried to use [Disqus](http://disqus.com) for adding commenting to my
blog pages; but Disqus is too complex and I need something simpler:

- 4 fields: Name, Email, URL + Comment
- Those 3 author-related fields should be tracked with a cookie and
  auto-completed
- Gravatar for user images
- Moderation (editing or removing) by email
- Fast, light

TheBuzzEngine is an implementation for the above and it runs on Google's App Engine.

Highlights
----------

Cross-domain requests are needed and are implemented using
Access-Control-Allow-Origin, if the browser has support for it,
otherwise it uses a Flash plugin as a fallback (e.g. IExplorer < 8,
Firefox < 3.5).

The flash plugin is a lot slower / heavyweight and is not loaded
unless needed.

App Engine Facilities used thus far:

- datastore
- memcached
- tasks queue
- sending email

Browsers supported
------------------

Tested with Chrome 5, Firefox 3.5, Opera 11, IExplorer 8, IExplorer 6.

In IExplorer &lt; 8 the commenting form is disabled (meaning only
comments are shown). I may fix this, but incentive for me to fix it
for IExplorer 6 is pretty low. If you want IExplorer 6, send me a note
and I'll reconsider.