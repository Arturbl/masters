FROM mysql:latest
ENV LANG en_US.UTF-8

COPY init.sql /docker-entrypoint-initdb.d/

MAINTAINER Artur Costa
ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD admin
ENV POSTGRES_DB mysql
ENV PGDATA /var/lib/postgresql/data/
ENV TZ=UTC
EXPOSE 9876