#!/usr/bin/env bash

set -e

PACKAGE=$(basename $0)
JAR_LOCATION=/usr/share/java/$PACKAGE
LOG_CONFIG_LOCATION=/etc/$PACKAGE

/usr/bin/java -server \
    -showversion \
    -jar ${JAR_LOCATION}/${PACKAGE}-LATEST.jar \
    -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=8081 \
    -XX:+UseParallelGC \
    -XX:+UseParallelOldGC \
    -XX:MaxGCPauseMillis=100 \
    -XX:-OmitStackTraceInFastThrow \
    -Dcom.sun.management.jmxremote \
    -Dcom.sun.management.jmxremote.port=8082 \
    -Dcom.sun.management.jmxremote.local.only=false \
    -Dcom.sun.management.jmxremote.rmi.port=8082 \
    -Dcom.sun.management.jmxremote.authenticate=false \
    -Dcom.sun.management.jmxremote.ssl=false \
    -Djava.rmi.server.hostname=localhost \
    -Dfile.encoding=UTF-8 \
    -Djava.awt.headless=true \
    -Djava.security.egd=file:/dev/./urandom \
    -Dnetworkaddress.cache.ttl=60 \
    -Dsun.net.client.defaultConnectTimeout=10000 \
    -Dsun.net.client.defaultReadTimeout=10000 \
    -Duser.language=en \
    -Duser.country=US \
    -Duser.timezone=GMT \
    -Dlogging.config=${LOG_CONFIG_LOCATION}/log4j2.xml
