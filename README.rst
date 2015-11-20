Packaging files for Varnish Cache
=================================

This repository contains the necessary scripts to package up
Varnish Cache.

How to build
------------

The flow is roughly:

1) Set up the build environment. On Redhat that is mock, on Debian/Ubuntu you
   need sbuild.
2) Put the Varnish Cache .tar.gz archive into source/.
3) Run ./package-deb or ./package-rpm.


Contact
-------

You can reach the developers and packagers using the normal
email list: <varnish-dev@varnish-cache.org>

