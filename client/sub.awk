# awk script to search and replace "$(patterns)".
# The patterns and their replacements are specified by the array "a".
BEGIN {
    id_window = 14000
    id_control = 120
    i = 0;

    # extend this array with new patterns/replacements
    # FIXME: remove obsolete patterns
    a[i++] = "host:192.168.0.103"
    a[i++] = "port:9001"
    a[i++] = "repos/host:192.168.0.103"
    a[i++] = "repos/port:9002"
    a[i++] = "version:0.7"
    a[i++] = "window/main:" id_window++
    a[i++] = "window/title:" id_window++
    a[i++] = "label/hello-world:" id_control++
    a[i++] = "list/main:" id_control++
    a[i++] = "list/title:" id_control++

    if (debug) {
        a[i++] = "tag/id:<id>com.github.amhk.boxee-svtplay-debug</id>"
        a[i++] = "tag/test-app:<test-app>true</test-app>"
    } else {
        a[i++] = "tag/id:<id>com.github.amhk.boxee-svtplay</id>"
        a[i++] = "tag/test-app:"
    }

    # sanity check: key duplicates are not allowed and will throw an error
    i = 0
    for (i in a) {
        split(a[i], tmp, ":")
        k = tmp[1]
        v = tmp[2]
        for (j in keys) {
            if (k == keys[j]) {
                print "error: duplicate key '" k "'" > "/dev/stderr"
                print "i=" i " j=" j > "/dev/stderr"
                exit 1
            }
        }
        keys[i] = k
        values[i] = v
    }
}

# for each line, search for each pattern and replace it with its corresponding
# replacement
{
    for (i in a) {
        split(a[i], tmp, ":")
        pattern = "\\$\\(" tmp[1] "\\)";
        replacement = tmp[2]
        gsub(pattern, replacement, $0)
    }
    if ((unexpected = match($0, "\\$\\(.*\\)")) != 0) {
        print "error: unexpected pattern in line '" $0 "'"> "/dev/stderr"
        exit 1
    }
    print
}
