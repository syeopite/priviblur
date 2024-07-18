FROM alpine:3.18 AS base

FROM base AS build

WORKDIR /priviblur

COPY ./.git/ ./.git/
COPY ./requirements.txt ./requirements.txt
COPY ./src/ ./src/
COPY ./assets/ ./assets/
COPY ./locales/ ./locales/

RUN apk add --no-cache py3-pip && \
    pip3 install --break-system-packages -r requirements.txt && \
    pybabel compile -d locales -D priviblur

FROM build

COPY --from=build /priviblur /priviblur
WORKDIR /priviblur

RUN apk add --no-cache python3 git tini && \
    addgroup -g 1000 -S priviblur && \
    adduser -u 1000 -S priviblur -G priviblur && \
    # chown is needed otherwise git will error out with "fatal: detected dubious ownership in repository at '/priviblur'"
    chown -R priviblur:priviblur /priviblur

EXPOSE 8000
USER priviblur
ENTRYPOINT [ "/sbin/tini", "--"]
CMD [ "python", "-m", "src.server" ]
