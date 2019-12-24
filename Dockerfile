FROM python:3-alpine

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
  gunicorn[gevent]==19.9.0 \
  pymongo \
  python-dateutil \
  python-jose[cryptography]

COPY api /usr/src/app/api
COPY txrouter /usr/src/app/txrouter
COPY sc.py /usr/src/app/sc.py

EXPOSE 8080

ENTRYPOINT ["gunicorn"]

CMD ["-w", "4", "-b", "0.0.0.0:8080", "-k", "gevent", "-c", "sc.py", "api.server:create_app()"]