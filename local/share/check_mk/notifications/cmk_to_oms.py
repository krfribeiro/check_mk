#!/usr/bin/env python
import os, sys, time, subprocess, json, requests, datetime, hashlib, hmac, base64

# OMS Related Variables #
customer_id = os.environ['NOTIFY_PARAMETER_1']
shared_key = os.environ['NOTIFY_PARAMETER_2']
log_type = os.environ['NOTIFY_PARAMETER_3']

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

MK_HOSTNAME = os.environ['NOTIFY_HOSTNAME']
MK_DESCRIPTION = os.environ['NOTIFY_SERVICEOUTPUT']
MK_PLUGIN_OUTPUT = os.environ['NOTIFY_SERVICEDESC']
MK_LAST_STATE_CHANGE = time.strftime("%Y-%m-%d %H:%M:%S")
MK_SERVICESTATE = os.environ['NOTIFY_SERVICESTATE']

MK_JSON_OUTPUT = json.dumps([{'mk_hostname': MK_HOSTNAME, 'mk_description': MK_DESCRIPTION, 'mk_plugin_output': MK_PLUGIN_OUTPUT, 'mk_last_state_chage': MK_LAST_STATE_CHANGE, 'mk_servicestate': MK_SERVICESTATE }])

post_data(customer_id, shared_key, MK_JSON_OUTPUT, log_type)