#!/bin/sh
curl https://www.octave.org/download 2>/dev/null |grep 'is the latest stable release' |sed -e 's,</strong>.*,,;s,.* ,,'
