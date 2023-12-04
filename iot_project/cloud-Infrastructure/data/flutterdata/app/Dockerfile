FROM instrumentisto/flutter:latest AS builder

RUN apt-get update
RUN apt-get install -y make
RUN apt-get clean

RUN mkdir /app/

COPY .. /app/
WORKDIR /app/

RUN rm -rf build
RUN make web-build

FROM nginx:1.21.0-alpine AS production

COPY --from=builder /app/build/web/ /usr/share/nginx/html/

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
