#!/usr/bin/env python3
# MS-Teams
# Author : ricardoftribeiro@gmail.com @krfribeiro

import os, sys
import requests
import json
import re

context = dict([ (var[7:], value)
                  for (var, value) in list(os.environ.items())
                  if var.startswith("NOTIFY_")])

map_states = {
        "OK":           ("ok.png","2eb886" ),
        "WARNING":      ("warning.png","daa038" ),
        "CRITICAL":     ("critical.png","a30200" ),
        "UNKNOWN":      ("unknown.png","cccccc" ),
        "DOWN":         ("critical.png","a30200" ),
        "UP":           ("ok.png","2eb886" ),
}

regexp = re.compile(r'CRITICAL|WARNING|UNKNOWN|OK|DOWN|UP')

if 'PARAMETER_WEBHOOK' in context:
    msteams_path = context["PARAMETER_WEBHOOK"]
else:
    sys.stderr.write("Webhook URL not set\n")
    sys.exit(2)

if 'PARAMETER_URL_PREFIX' in context:
    baseURL=re.sub('/$','',context['PARAMETER_URL_PREFIX'])
else:
    baseURL="https://" + context['MONITORING_HOST'] + "/" + context['OMD_SITE']

icons_path = "https://github.com/krfribeiro/check_mk/raw/master/local/share/check_mk/web/images/"

headers = {"Content-type": "application/json", "Accept": "text/plain"}
message = context['NOTIFICATIONTYPE']  + ' | Hostname : ' + context['HOSTNAME'] + " "
authorText = ""

if context['WHAT'] == 'SERVICE':
    message += "| Service: " + context['SERVICEDESC']
    context['DETAILS_OUTPUT'] = context['SERVICEOUTPUT']
    infoURL = baseURL + context['SERVICEURL']
    if context['NOTIFICATIONAUTHOR'] != '':
        authorText += "Triggered by **" + context['NOTIFICATIONAUTHOR'] + "** - *" + context['NOTIFICATIONCOMMENT']  + "*"
    if context['NOTIFICATIONTYPE'] == 'DOWNTIMESTART':
        icon = "downtime.png"
        colour = "439FE0"
        message += " - Downtime started"
    elif context['NOTIFICATIONTYPE'] == 'DOWNTIMEEND':
        icon = "downtime.png"
        colour = "33cccc"
        message += " - Downtime ended"
    elif context['NOTIFICATIONTYPE'] == 'ACKNOWLEDGEMENT':
        icon = "acknowledge.png"
        colour = "8f006b"
        message += " | " + context['SERVICEACKCOMMENT']
    elif regexp.search(context['SERVICESTATE']):
        icon, colour = map_states.get(context['SERVICESTATE'])
        message += " is " + context['SERVICESTATE']
    else:
        icon = "cmk.png"
else:
    message += "is " + context['HOSTSTATE']
    context['DETAILS_OUTPUT'] = context['HOSTOUTPUT']
    infoURL = baseURL + context['HOSTURL']
    if context['NOTIFICATIONAUTHOR'] != '':
        authorText += "Triggered by **" + context['NOTIFICATIONAUTHOR'] + "** - *" + context['NOTIFICATIONCOMMENT']  + "*"
    if context['NOTIFICATIONTYPE'] == 'DOWNTIMESTART':
        icon = "downtime.png"
        colour = "439FE0"
        message += " - Downtime started"
    elif context['NOTIFICATIONTYPE'] == 'DOWNTIMEEND':
        icon = "downtime.png"
        colour = "33cccc"
        message += " - Downtime ended"
    elif context['NOTIFICATIONTYPE'] == 'ACKNOWLEDGEMENT':
        icon = "acknowledge.png"
        colour = "8f006b"
        message += " | " + context['HOSTACKCOMMENT']
    elif regexp.search(context['HOSTSTATE']):
        icon, colour = map_states.get(context['HOSTSTATE'])
    else:
        icon = "cmk.png"

sections = {
        "activitySubtitle": authorText,
        "activityImage": icons_path + icon,
        "facts": [{
            "name": "Detail",
            "value": context['DETAILS_OUTPUT']
        }, {
            "name": "Affected groups",
            "value": context['HOSTGROUPNAMES']
        }],
        "markdown": "True"
    }

data = {
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
        "title": message,
    "themeColor": colour,
    "summary": message,
    "sections": [sections],
    "potentialAction": [{
        "@type": "OpenUri",
        "name": "Alarm Details",
        "targets": [{
            "os": "default",
            "uri": infoURL
        }]
    }]
}

conn = requests.post(msteams_path, data = json.dumps(data))

if conn.status_code == 200:
  sys.exit(0)
else:
  sys.stderr.write(conn.text)
  sys.exit(2)
