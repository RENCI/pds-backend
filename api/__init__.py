import requests
from txrouter import plugin_config, plugin
from txrouter.logging import l
import logging
import connexion
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@l("get", "backend")
def get_plugin(name, path, headers, kwargs={}):
    pc = plugin_config.get_plugin_config(name)
    if pc is None:
        return "not found", 404
    
    port = pc.get("port", None)
    if port is None:
        raise RuntimeError("plugin doesn't have port")

    resp = requests.get("http://{host}:{port}/{path}".format(host=pc["name"], port=port, path=path), headers=headers, params=kwargs, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()


@l("post", "backend")
def post_plugin(name, path, headers, body, kwargs={}):
    pc = plugin_config.get_plugin_config(name)
    if pc is None:
        return "not found", 404

    port = pc.get("port", None)
    if port is None:
        raise RuntimeError("plugin doesn't have port")

    resp = requests.post("http://{host}:{port}/{path}".format(host=pc["name"], port=port, path=path), headers=headers, params=kwargs, json=body, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()


def get_plugin_config(name):
    pc = plugin_config.get_plugin_config(name)
    pc["_id"] = str(pc["_id"])
    return pc


def fil(name, name_regex):
    fils = []
    if name_regex is not None:
        fils.append({"name": {"$regex": name_regex}})
    if name is not None:
        fils.append({"name": name})
    if len(fils) == 0:
        return {}
    else:
        return {"$and": fils}


def get_plugin_configs(name=None, name_regex=None):
    ps = plugin_config.get_plugin_configs(fil(name, name_regex))
    for pc in ps:
        pc["_id"] = str(pc["_id"])

    return ps


def add_plugin_configs(body):
    pc = plugin_config.add_plugin_configs(body)
    return len(pc)


def delete_plugin_config(name=None, name_regex=None):
    return delete_plugin_configs(name=name, name_regex=name_regex)


def delete_plugin_configs(name=None, name_regex=None):
    return plugin_config.delete_plugin_configs(fil(name, name_regex))


def update_plugin_config(name, body):
    plugin_config.replace_plugin_config(name, body)


def get_plugin_container(name):
    pc = plugin_config.get_plugin_config(name)
    container = plugin.get_container(pc)
    if container is not None:
        return {
            "status": container.status
        }
    else:
        return None


def add_plugin_container(name):
    pc = plugin_config.get_plugin_config(name)
    plugin.run_container(pc)


def delete_plugin_container(name):
    pc = plugin_config.get_plugin_config(name)
    plugin.stop_container(pc)
    plugin.remove_container(pc)


def get_containers():
    containers = []
    for pc in plugin_config.get_plugin_configs({}):
        container = plugin.get_container(pc)
        if container is not None:
            cs = {
                "status": container.status
            }
        else:
            cs = None

        containers.append({
            "name": pc["name"],
            "container": cs
        })
    return containers


def add_containers():
    for pc in plugin_config.get_plugin_configs({}):
        plugin.run_container(pc)


def delete_containers():
    for pc in plugin_config.get_plugin_configs({}):
        plugin.stop_container(pc)
        plugin.remove_container(pc)
