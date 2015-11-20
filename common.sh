
function findversion() {
	tarfile=$1

	# This looks like something that should work, but I can't get it right.
	# tar -zxf sources/varnish-4.1.0.tar.gz --wildcards-match^Clash --wildcards '*figure';

	# Workaround follows.
	TMP=tmp.$$.$RANDOM
	mkdir -p $TMP
	tar zxf $tarfile -C $TMP
	mv $TMP/*/configure .
	rm -rf $TMP

	V=$(grep PACKAGE_VERSION= configure | sed "s/.*=//;s/'//g")
	if [ "$V" = "trunk" ]; then
		V="5.0"
		MINOR="0"
	else
		MINOR="${V##*.}"
		V="${V%.*}"
	fi
	rm configure
}

#findversion sources/varnish-4.1.0.tar.gz
#echo $V
#echo $MINOR

