#!/usr/bin/python3
from requests.models import HTTPError
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
import json
import requests
from nornir_jinja2.plugins.tasks import template_file
from nornir.core.exceptions import NornirExecutionError

__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir(config_file="config.yml", core={"raise_on_error": True})

# Filter the hosts by the 'PE' router type.
pe_routers = nr.filter(type="PE_ROUTER")


def update_nso_devices(task):
    """This runbook will generate a Jinja2 Template to Add a device to
    our NSO instance."""

    # Generate device payload
    device = task.run(
        task=template_file,
        path="templates/nso",
        template="device_update.j2",
    )

    NSO = "192.168.0.105"
    url = f"http://{NSO}:8080/restconf/data"
    # url = "http://192.168.0.105:8080/restconf/data/tailf-ncs:devices"

    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }
    auth = ("admin", "admin")

    resp = requests.request(
        "POST",
        url=f"{url}/tailf-ncs:devices",
        auth=auth,
        headers=headers,
        data=device.result,
    )

    # Fail if response code is anything but 200/201.
    resp.raise_for_status()

def main():

    print_result(nr.run(task=update_nso_devices))


if __name__ == "__main__":
    main()
