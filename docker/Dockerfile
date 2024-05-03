FROM alpine:3.18
WORKDIR /priviblur

COPY ./.git/ ./.git/
COPY ./requirements.txt ./requirements.txt
COPY ./src/ ./src/
COPY ./assets/ ./assets/
COPY ./locales/ ./locales/

# Rust is needed for orjson
RUN apk add --no-cache git python3 py3-pip rust cargo tini && \
    addgroup -g 1000 -S priviblur && \
    adduser -u 1000 -S priviblur -G priviblur && \
    pip3 install --break-system-packages -r requirements.txt && \
    pybabel compile -d locales -D priviblur && \
    chown -R priviblur:priviblur /priviblur && \
    git config --global --add safe.directory /priviblur

EXPOSE 8000
USER priviblur
ENTRYPOINT [ "/sbin/tini", "--"]
CMD [ "python", "-m", "src.server" ]
