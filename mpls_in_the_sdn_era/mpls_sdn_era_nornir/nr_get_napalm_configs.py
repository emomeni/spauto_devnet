#!/usr/bin/python3
"""Extract configuration from devices using NAPALM.

We loop through our inventory and get data from the devices based on task.host.
"""

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file

__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")


def get_device_facts(task):
    """Extract configuration from devices with NAPALM's help."""
    facts = task.run(task=napalm_get, getters="get_facts")
    # Store config in host_vars
    task.host["facts"] = facts.result


def write_facts(task):
    """Dump facts to file."""
    facts = task.host["facts"]

    write_file(
        task, filename=f"napalm_facts/AS65000/{task.host}.cfg", content=str(facts)
    )


def main():
    """Execute the nornir runbook."""
    print_result(nr.run(task=get_device_facts))
    print_result(nr.run(task=write_facts))


if __name__ == "__main__":
    main()
