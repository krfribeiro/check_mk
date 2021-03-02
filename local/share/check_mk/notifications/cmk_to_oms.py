#!/usr/bin/env python
import os, sys, time, subprocess, json, requests, datetime, hashlib, hmac, base64

# HTTP/HTTPS Proxies - If you need some ... #

os.environ["HTTP_PROXY"] = 'http://10.144.36.1:8080/'
os.environ["HTTPS_PROXY"] = 'https://10.144.36.1:8080/'

# OMS Related Variables #
customer_id = '66449870-a786-44f3-973e-dc9bf3f56a64'
shared_key = "dNtkVNvUmeaNSZMFW4iyRxrrmkuf7z12sdCiBKBTDN608/mVHxuOd6eqPbpRV/UhL+jKk+6wBcGzxKAlttYegw=="
log_type = 'TESTMKALERTS'

# OMS Related Functions #

# Build the API signature
def build_signature(customer_id, shared_key, date, content_length, method, content_type, resource):
    x_headers = 'x-ms-date:' + date
    string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
    bytes_to_hash = bytes(string_to_hash).encode('utf-8')
    decoded_key = base64.b64decode(shared_key)
    encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest())
    authorization = "SharedKey {}:{}".format(customer_id,encoded_hash)
    return authorization

# Build and send a request to the POST API
def post_data(customer_id, shared_key, body, log_type):
    method = 'POST'
    content_type = 'application/json'
    resource = '/api/logs'
    rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(body)
    signature = build_signature(customer_id, shared_key, rfc1123date, content_length, method, content_type, resource)
    uri = 'https://' + customer_id + '.ods.opinsights.azure.com' + resource + '?api-version=2016-04-01'

    headers = {
        'content-type': content_type,
        'Authorization': signature,
        'Log-Type': log_type,
        'x-ms-date': rfc1123date
    }

    response = requests.post(uri,data=body, headers=headers)
    if (response.status_code >= 200 and response.status_code <= 299):
        print 'Accepted'
    else:
        print "Response code: {}".format(response.status_code)

# MK Alert Handling #

# MK_HOSTNAME = os.environ['NOTIFY_HOSTNAME']
# MK_DESCRIPTION = os.environ['NOTIFY_SERVICEOUTPUT']
# MK_PLUGIN_OUTPUT = os.environ['NOTIFY_SERVICEDESC']
# MK_LAST_STATE_CHANGE = time.strftime("%Y-%m-%d %H:%M:%S")
# MK_SERVICESTATE = os.environ['NOTIFY_SERVICESTATE']

MK_HOSTNAME = "WSDPSCDB005"
MK_DESCRIPTION = "Memory utilization"
MK_PLUGIN_OUTPUT = "Memory is high"
MK_LAST_STATE_CHANGE = time.strftime("%Y-%m-%d %H:%M:%S")
MK_SERVICESTATE = "CRITICAL"

BASH_COMMAND="grep '%s;' mk_inventorydata | awk -F ';' '{print $2\",\"$3\",\"$4\",\"$5}'" % MK_HOSTNAME
NEW_INFO = subprocess.check_output(['bash','-c',BASH_COMMAND])

MK_HOST_IP = NEW_INFO.split(",")[0]
MK_DATACENTER = NEW_INFO.split(",")[1]
MK_TEAM = NEW_INFO.split(",")[2]
MK_VENDOR = NEW_INFO.split(",")[3].replace('\n','')

MK_JSON_OUTPUT = json.dumps([{'mk_hostname': MK_HOSTNAME, 'mk_description': MK_DESCRIPTION, 'mk_plugin_output': MK_PLUGIN_OUTPUT, 'mk_last_state_chage': MK_LAST_STATE_CHANGE, 'mk_servicestate': MK_SERVICESTATE, 'mk_host_ip': MK_HOST_IP, 'mk_team': MK_TEAM, 'mk_datacenter': MK_DATACENTER, 'mk_vendor': MK_VENDOR }])

post_data(customer_id, shared_key, MK_JSON_OUTPUT, log_type)