FROM python:3-alpine

RUN mkdir test
WORKDIR test

RUN pip3 install requests pytest pymongo docker pyyaml python-dateutil connexion
RUN pip3 install requests-jwt
RUN pip3 install python-jose

COPY test/test_pds_backend.py test_pds_backend.py
COPY txrouter txrouter
COPY debug debug
COPY api api

ENTRYPOINT ["pytest"]



