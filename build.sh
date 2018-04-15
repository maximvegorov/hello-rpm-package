#!/usr/bin/env bash

set -e
set -x

PACKAGE=${PACKAGE:-$(basename $(pwd))}

rm -rf ./rpmbuild

mkdir -p rpmbuild/{BUILD,SOURCES,SPECS,RPMS,SRPMS}

./mvnw clean package

ARCHIVE_NAME=$PACKAGE-$(grep -i -m 1 'Version:' rpm/rpm.spec | awk '{print $2}')
ARCHIVE_DIR=rpmbuild/SOURCES/$ARCHIVE_NAME

mkdir -p $ARCHIVE_DIR

mv target/$PACKAGE-LATEST.jar $ARCHIVE_DIR
sed "s/%%%PACKAGE%%%/$PACKAGE/" rpm/log4j2.xml > $ARCHIVE_DIR/log4j2.xml
sed "s/%%%PACKAGE%%%/$PACKAGE/" rpm/start.sh > $ARCHIVE_DIR/$PACKAGE
sed "s/%%%PACKAGE%%%/$PACKAGE/" rpm/systemd.service > $ARCHIVE_DIR/$PACKAGE.service

tar -czf rpmbuild/SOURCES/$ARCHIVE_NAME.tar.gz -C rpmbuild/SOURCES $ARCHIVE_NAME
rm -rf $ARCHIVE_DIR

sed "s/%%%PACKAGE%%%/$PACKAGE/" rpm/rpm.spec > rpmbuild/SPECS/$PACKAGE.spec

rpmbuild --define "-topdir $(pwd)/rpmbuild" -bb rpmbuild/SPECS/$PACKAGE.spec
