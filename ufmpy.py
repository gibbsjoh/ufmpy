# set of functions to connect to and work with the FileMaker Data API from MicroPython

import urequests
import ubinascii
import json
import ujson
import utime
import re

# set server name, creds, API endpoints
# for the moment, the server is defind here
# tbd in future version - pass the server etc as parameters
fmServer = "https://fmserver.smthng.pw"
accountName = "dataapi"
password = "0ccur4nc3!"

adminAccount = "admin"
adminPassword = "dance200"

# the username/password is passed as username:password, Base64 encoded
creds = accountName + ":" + password
credsEncoded = ubinascii.b2a_base64(creds).strip()
credsEncoded = credsEncoded.decode('utf-8')

adminCreds = adminAccount + ":" + adminPassword
adminCredsEncoded = ubinascii.b2a_base64(adminCreds)
adminCredsEncoded = adminCredsEncoded.decode('utf-8').strip()

# solution name and api version
solutionName = "HomeList"
apiVersion = "v1"

##################################################################

# define functions
####################################
# get Admin API Token              #
####################################
def fmGetAdminToken():
    theEndpoint = "/fmi/admin/api/v2/user/auth"
    authString ="Basic " + str(adminCredsEncoded)
    #print (authString)
    # FMS seems to need an empty data payload and a Content-Length header, so we do that here:
    data = json.dumps({}).encode('utf-8')
    contentLength = len(data)

    # define the URL
    url = fmServer + theEndpoint

    # set the headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": authString,
        "Content-Length": "0"
    }
    # Properly format headers as a JSON string
    headers_json = ujson.dumps(headers)

    # # query the enpoint
    response = urequests.post(url, headers=ujson.loads(headers_json))

    # Check the response
    if response.status_code == 200:
        theResponse = response.json()
        theToken = theResponse["response"]["token"]
        return str(theToken)
    else:
        return ("Error ", response.status_code)
    # END of Function

######################################
# Get the server info from Admin API #
######################################
def fmGetServerInfo(theToken):
    # returns server metadata:
    # "serverName": "localhost",
    #"serverID": "3EAE027BD85CFF61ACB745A7B04D6D8AEA5263EE8604C7E8CFBD1B3BDACE7F26",
    #"serverIP": "192.168.1.1",
    #"serverVersion": "19.0.1.103",
    #"serverHostTime": "2023-01-01T08:05:01"
    # define the endpoint
    theEndpoint = "/fmi/admin/api/v2/server/metadata"
    url = fmServer + theEndpoint

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + theToken,
        "Content-Length": "0"
    }
    # Properly format headers as a JSON string
    headers_json = ujson.dumps(headers)

    response = urequests.get(url, headers=ujson.loads(headers_json))

    # Check and return the response
    if response.status_code == 200:
        theResponse = response.json()
        return theResponse
    else:
        return response.status_code

##########################################################
# Invalidate the token (so we don't run into api limits) #
#########################################################
def fmInvalidateAdminToken(theToken):
    theEndpoint = "/fmi/admin/api/v2/user/auth/" + theToken
    url = fmServer + theEndpoint

    headers = {
        "Content-Type": "application/json",
        "Content-Length": "0"
    }
    # Properly format headers as a JSON string
    headers_json = ujson.dumps(headers)

    response = urequests.delete(url, headers=ujson.loads(headers_json))

    # Check and return the response
    if response.status_code == 200:
        theResponse = response.json()
        return theResponse
    else:
        return response.status_code


####################################
# get token for specified solution #
####################################
def fmGetToken(solutionName):
    theEndpoint = "/fmi/data/" + apiVersion + "/databases/" + solutionName + "/sessions"
    authString = "Basic " + str(credsEncoded)
    # FMS seems to need an empty data payload and a Content-Length header, so we do that here:
    data = json.dumps({}).encode('utf-8')
    contentLength = len(data)

    # define the URL
    url = fmServer + theEndpoint

    # set the headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": authString,
        "Content-Length": str(contentLength)
    }

    # query the enpoint
    response = urequests.post(url, headers=headers, data=data)

    # Check the response
    if response.status_code == 200:
        theResponse = response.json()
        theToken = theResponse["response"]["token"]
        return theToken
    else:
        return response.status_code
    # END of Function

