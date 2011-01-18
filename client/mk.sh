#!/bin/bash
set -e

appname=com.github.amhk.boxee-svtplay
out=../out/$appname

function target-xml()
{
    local src="$1"
    local dest=$out/"$2"

    echo "[APP] $dest"
    awk $awkflags -f sub.awk "$src" | tidy -xml -utf8 -qi -w 80 -o "$dest"
    if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
        rm "$dest"
    fi
}

function target-meta()
{
    local src="$1"
    local dest=$out/"$2"

    echo "[APP] $dest"
    cp "$src" "$dest"
}

clean=0
awkflags=""

while getopts "cd" flag; do
    case $flag in
        c) clean=1;;
        d) out=$out-debug; awkflags="-v debug=1";;
        *) exit 1;;
    esac
done

if [[ $clean -eq 1 ]]; then
    rm -rf $out
    rm -rf $out-debug
else
    mkdir -p $out/'skin/Boxee Skin NG/720p'
    target-xml descriptor.xml descriptor.xml
    target-xml main.xml 'skin/Boxee Skin NG/720p/main.xml'
    target-meta ../AUTHORS AUTHORS
    target-meta ../LICENSE LICENSE
    target-meta ../README README
fi
