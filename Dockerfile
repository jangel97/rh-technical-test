FROM registry.access.redhat.com/ubi8/ubi-minimal:8.3
LABEL maintainer="Jose Angel Morena Simon"
#Add labels of OCP description etc. 
ENV TZ=Europe/Madrid
ENV HOME /code
ENV USER 1001
WORKDIR $HOME
ADD https://ftp.cixug.es/apache/tomcat/tomcat-9/v9.0.45/bin/apache-tomcat-9.0.45.tar.gz .
COPY start.sh .
RUN microdnf --setopt=tsflags=nodocs install -y java-1.8.0-openjdk-devel tar gzip && \
            microdnf reinstall tzdata -y && \
            microdnf clean all && \
            ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
            tar xvf apache-tomcat-9.0.45.tar.gz && \
            curl -L -o apache-tomcat-9.0.45/webapps/sample.war https://tomcat.apache.org/tomcat-9.0-doc/appdev/sample/sample.war && \
            chmod -R 755 $HOME && chown -R $USER:$USER $HOME
USER $USER
ENTRYPOINT [ "./start.sh"]


