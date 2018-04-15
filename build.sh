#!/usr/bin/env bash

set -e

PACKAGE=${PACKAGE:-$(basename $(pwd))}

rm -rf ./rpmbuild &> /dev/null

mkdir -p rpmbuild/{BUILD,SOURCES,SPECS,RPMS,SRPMS}

./mvnw clean package

cp target/$PACKAGE-LATEST.jar rpmbuild/BUILD
sed 's/%%%PACKAGE%%%/$PACKAGE/' rpm/log4j2.xml rpmbuild/BUILD/$PACKAGE.log4j2.xml
sed 's/%%%PACKAGE%%%/$PACKAGE/' rpm/start.sh > rpmbuild/BUILD/$PACKAGE
sed 's/%%%PACKAGE%%%/$PACKAGE/' rpm/systemd.service > rpmbuild/BUILD/$PACKAGE.service
sed 's/%%%PACKAGE%%%/$PACKAGE/' rpm/rpm.spec > rpmbuild/BUILD/$PACKAGE.spec

rpmbuild --define "-topdir $(pwd)/rpmbuild" -bb rpmbuild/SPECS/$PACKAGE.spec
