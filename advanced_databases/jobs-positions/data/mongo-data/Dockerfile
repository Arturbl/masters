FROM mongo:latest

ENV LANG en_US.UTF-8
ENV TZ=UTC

COPY init.js /docker-entrypoint-initdb.d/

LABEL maintainer="Artur Costa"

EXPOSE 27017
