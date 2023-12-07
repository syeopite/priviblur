FROM alpine:3.18

# Rust is needed for orjson
RUN apk add git python3 py3-pip rust cargo tini

RUN addgroup -g 1000 -S priviblur && \
    adduser -u 1000 -S priviblur -G priviblur

WORKDIR /priviblur

COPY ./.git/ ./.git/

COPY ./requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY ./src/ ./src/
COPY ./assets/ ./assets/
COPY ./locales/ ./locales/

RUN pybabel compile -d locales -D priviblur

EXPOSE 8000
USER priviblur
RUN git config --global --add safe.directory /priviblur
ENTRYPOINT [ "/sbin/tini", "--"]
CMD [ "python", "-m", "src.server" ]