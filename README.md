# FOG_server_using_API

Every request need to be authenticated. To do, we need two token: 
- **fog-user-token** located in user panel --> API settings --> user API token
- **fog-api-token** located in FOG configuration --> FOG settings --> API system
Remember to check in both cases the checkbox: API enabled

### GET request:
- GET all current task
- GET all image (instead image could be: host/task/group/history...)
- GET information of particular image using ID. (As said above, could be host/task ecc), all use the same form 
  
### POST request:
- CREATE an host by sending a JSON object

### DELETE request:
- DELETE a particular host

### SNAPIN
We need to send to the request a JSON object with this fields:
```
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
```
The minimum information needed is just the *taskTypeID*

### VIA COMMAND LINE

Two examples of operations done via command line:
- CREATE a snapin
- GET all current task and write them in a local JSON file


