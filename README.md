About
=======

TheBuzzEngine is a simple commenting system, designed for Google App
Engine, as a replacement for DISQUS and similar services.

Working Example
---------------

[http://alexn.org/test.html](http://alexn.org/test.html)

Details
=======

I tried to use [Disqus](http://disqus.com) for adding commenting to my
blog pages; but frankly Disqus kind of sucks, as it is too complex,
too hard to optimize and just provides too much. All I need is:

- 4 fields: Name, Email, URL + Comment
- Those 3 author-related fields should be tracked with a cookie and
  auto-completed; no stinkin' Facebook / Twitter login for me
- Gravatar for user images, and that's enough
- Moderation with Askimet and/or manual approvals
- Fast, light

TheBuzzEngine is an implementation for the above (having control over
the source-code is gratifying); and it runs on Google's App Engine,
which is both free of charge (for me, as I won't exceed the free
quota) and infinitely scalable (at least for this type of problem).

I just started working on it. Work in progress.

Highlights
----------

Cross-domain requests are needed and are implemented using
Access-Control-Allow-Origin, if the browser has support for it,
otherwise it uses a Flash plugin as a fallback (e.g. IExplorer < 8,
Firefox < 3.5).

The flash plugin is a lot slower / heavyweight and is not loaded
unless needed.

Missing
-------

Integration with Askimet + moderation interface are missing for
now. Myself I'm relying on the App Engine's own admin interface, but
it is suboptimal and I'm going to improve this.

Only tested in Firefox + Chrome, but should work well in IExplorer and
older browser. Still, more testing is neeed.