##################################################
# Get a current timestamp as dd/mm/yyyy hh:mm:ss #
##################################################
def currentTimestamp():
    timestampNow = "{:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}".format(
        timestamp[2], timestamp[1], timestamp[0],  # Day, Month, Year
        timestamp[3], timestamp[4], timestamp[5]   # Hour, Minute, Second
    )
    return timestampNow
    # END of currentTimestamp function

#####################################
# perform a find and return results #
#####################################
def fmPerformFind(theSolution, theLayout, theQuery, theToken):
    # lots of params here, all self explanatory. needs the token we got from the function above
    # define the endpoint
    theEndpoint = "/fmi/data/" + apiVersion + "/databases/" + theSolution + "/layouts/" + theLayout + "/_find"
    url = fmServer + theEndpoint

    # example query with sort, see https://help.claris.com/en/data-api-guide/content/perform-find-request.html
    # query = {
    # "query": [
    #     {"Field1": "Value1"},
    # ],
    # "sort": [
    #     {"fieldName": "CreationTimestamp", "sortOrder": "ascend"},
    # ]
    # }

    data = json.dumps(theQuery).encode('utf-8')
    contentLength = len(data)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + theToken,
        "Content-Length": str(contentLength)
    }

    response = urequests.post(url, headers=headers, data=data)

    # Check and return the response
    if response.status_code == 200:
        theResponse = response.json()
        return theResponse
    else:
        return response.status_code

########################################
# modify a specific record by recordid #
########################################
def editRecord(theSolution, theLayout, theRecordID, thePayload, theToken):
    # lots of params here, all self explanatory. needs the token we got from the function above
    # define the endpoint
    theEndpoint = "/fmi/data/" + apiVersion + "/databases/" + theSolution + "/layouts/" + theLayout + "/records/" + theRecordID
    url = fmServer + theEndpoint

    data = json.dumps(thePayload).encode('utf-8')
    contentLength = len(data)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + theToken,
        "Content-Length": str(contentLength)
    }

    response = urequests.patch(url, headers=headers, data=data)

    # Check and return the response
    if response.status_code == 200:
        theResponse = response.json()
        return theResponse
    else:
        return response.status_code

#########################
# create a new record   #
#########################
def createRecord(theSolution, theLayout, thePayload, theToken):
    # lots of params here, all self explanatory. needs the token we got from the function above
    # define the endpoint
    theEndpoint = "/fmi/data/" + apiVersion + "/databases/" + theSolution + "/layouts/" + theLayout + "/records"
    url = fmServer + theEndpoint

    data = json.dumps(thePayload).encode('utf-8')
    contentLength = len(data)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + theToken,
        "Content-Length": str(contentLength)
    }

    response = urequests.post(url, headers=headers, data=data)

    # Check and return the response
    if response.status_code == 200:
        theResponse = response.json()
        return theResponse
    else:
        return response.status_code
    
##################################
# Invalidate the Data API token  #
##################################
def fmInvalidateDAPIToken(theDatabase,theToken):
    theEndpoint = "/fmi/data/v1/databases/" + theDatabase + "/sessions/" + theToken
    url = fmServer + theEndpoint

    headers = {
        "Content-Type": "application/json",
        "Content-Length": "0"
    }
    # Properly format headers as a JSON string
    headers_json = ujson.dumps(headers)

    response = urequests.delete(url, headers=ujson.loads(headers_json))

    # Check and return the response
    if response.status_code == 200:
        theResponse = response.json()
        return theResponse
    else:
        return response.status_code
