About
=======

I recently redesigned my homepage (at [alexn.org](http://alexn.org/)),
deploying it with the help of the Jekyll static site generator and
GitHub Pages.

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