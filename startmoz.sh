#! /bin/sh

if [[ "$1" != http* ]] ; then
    if [[ "$1" == www* ]] ; then
	URL="http://$1"
    elif [[ "$1" != /* ]] && [[ "$1" != ~* ]] ; then
	URL="file://`pwd`/$1"
    else
	URL="file://$1"
    fi
else
    URL="$1"
fi

if which firefox > /dev/null 2>&1 ; then
    if ps -u $USER | grep -q "firefox" ; then
	firefox -remote "openURL($URL, new-tab)" &
    else
	firefox $URL &
    fi
elif which firebird > /dev/null 2>&1 ; then
    if ps -u $USER | grep -q "MozillaFirebird" ; then
	firebird -remote "openURL($URL, new-tab)" &
    else
	firebird $URL &
    fi
elif which mozilla > /dev/null 2>&1 ; then
    if ps -u $USER | grep -q "mozilla" ; then
	mozilla -remote "openURL($URL, new-tab)" &
    else
	mozilla $URL &
    fi
fi
