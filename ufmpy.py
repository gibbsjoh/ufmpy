# set of functions to connect to and work with the FileMaker Data API from MicroPython

import urequests
import ubinascii
import json

# set server name, creds, API endpoints
# for the moment, the server is defind here
# tbd in future version - pass the server etc as parameters
fmServer = "https://fmserver.example.com"
accountName = "dataapi"
password = "password"

# the username/password is passed as username:password, Base64 encoded
creds = accountName + ":" + password
credsEncoded = ubinascii.b2a_base64(creds).strip()
credsEncoded = credsEnc.decode('utf-8')

# solution name and api version
solutionName = "HomeList"
apiVersion = "v1"

##################################################################

# define functions
####################################
# get token for specified solution #
####################################
def fmGetToken(solutionName):
    theEndpoint = "/fmi/data/" + apiVersion + "/databases/" + solutionName + "/sessions"
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
    theEndpoint = "/fmi/data/" + apiVersion + "/databases/" + solutionName + "/layouts/" + theLayout + "/_find"
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
