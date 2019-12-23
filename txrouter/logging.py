import syslog
import time
import logging
import requests
from txrouter.utils import tstostr
from txrouter import plugin_config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


post_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
def l(event, source):
    def function_wrapper(func):
        def function_wrapped(*args, **kwargs):
            log(syslog.LOG_NOTICE, f"{event}_begin", timestamp(), source, *args, **kwargs)
            try:
                ret = func(*args, **kwargs)
                log(syslog.LOG_NOTICE, f"{event}_end", timestamp(), source, *args, ret=ret, **kwargs)
                return ret
            except Exception as e:
                log(syslog.LOG_ERR, f"{event}_exception", timestamp(), source, *args, exception=e, **kwargs)
                raise
        return function_wrapped
    return function_wrapper


def to_json(data):
    if data is None:
        return None
    if isinstance(data, dict):
        return {k: to_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_json(v) for v in data]
    elif isinstance(data, int) or isinstance(data, float) or isinstance(data, bool) or isinstance(data, str):
        return data
    else:
        return str(data)


def log(level, event, timestamp, source,*args, **kwargs):
    pc = plugin_config.get_plugin_config("logging")
    if pc is None:
        logger.log(logging.INFO, f"{level},{event},{timestamp},{source},{args},{kwargs}")
    else:
        requests.post("http://{host}:{port}/log".format(host=pc["name"], port=pc["port"]), headers=post_headers, json={
            "event": event,
            "level": str(level),
            "timestamp": timestamp,
            "source": source,
            "args": to_json(args),
            "kwargs": to_json(kwargs)
        })
    

def timestamp():
    return tstostr(time.time())


