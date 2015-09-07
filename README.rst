Packaging files for Varnish Cache
=================================

This repository contains the necessary scripts to package up
Varnish Cache.

git submodules are used for debian/ and redhat/. This may or may not be a good
idea, time will tell.

To get a complete checkout, run:

    git submodule init
    git submodule update


If you don't have Varnish Cache project access, you probably don't have
SSH access to the debian repository. Use this one-liner to use
the anonymous git service instead:

    sed -i 's|git@git.varnish-cache.org:|git://git.varnish-cache.org/|g' .gitmodules

Do this before you run init/update.
