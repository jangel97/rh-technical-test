#!/bin/bash
set -a
echo "Starting Tomcat server"
exec ./apache-tomcat-9.0.45/bin/catalina.sh run $@
