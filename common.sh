
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
	RELEASE=""
	if [ "$V" = "trunk" ]; then
		V="5.1"
		MINOR="0"
	else
		# 4.1.1
		# 4.1.1-beta1
		MINOR="${V:4:1}"
		RELEASE="${V:6}"
		V="${V:0:3}"
	fi
	rm configure
}

#findversion sources/varnish-4.1*gz
#echo "V is: $V"
#echo "MINOR is $MINOR"
#echo "RELEASE is $RELEASE"

