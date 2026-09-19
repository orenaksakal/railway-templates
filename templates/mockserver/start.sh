#!/bin/sh
set -eu
/bootstrap mkdir -p /config
if [ ! -e /config/expectations.json ]; then
  printf '[]\n' > /config/expectations.json
fi
exec /usr/lib/jvm/temurin25-trimmed/bin/java -Dfile.encoding=UTF-8 -XX:MaxRAMPercentage=75.0 -XX:SharedArchiveFile=/mockserver.jsa -cp '/mockserver-netty-jar-with-dependencies.jar:/libs/*' -Dmockserver.propertyFile=/config/mockserver.properties org.mockserver.cli.Main
