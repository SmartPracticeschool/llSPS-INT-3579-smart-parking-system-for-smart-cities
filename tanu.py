import time
import sys
import ibmiotf.application
import ibmiotf.device
import random

#Provide your ibm watson device credentials

organization= "78z40p"
deviceType= "NodeMCU"
deviceId= "mcu123"
authMethod= "token"
authToken= "smartparking123"

# initialize GPIO

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)#command received from nodered
    print(type(cmd.data))
    i=cmd.data['command']
    if i== 'lighton':
        print("light is on")
    elif i== 'lightoff':
        print("light is off")
try:
         deviceOptions = {"org": organization, "type":deviceType, "id":deviceId, "auth-method":authMethod, "auth-token":authToken}
         #JSON format
         deviceCli= ibmiotf.device.Client(deviceOptions)
         #connecting the client

except Exception as e:
         print("Caught exception connecting device %s" %str(e))
         sys.exit()
         
deviceCli.connect()
#connecting to the patform

while True:

    enter=random.randint(1,40)
    exits=random.randint(1,40)
    available=random.randint(1,40)                     
#Send entry and exit status to ibm watson
    data={'Entry' : enter ,'Exit':exits,'Availableslots':available}
# print (data)
    def myOnPublishCallback():
        print("Publish Entries= %s" %enter,"Exits=%s " %exits,"Availableslots= %s" %available,"to IBM Watson")
#publish the data
    success=deviceCli.publishEvent("Smart Parking","json", data , qos=0, on_publish=myOnPublishCallback)
    if not success:
        print("Not connected to IOT")
        time.sleep(2)

        deviceCli.commandCallback = myCommandCallback
#subscribing

   #Disconnect the device and appication from cloud
deviceCli.disconnect()
