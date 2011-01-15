#!/bin/bash
set -e

out=../out
mkdir -p $out
tmp=$(mktemp -d)
trap "rm -rf $tmp" EXIT

rm -rf $out/download $out/index.xml
mkdir $out/download

echo "<apps>" >> $tmp/index.html
for app in $(find $out -mindepth 0 -maxdepth 1 -type d -name 'net.kongstadbrun.*' | cut -d/ -f3-); do
	version=$(egrep '<version>' $out/$app/descriptor.xml | egrep -oe '[0-9]+\.[0-9]')
	zip="$app-$version.zip"
    echo "[REPOS] $app, v $version -> $zip"
    # zip and strip test-app tag
    cp -a $out/$app $tmp
    pushd $tmp > /dev/null
    sed -i 's+<test-app>true</test-app>++' $app/descriptor.xml
    zip -qr app.zip $app
    popd > /dev/null
    mv $tmp/app.zip $out/download/$zip
	cat $tmp/$app/descriptor.xml >> $tmp/index.html
done
echo "</apps>" >> $tmp/index.html

tidy -xml -utf8 -qi -w 80 -o $out/repository.xml repository.xml
tidy -xml -utf8 -qi -w 80 -o $out/index.xml $tmp/index.html
