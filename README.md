# FOG_server_using_API

This script discover which Virtual machines on Virtualbox are registered as an host on FOG server. After that, there is the possibility to turn it on/off.

The script is composed by three parts:
1) Get all hosts on FOG server: using *GET:/fog/host*
2) Get VM running on VirtualBox (necessary step for testing)
3) Get host registered in Fog server and installed in VirtualBox done by "mergeing" the two steps described above

After this set-up part, it's time to turn on/off VM.
I've done it by using task --> *POST: /fog/host/<id_host>/task*. I assumed that an empty snapin has already been created and has ID = 1 so as to avoid creating it every time.
- turn on: I inserted in JSON task the option **"wol":"true"**
- turn off: I inserted in JSON task the option  **"shutdown": "true"**

In function *turn on* and *turn off* comments there is a way to turn on/off Virtual machine using VBoxManage that is the command-line interface to Oracle VM VirtualBox. Used in the testing phase
