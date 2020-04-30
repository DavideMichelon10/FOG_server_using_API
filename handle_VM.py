#!/usr/bin/python3

import requests
import subprocess
import json


class VM(object):
    def __init__(self, vb_name):
        self.vb_name = vb_name


class FogHost(object):
    def __init__(self, id, name, mac):
        self.id = id
        self.name = name
        self.mac = mac


class HostInVBox(object):

    def __init__(self, id, name, vb_name, mac, status):
        self.name = name
        self.vb_name = vb_name
        self.mac = mac
        self.status = status
        self.id = id


# GET VirtualBox machine

def get_vm_name(vms):
    result_vms = subprocess.run(["VBoxManage", "list", "vms"], stdout=subprocess.PIPE)
    result = str(result_vms.stdout)
    i = 1
    is_quotation_mark = False
    is_first = False
    vm_name = ""

    while i < len(result):
        if result[i] == '"':
            if is_quotation_mark:
                is_quotation_mark = False
                vms.append(VM(vm_name))
                vm_name = ""
            else:
                is_quotation_mark = True
                is_first = True

        if is_quotation_mark and is_first == False:
            vm_name += result[i]

        is_first = False
        i += 1


def get_running_vm(vm, vb_name):
    result_vms = subprocess.run(["VBoxManage", "list", "runningvms"], stdout=subprocess.PIPE)
    result = str(result_vms.stdout)
    if vb_name in result:
        vm.status = 'ON'
    else:
        vm.status = 'OFF'


def get_vm_mac(vm, vb_name):
    result_vms = subprocess.run(["VBoxManage", "showvminfo", vb_name], stdout=subprocess.PIPE)
    result = str(result_vms.stdout)

    i = 0
    while i < len(result):
        if result[i] == "M" and result[i + 1] == "A" and result[i + 2] == "C":
            j = i + 5
            mac = ""
            while result[j] != ",":
                mac += str(result[j])
                j = j + 1
            vm.mac = mac
            break

        i += 1


def format_json(body):
    body = list(body)

    if body[0] == 'b':
        body[0] = ''

    if body[0] == "'":
        body[0] = ''

    if body[-3] == "n" and body[-4] == "\\":
        body[-3] = body[-4] = ''

    body = ''.join(body)

    i = 0
    while i < len(body):
        if body[i] == "<":
            string_to_delete = ''
            while body[i] != ">" and i < len(body):
                string_to_delete += body[i]
                i += 1

            string_to_delete += ">"
            body = body.replace(string_to_delete, '')
        i += 1

    body = list(body)
    if body[0] == "'":
        body[0] = ''

    if body[-1] == "'":
        body[-1] = ''

    return ''.join(body)


def vb_contain_fog_host(vm, fog_hosts, host_in_vb):
    for host in fog_hosts:
        if host.mac == vm.mac:
            host_in_vb.append(HostInVBox(host.id, host.name, vm.vb_name, host.mac, vm.status))


def check_input(msg):
    while True:
        choose = input(msg)
        if choose.upper() == "Y" or choose.upper() == "N":
            return choose
        else:
            print("Sorry, unrecognized character. Please, try again")


# I suppose I've already created an empty snapin with id = 1
def turn_off_vm(selected_host, headers, ip_address):
    print(selected_host.id)
    snapin_task = '{"taskTypeID":12,"taskName": "shutdown","shutdown": "true","deploySnapins": 1,"wol": "false" }'
    choose = check_input('Host selected is on. Would you like to turn off? [Y/n]')
    if choose.upper() != "N":
        requests.post(ip_address + '/fog/host/' + selected_host.id + '/task', headers=headers, data=snapin_task)
        print(selected_host.vb_name, " is turning off...")

        # subprocess.run(["VBoxManage", "controlvm", selected_host.vb_name, "poweroff", "--type", "headless"],
        # stdout=subprocess.PIPE)


# I suppose I've already created an empty snapin with id = 1
def turn_on_vm(selected_host, headers, ip_address):
    choose = check_input('Host selected is off. Would you like to turn on?[Y/n]')
    snapin_task = '{"taskTypeID":12,"taskName": "wake_up","shutdown": "false","deploySnapins": 1,"wol": "true" }'
    if choose.upper() != "N":
        requests.post(ip_address + '/fog/host/' + selected_host.id + '/task', headers=headers, data=snapin_task)
        print(selected_host.vb_name, " is turning on...")

        # subprocess.run(["VBoxManage", "startvm", selected_host.vb_name, "--type", "headless"],
        #               stdout=subprocess.PIPE)


def main():
    vms = []
    fog_hosts = []
    host_in_vb = []

    user_token = 'ZjZhMzM3MzcwYmU1YTAwYTIyODk3YWVkZWNiYjJlZjVlNDEzNWQzMWFkNWRjNmIzMzkyNjYwNzRkZTVhZjQ5YzEwOGY3NWFhMTVhYzBiZGI1NTdlYTFlZTRmZDA3NjRmOGM0MmM5NGUzZmExNjNhYjZkYjBhZDQ4ZmFmY2ZmYTY'
    api_token = 'NGMyMjc4YmU3ZTkwYzA5ZTY2OTIxMDZmOGZjY2MyOGM5NzM1ZjRiYzkxYjNlMTAxN2IzOWI4MTFjODE2Y2RhMDIwNGMxNTgxYjI1OWY4MzM0NTlhYjI3ZjI4OWQ2ZGQ2ZjFmYTNmODc3MWE1YjQ5NDgyYjNiNjVjZTc2NmZiZjQ '
    ip_address = 'http://192.168.1.111'
    headers = {'fog-user-token': user_token, 'fog-api-token': api_token}

    get_hosts = requests.get(ip_address + '/fog/host', headers=headers)
    body = str(get_hosts.content)

    formatted_body = format_json(body)

    body_json = json.loads(formatted_body)

    for x in body_json['hosts']:
        id = x['id']
        name = x['name']
        mac = x['macs'][0]
        mac = mac.replace(':', '')
        mac = mac.upper()
        fog_hosts.append(FogHost(id, name, mac))

    print()
    print("Hos registered on FOG server: ")
    for obj in fog_hosts:
        print("id:", obj.id, " name:", obj.name, "mac: ", obj.mac)

    get_vm_name(vms)
    for vm in vms:
        get_vm_mac(vm, vm.vb_name)
        get_running_vm(vm, vm.vb_name)

    print()
    print("VM installed on VirtualBox: ")
    for obj in vms:
        print("name:", obj.vb_name, " mac:", obj.mac, " status:", obj.status)

    for vm in vms:
        vb_contain_fog_host(vm, fog_hosts, host_in_vb)

    print()
    print("Host registered in Fog server and installed in VirtualBox: ")

    for vm_host in host_in_vb:
        print("id:", vm_host.id, " VBox name:", vm_host.vb_name, " mac:", vm_host.mac, " status:", vm_host.status)

    is_present = False
    while not is_present:
        id_selected = input("Choose on which host would you turn on/off: ")
        for vm_host in host_in_vb:
            if int(id_selected) == int(vm_host.id):
                selected_host = vm_host
                is_present = True

        if selected_host.status == 'ON':
            turn_off_vm(selected_host, headers, ip_address)
        else:
            turn_on_vm(selected_host, headers, ip_address)


main()
