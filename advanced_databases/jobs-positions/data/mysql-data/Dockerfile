FROM mysql:latest
ENV LANG en_US.UTF-8

COPY init.sql /docker-entrypoint-initdb.d/
LABEL maintainer="Artur Costa"

ENV TZ=UTC
EXPOSE 3306

CMD ["mysqld"]
