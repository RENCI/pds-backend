[![Build Status](https://travis-ci.com/RENCI/tx-router.svg?branch=master)](https://travis-ci.com/RENCI/tx-router)

# tx-router

## how to deploy

### set port

The default port is `8080`, if you want to change the port, set it with environmental variable `TXROUTER_API_PORT`.

### run command

#### unsecure mode
##### start `tx-router` 
```
docker-compose -f docker-compose.yml -f nginx/unsecure/docker-compose.yml up --build -d -V
```

##### stop `tx-router`
```
docker-compose -f docker-compose.yml -f nginx/unsecure/docker-compose.yml down -t <timeout>
```

set `<timeout>` to a longer time to prevent time out before graceful shutdown

#### secure mode
##### start `tx-router` 

set environmental variables, see test/env.src for examples.

```
docker-compose -f docker-compose.yml -f nginx/secure/docker-compose.yml up --build -d -V
```

##### stop `tx-router`
```
docker-compose -f docker-compose.yml -f nginx/secure/docker-compose.yml down -t <timeout>
```
## How to configure

The system can be a router for any kind of plugin

### logging

A logger is a special kind of plugin.

If a logging plugin is not defined, messages will:
* be routed to the "Logging facility for Python"
* have the following format:
```
{level},{event},{timestamp},{source},{args},{kwargs}
```
* be output to the console
* use logging levels defined by the set of configured plugins, not by the "Logging facility for Python" plugin.

### plugin configuration format for INIT_PLUGIN_PATH

__For this release, all plugins must be a deployable docker container that also implements an OpenAPI__

## plugin configuration format for ${INIT_PLUGIN_PATH}

See test/env.src for example path value

`.yaml` or `.yml`:

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
## How to use

### Plugin configuration format used dynamically

__For this release, all plugins must be a deployable docker container that also implements an OpenAPI__

Plugin configuration is read from a yaml file, and thereafter passed  to functions and RESTful APIs, as JSON.

e.g., /v1/admin endpoints described by api/openapi/my_api.yaml accept the JSON format of the plugin configuration. See #/components/schemas/PluginConfig in the my_api.yaml for more detail.

As a further example, the plugin functions in txrouter/plugin.py use the same JSON format for describing plugin configuration.

Following is the format of a dynamic plugin configuration:
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

### Custom Environmental Variables

The following can be set directly in the docker-compose.yml file or use the environmental variables in the example dockerfile

*_COMPOSE_PROJECT_NAME_: user-defined docker "bridge" network is defined from this variable: "${COMPOSE_PROJECT_NAME}_default"
*_INIT_PLUGIN_PATH_: path to the yml files for the plugins. See the pds-plugin repo for examples
*_JWT_SECRET_: set to any secure string
*_SSL_CERT_DIR_: to a directory containing `cert.pem` and `key.pem`
*_MONGO_*_: varibles for using the MONGO database instance. Can be anything, pick something secure:
 - MONGO_HOST
 - MONGO_PORT
 - MONGO_DATABASE
 - MONGO_NON_ROOT_USERNAME
 - MONGO_NON_ROOT_PASSWORD

## test
```
./test.sh
```
