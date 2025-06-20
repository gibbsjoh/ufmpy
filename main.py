# MicroPython script to get data from FileMaker Server via data api and display on I2C LCD

import ufmpy
import ujson
lcd.clear()

## demo to get server info, then query a database
whatToDo = "solution"

if(whatToDo == "solution"):
    lcd.putstr("Getting FMS Token")
    token = ufmpy.fmGetToken("HomeList")

    if (token[:5] != "Error"):
        #do other stuff here
        print("success!")
        haveToken = 1
        sleep(2)
        lcd.clear()
        lcd.putstr("Got token!")
    else:
        haveToken = 0
        print(token)

    if (haveToken == 1):
        #query database
        theQuery = {
            "query": [
                {"AppName": "Netflix"},
            ],
            "sort": [
                {"fieldName": "AppName", "sortOrder": "ascend"},
            ]
        }
        theResult = ufmpy.fmPerformFind("HomeList", "dataapi_APPS", theQuery, token)
        print(theResult)
        # get the record ID
        theRecordID = theResult["response"]["data"][0]["recordId"]
        print(theRecordID)
        sleep(3)
        # edit the record
        thePayload = {"fieldData":{"zz_Dummy1":"I love MicroPython"}}
        theResult = ufmpy.editRecord("HomeList", "dataapi_APPS", theRecordID, thePayload, token)
        print(theResult)
    
    # edit a record

elif(whatToDo == "admin"):
    lcd.putstr("Getting token..")
    adminToken = ufmpy.fmGetAdminToken()
    sleep(3)
    lcd.move_to(0,1)
    lcd.putstr("Got Token!")
    #print("Get token result:")
    #print(adminToken)
    # get the server name and version
    sleep(3)
    lcd.clear()
    metaData = ufmpy.fmGetServerInfo(adminToken)
    theName = metaData["response"]["ServerName"]
    theVersion = metaData["response"]["ServerVersion"]
    lcd.putstr(theName)
    lcd.move_to(0,1)
    lcd.putstr(theVersion)
    sleep(5)
    #print(theName, " ", theVersion)
    # kill the token
    killToken = ufmpy.fmInvalidateAdminToken(adminToken)
    print("Invalidate Token result: ", ujson.dumps(killToken))

