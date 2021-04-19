FROM registry.access.redhat.com/ubi8/ubi-minimal:8.3
LABEL maintainer="Jose Angel Morena Simon"
ENV TZ=Europe/Madrid
ENV HOME /code
ENV USER 1001
WORKDIR $HOME
ADD https://ftp.cixug.es/apache/tomcat/tomcat-9/v9.0.45/bin/apache-tomcat-9.0.45.tar.gz .
RUN microdnf --setopt=tsflags=nodocs install -y java-1.8.0-openjdk-devel tar gzip && \
            microdnf reinstall tzdata -y && \
            microdnf clean all && \
            ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
            tar xvf apache-tomcat-9.0.45.tar.gz
ADD https://tomcat.apache.org/tomcat-9.0-doc/appdev/sample/sample.war apache-tomcat-9.0.45/webapps/
COPY start.sh .
RUN chmod -R 755 $HOME && chown -R $USER:$USER $HOME
USER $USER
ENTRYPOINT [ "./start.sh"]
