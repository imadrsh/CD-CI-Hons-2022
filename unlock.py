from nornir import InitNornir
from nornir_jinja2.plugins.tasks import template_file
from nornir_scrapli.tasks import netconf_edit_config, netconf_unlock, netconf_lock, netconf_commit
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml


nr = InitNornir(config_file="/home/imad/Nornir-Automation/config.yaml")


def config_unlock(task):
    task.run(task=netconf_unlock, target="candidate", name="Unlocking candidate Configuration")




unlock = nr.run(task=config_unlock)
print_result(unlock)