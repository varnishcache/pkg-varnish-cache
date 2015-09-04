Packaging files for Varnish Cache
=================================

This repository contains the necessary scripts to package up
Varnish Cache.

git submodules are used for debian/ and redhat/. This may or may not be a good
idea, time will tell.

To get a complete checkout, run:

    git submodule init
    git submodule update


You may need to change the git remote address in .gitmodules from
git@git.varnish-cache.org:varnish-cache-debian.git to
git://git.varnish-cache.org/varnish-cache-debian.git if you don't
have Varnish Cache project access. Do this before you run init/update.
