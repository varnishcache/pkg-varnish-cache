Packaging files for Varnish Cache
=================================

This repository contains the necessary scripts to package up Varnish Cache.

How to build
------------

The flow is roughly:

1) Set up the build environment. On Redhat that is mock, on Debian/Ubuntu you
   need sbuild.
2) Put the Varnish Cache .tar.gz archive into sources/.
3) Run ./package-deb or ./package-rpm.


Branch structure
----------------

This repository will contain a master branch and zero or more
maintenance branches.

master should be used to build the last stable release _and_ the development
release, all the way up until development diverges enough that it isn't
useful/possible any more.

At that point, a maintenance branch should be branched off. These should be
deleted from git 12 months after the release is end of life. Before deletion,
a git archive of the branch should be extracted and made public.

If you can work around branching, do it. Rather have one slightly untidy
packaging ruleset, than two/three slightly different that needs to be kept in
sync.

Setting up the Build environment
--------------------------------

Debian/Ubuntu
`````````````
.. _sbuild: https://wiki.debian.org/sbuild
.. _schroot: https://wiki.debian.org/Schroot

	NOTICE: These instructions need improvements. Please send pull
	requests!

* install sbuild_, schroot_ and other required tools::

     sudo apt-get install sbuild schroot debootstrap

* use ``sbuild-createchroot`` to set up a standard chroot for building
  packages, see sbuild_

  set ``$REL`` to the release to be set up, ``$ARCH`` to the architecture::

     REL=jessie
     ARCH=amd64
     sudo sbuild-adduser $LOGNAME
     sudo sbuild-createchroot \
       --include=eatmydata,ccache,gnupg \
       ${REL} \
       /srv/chroot/${REL}-${ARCH}-sbuild \
       http://httpredir.debian.org/debian

  The ``package-deb`` script assumes a chroot environment by the name
  ``trusty-amd64``, so an alias needs to be added to the chroot we've
  just created::

     echo 'aliases=trusty-amd64' | \
       sudo tee -a /etc/schroot/chroot.d/${REL}-${ARCH}-sbuild-*


Contact
-------

You can reach the developers and packagers using this email list:
<varnish-dev@varnish-cache.org>
