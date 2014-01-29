#! /bin/bash

USAGE="Usage: exract.sh data.mdb"

if [ $# == 0 ] ; then
    echo $USAGE
    exit 1;
fi

for TT in $(mdb-tables $1); do
    mdb-export -D '%Y-%m-%d %H:%M:%S' $1 "$TT" > "${TT}.csv"
done
