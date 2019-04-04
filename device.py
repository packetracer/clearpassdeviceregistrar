#!/usr/bin/python
import cgi
import requests
import json

form = cgi.FieldStorage()
ip = form.getvalue('ip')
name = form.getvalue('name')
desc = form.getvalue('desc')
dtype = form.getvalue('dtype')

#Clearpass URLs
CPPMURL = 'https://cppmhostname/api/oauth'
DEVICEURL = 'https://cppmhostname/api/network-device'

def authMe():
        body = {
          "grant_type": "client_credentials",
          "client_id": 'CLIENT ID HERE',
          "client_secret": 'CLIENT SECRET HERE'
        }
        response = requests.post(CPPMURL, data=body, verify=False)
        if response.status_code == 200:
                headers = {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer {}".format(json.loads(response.text)['access_token'])
                }
                return (headers)
        else:
                return "FAILURE"
#MAKE SURE TO PUT YOUR PROPER SECRETS AND VENDORS HERE
def createDevice(headers):
        body = {
          "description": "{}".format(desc),
          "name": "{}".format(name),
          "ip_address": "{}".format(ip)
        }
        if dtype == "APC":
                body.update({"radius_secret": "APCSECRET,"vendor_name":"APC","attributes":{"sysName":"APC"}})
        if dtype == "SW":
                body.update({"radius_secret":"SWITCHSECRET","tacacs_secret":"SWITCHSECRET","vendor_name":"VENDORNAME","attributes":{"sysName":"SW"}})
        if dtype == "RTR":
                body.update({"radius_secret":"ROUTERSECRET","tacacs_secret":"ROUTERSECRET","vendor_name":"VENDORNAME","attributes":{"sysName":"RTR"}})
        if dtype == "OTHER":
                body.update({"radius_secret":"NONE","vendor_name":"IETF"})
        response = requests.post(DEVICEURL, data=json.dumps(body), headers=headers, verify=False)
        return response
