FROM python:3-alpine

RUN mkdir test
WORKDIR test

RUN pip3 install \
  connexion \
  docker \
  pymongo \
  pytest \
  python-dateutil \
  pyyaml \
  requests

RUN pip3 install requests-jwt
RUN pip3 install python-jose

COPY test/test_tx_router.py test_tx_router.py
COPY txrouter txrouter
COPY debug debug
COPY api api

ENTRYPOINT ["pytest"]



