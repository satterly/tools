#!/bin/sh

SRC_DBHOST=localhost
SRC_DBPORT=8432
SRC_DBUSER=discussion_app

DEST_DBHOST=localhost
DEST_DBPORT=5432
DEST_DBUSER=pgowner

echo "Dumping data to $SRC_DBHOST:$SRC_DBPORT"

psql \
  -v ON_ERROR_STOP=1 \
  -d discussion \
  -U $SRC_DBUSER \
  -h $SRC_DBHOST \
  -p $SRC_DBPORT \
  -f dump.sql

echo "Loading dumped data to $DEST_DBHOST:$DEST_DBPORT"

psql \
  -v ON_ERROR_STOP=1 \
  -d discussion \
  -U $DEST_DBUSER \
  -h $DEST_DBHOST \
  -p $DEST_DBPORT \
  -f load.sql