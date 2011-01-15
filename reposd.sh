#!/bin/bash
set -e

rm -rf download index.xml && mkdir download
echo "<apps>" >> index.xml
for app in $(find . -mindepth 0 -maxdepth 1 -type d -name 'net.kongstadbrun.*' | cut -d/ -f2-); do
	version=$(egrep '<version>' $app/descriptor.xml | egrep -oe '[0-9]+\.[0-9]')
	zip="download/$app-$version.zip"
	echo "$app, v $version -> $zip"
	zip -qr $zip $app
	cat $app/descriptor.xml >> index.xml
done
echo -e "</apps>\n\n" >> index.xml

python -m SimpleHTTPServer 9000
