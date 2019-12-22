[![Build Status](https://travis-ci.com/RENCI/pds-backend.svg?token=hSyYs1SXtzNJJDmjUzHi&branch=master)](https://travis-ci.com/RENCI/pds-backend)

# pds-backend

## how to deploy

### set port

The default port is `8080`, if you want to change the port, update in `.env` file `API_PORT`.

### run command

#### unsecure mode
##### start `pds-backend` 
```
docker-compose -f docker-compose.yml -f nginx/unsecure/docker-compose.yml up --build -d -V
```

##### stop `pds-backend`
```
docker-compose -f docker-compose.yml -f nginx/unsecure/docker-compose.yml down -t <timeout>
```

set `<timeout>` to a longer time to prevent time out before graceful shutdown

#### secure mode
##### start `pds-backend` 

modify `.env`:

set the `JWT_SECRET` variable to a string

set `SSL_CERT_DIR` to a directory containing `cert.pem` and `key.pem`

```
docker-compose -f docker-compose.yml -f nginx/secure/docker-compose.yml up --build -d -V
```

##### stop `pds-backend`
```
docker-compose -f docker-compose.yml -f nginx/secure/docker-compose.yml down -t <timeout>
```

## plugin configuration format
```
{
  "image": docker image,
  "name": name,
  "port": port,
  "environment": environment,
  "volumes": [ {
    "source": source path,
    "target": target path,
    "type": type,
    "read_only": read only
  } ],
  depends_on: [ service ]
}
```

## plugin configuration format for INIT_PLUGIN_PATH
`.yaml` or `.yml`

```
services:
  <name>:
    image: <docker image>
    port: <port>
    environment: <environment>
    volumes:
      - source: <source path>
        target: <target path>
        type: <type>
        read_only: <read only>
    depends_on:
      - <service>
volumes:
  <name>:
    persistent: <persistent>
```

## test
```
./test.sh
```
