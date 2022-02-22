from nornir import InitNornir
from nornir_jinja2.plugins.tasks import template_file
from nornir_scrapli.tasks import netconf_edit_config, netconf_unlock, netconf_lock, netconf_commit
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml




nr = InitNornir(config_file="/home/imad/Nornir-Automation/config.yaml")


def load_vars(task):


    host_data = task.run(task=load_yaml, file= f"/home/imad/Nornir-Automation/host_vars/{task.host}.yaml")
    task.host["facts"] = host_data.result

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

def config_lock(task):
    task.run(task=netconf_lock, target="candidate", name="Locking candidate Configuration")

def config_commit(task):
    task.run(task=netconf_commit, name="Committing candidate Configuration")

def config_unlock(task):
    task.run(task=netconf_unlock, target="candidate", name="Unlocking candidate Configuration")
    

def main():

    nr = InitNornir(config_file="/home/imad/Nornir-Automation/config.yaml")



    #lock = nr.run(task=config_lock) 
    #print_result(lock)

    var = nr.run(task=load_vars)
    print_result(var)
    

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
    

    commit_config = nr.run(task=config_commit)
    print_result(commit_config)

    #unlock = nr.run(task=config_unlock)
    #print_result(unlock)

if __name__ == "__main__":
    main()