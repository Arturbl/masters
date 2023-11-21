FROM mysql:latest

MAINTAINER 'Artur Costa'

COPY init.sql /docker-entrypoint-initdb.d/

RUN chown -R mysql:root /var/lib/mysql/

EXPOSE 3306