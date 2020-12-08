FROM python:3.8-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk add \
  gcc \ 
  libffi-dev \
  musl-dev \
  openssl-dev

RUN pip3 install --no-cache-dir \
  connexion \
  docker \
  flask-cors \
  get_docker_secret==1.0.1 \
  gevent==20.9.0
  gunicorn[gevent]==20.0.4 \
  pymongo \
  python-dateutil \
  python-jose[cryptography]

COPY api /usr/src/app/api
COPY tx /usr/src/app/tx
COPY tx-utils/src /usr/src/app
COPY sc.py /usr/src/app/sc.py

EXPOSE 8080

ENTRYPOINT ["gunicorn"]

CMD ["-w", "4", "-b", "0.0.0.0:8080", "-k", "gevent", "-c", "sc.py", "api.server:create_app()"]
