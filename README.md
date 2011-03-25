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
blog pages; but Disqus is too complex and I needed something simpler:

- 4 fields: Name, Email, URL + Comment
- Those 3 author-related fields should be tracked with a cookie and
  auto-completed
- Gravatar for user images
- Moderation (editing or removing) by email
- Fast, light

TheBuzzEngine is an implementation for the above and it runs on
Google's App Engine.

Cross-domain requests
---------------------

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

