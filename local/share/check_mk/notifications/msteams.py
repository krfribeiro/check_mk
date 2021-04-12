#!/usr/bin/env python
# MS-Teams
# Author : ricardoftribeiro@gmail.com @krfribeiro

import os, sys
import requests
import json
import re

context = dict([ (var[7:], value.decode("utf-8"))
                  for (var, value) in os.environ.items()
                  if var.startswith("NOTIFY_")])

if 'PARAMETER_WEBHOOK' in context:
    msteams_path = context["PARAMETER_WEBHOOK"]
else:
    sys.stderr.write("Webhook URL not set\n")
    return 2

if 'URL_PREFIX' in context:
    baseURL=re.sub('/$','',context['PARAMETER_URL'])
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
    elif context['SERVICESTATE'] ==  'CRITICAL':
      	icon = "critical.png"
      	colour = "a30200"
      	message += " is " + context['SERVICESTATE']
    elif context['SERVICESTATE'] ==  'WARNING':
      	icon = "warning.png"
      	colour = "daa038"
      	message += " is " + context['SERVICESTATE']
    elif context['SERVICESTATE'] ==  'UNKNOWN':
      	icon = "unknown.png"
      	colour = "cccccc"
      	message += " is " + context['SERVICESTATE']
    elif context['SERVICESTATE'] ==  'OK':
        icon = "ok.png"
        colour = "2eb886"
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
    elif context['HOSTSTATE'] ==  'DOWN':
      	icon = "critical.png"
      	colour = "a30200"
    elif context['HOSTSTATE'] ==  'WARNING':
      	icon = "warning.png"
      	colour = "daa038"
    elif context['HOSTSTATE'] ==  'UNKNOWN':
      	icon = "unknown.png"
      	colour = "cccccc"
    elif context['HOSTSTATE'] ==  'UP':
      	icon = "ok.png"
      	colour = "2eb886"
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
    "summary": "Summary",
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
  return 0
else:
  sys.stderr.write(conn.text)
  return 2