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

function target-python()
{
    local src="$1"
    local dest=$out/"$2"

    echo "[APP python] $dest"
    awk $awkflags -f sub.awk "$src" > "$dest"
}

function target-cp()
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
    target-python svtplay.py svtplay.py
    target-cp ../AUTHORS AUTHORS
    target-cp ../LICENSE LICENSE
    target-cp ../README README
fi
