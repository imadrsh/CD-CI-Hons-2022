import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
import json
from nornir.core.filter import F
from ipaddress import ip_network, ip_address


nr = InitNornir(config_file="/home/imad/Nornir-Automation/config.yaml")

target = input("Enter the target IP: ")
ipaddr = ip_address(target)
my_list = []

def get_cisco(task):
    """
    Parse routing table and determine if target IP finds a match
    """
    response = task.run(task=send_command, command="show ip route")
    task.host["facts"] = response.scrapli_response.genie_parse_output()
    prefixes = task.host["facts"]["vrf"]["default"]["address_family"]["ipv4"]["routes"]
    for prefix in prefixes:
        net = ip_network(prefix)
        if ipaddr in net:
            source_proto = prefixes[prefix]["source_protocol"]
            if source_proto == "connected":
                try:
                    outgoing_intf = prefixes[prefix]["next_hop"]["outgoing_interface"]
                    for intf in outgoing_intf:
                        exit_intf = intf
                        my_list.append(
                            f"{task.host} is connected to {target} via interface {exit_intf}"
                        )
                except KeyError:
                    pass

nr.run(task=get_cisco)
import ipdb
ipdb.set_trace()

#pp nr.inventory.hosts["R1"]["facts"]["vrf"]["default"]["address_family"]["ipv4"]["routes"]


def configure_interface(task):
    template_to_load = task.run(task=template_file, template="interface.j2",path="/home/imad/Nornir-Automation/templates")
    configuration = template_to_load.result
    task.run(task=netconf_edit_config, target="candidate", config=configuration)

def configure_router(task):
    template_to_load = task.run(task=template_file, template="router.j2",path="/home/imad/Nornir-Automation/templates")
    configuration = template_to_load.result
    task.run(task=netconf_edit_config, target="candidate", config=configuration)

def configure_ntp(task):
    template_to_load = task.run(task=template_file, template="ntp.j2",path="/home/imad/Nornir-Automation/templates")
    configuration = template_to_load.result
    task.run(task=netconf_edit_config, target="candidate", config=configuration)

def configure_ip(task):
    template_to_load = task.run(task=template_file, template="ip.j2",path="/home/imad/Nornir-Automation/templates")
    configuration = template_to_load.result
    task.run(task=netconf_edit_config, target="candidate", config=configuration)

def configure_line(task):
    template_to_load = task.run(task=template_file, template="line.j2",path="/home/imad/Nornir-Automation/templates")
    configuration = template_to_load.result
    task.run(task=netconf_edit_config, target="candidate", config=configuration)


        config = nr.run(task=configure_router)
    print_result(config)

    config = nr.run(task=configure_interface)
    print_result(config)

    config = nr.run(task=configure_ntp)
    print_result(config)

    config = nr.run(task=configure_ip)
    print_result(config)

    config = nr.run(task=configure_line)
    print_result(config)