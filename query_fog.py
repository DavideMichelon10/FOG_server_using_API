import requests

##HOW TO get tokens from aplication:

#usertoken: user --> API settings --> user API token
#apitoken: FOG configuration --> FOG settings --> API system
#REmbember to check in both cases the checkbox: API enabled

usertoken='usertoken'
apitoken='apitoken'
ip_address='http://192.168.1.1'
headers = {'fog-user-token': usertoken, 'fog-api-token':apitoken }


###GET REQUEST

#current task
r = requests.get(ip_address+'/fog/task/current', headers=headers)

#all image/task/host/group/ipxe/snapin...
r = requests.get(ip_address+'/fog/image', headers=headers)

#information of particular image. 6 is the ID while image could be host/task/group/history...
r = requests.get(ip_address+'/fog/image/6', headers=headers)


###POST REQUEST
#Create an host
date='{ "id": "11232", "name": "ssdfg", "description": "asd", "ip": "", "imageID": "6", "building": "0", "createdTime": "2020-04-20 07:56:13", "deployed": "0000-00-00 00:00:00", "createdBy": "fog", "useAD": "", "ADDomain": "", "ADOU": "", "ADUser": "", "ADPass": "", "ADPassLegacy": "", "productKey": "", "printerLevel": "", "kernelArgs": "", "kernel": "", "kernelDevice": "", "init": "", "pending": "", "pub_key": "", "sec_tok": "", "sec_time": "0000-00-00 00:00:00", "pingstatus": "<i class=\\"icon-ping-down fa fa-exclamation-circle red\\" data-toggle=\\"tooltip\\" data-placement=\\"right\\" title=\\"Unknown\\"><\\/i>", "biosexit": "", "efiexit": "", "enforce": "", "primac": "08:00:27:f7:ee:a4", "imagename": "ubuntu_three", "hostscreen": { "id": "", "hostID": "", "width": "", "height": "", "refresh": "", "orientation": "", "other1": "", "other2": "" }, "hostalo": { "id": "", "hostID": "", "time": "" }, "inventory": { "id": "7", "hostID": "7", "primaryUser": "", "other1": "", "other2": "", "createdTime": "2020-04-20 07:56:13", "deleteDate": "0000-00-00 00:00:00", "sysman": "innotek GmbH", "sysproduct": "VirtualBox", "sysversion": "1.2", "sysserial": "0", "sysuuid": "8c1d5ae6-01b1-4c89-9e83-ae093ccf8d2a", "systype": "Type: Other", "biosversion": "VirtualBox", "biosvendor": "innotek GmbH", "biosdate": "12\\/01\\/2006", "mbman": "Oracle Corporation", "mbproductname": "VirtualBox", "mbversion": "1.2", "mbserial": "0", "mbasset": "Not Specified", "cpuman": "", "cpuversion": "", "cpucurrent": "", "cpumax": "", "mem": "MemTotal: 1982308 kB", "hdmodel": "VBOX HARDDISK", "hdserial": "VB3494c222-e8951cc8", "hdfirmware": "1.0", "caseman": "Oracle Corporation", "casever": "Not Specified", "caseserial": "Not Specified", "caseasset": "Not Specified", "memory": "1.89 GiB" }, "image": { "imageTypeID": "1", "imagePartitionTypeID": "1", "id": "6", "name": "ubuntu_three", "description": "", "path": "ubuntu_three", "createdTime": "2020-04-20 07:42:36", "createdBy": "fog", "building": "0", "size": "1717240.000000:7033815040.000000:", "osID": "50", "deployed": "2020-04-20 08:07:33", "format": "0", "magnet": "", "protected": "0", "compress": "6", "isEnabled": "1", "toReplicate": "1", "srvsize": "1789709861", "os": {}, "imagepartitiontype": {}, "imagetype": {} }, "macs": [ "07:10:17:f7:ee:a4" ]}'
r = requests.post(ip_address+'/fog/host/create', headers=headers, data=date)


###DELETE REQUEST
#Delete an host
r = requests.delete(ip_address+'/fog/host/11', headers=headers)

r = requests.get(ip_address+'/fog/host', headers=headers)



###FOCUS ON SNAPIN
new_snapin= '{ "id": "112", "name": "test_from_python", "description": "", "file": "script.sh", "args": "", "createdTime": "2020-04-20 09:23:12", "createdBy": "fog", "reboot": "", "shutdown": "1", "runWith": "\\/bin\\/bash", "runWithArgs": "", "protected": "0", "isEnabled": "1", "toReplicate": "1", "hide": "0", "timeout": "0", "packtype": "0", "hash": "2a1826cdf6d0465c2f03590ce485a53a205ca24187a6fb4833c111b68ee0cb3hjhe31f3496d7a1561772b0855b88c0f569cfa071845ef7dd4a562d1a48f72a2fa6a", "size": "74", "anon3": "", "storagegroupname": "default"}'
#r = requests.post(ip_address+'/fog/snapin/create', headers=headers, data=new_snapin)


#To create a snapin task, we need:
#snapin ID = 4
#host ID = 7
#URL TO CALL: POST --> http://192.168.1.1/fog/host/7/task
#SNAPIN TASK:
'''
snapin_task={
    "taskTypeID": <IDOFTASKTYPE>,
    "taskName": "NameToGiveTasking",
    "shutdown": <bool>true/false,
    "debug": <bool>true/false,
    "deploySnapins": <bool>/<IDOFSNAPIN or -1 for all>,
    "passreset": "what to change password if passreset task",
    "sessionjoin": "<SessionNameToJoin>",
    "wol": <bool>
}
'''
#taskTypeID: to find out which one use: get in mysql --> fog DB --> select ttID, ttName, ttType from taskTypes;
# 3 = DEBUG
# 13 = SINGLE SNAPIN
# 14 = WAKE UP
snapin_task = '{"taskTypeID":12,"taskName": "test_python","shutdown": "true","deploySnapins": 4,"wol": "true" }'


r = requests.post(ip_address+'/fog/host/7/task', headers=headers, data=snapin_task)


#VIA COMMAND LINE

#curl -H 'fog-api-token: apitoken' -H 'fog-user-token: usertoken' -X GET http://192.168.1.1/fog/task/current -o listalltasks.json
#curl -H 'fog-api-token: apitoken' -H 'fog-user-token: usertoken' -H 'Content-Type: application/json' -X POST -d '{"taskTypeID":12,"deploySnapins":4}' http://192.168.1.1/fog/host/7/task


