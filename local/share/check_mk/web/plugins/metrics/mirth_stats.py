#!/usr/bin/env python
# Mirth Datasource Program (Special Agent) for Check_MK
# Tested on Check_MK CEE 1.5 and 1.6
# Author : ricardo.ribeiro@axians.com
# -*- coding: utf-8 -*-

# finalDict[channel['channelId']], channel['received'], channel['error'], channel['filtered'], channel['queued'], channel['sent']

metric_info["mirth_received"] = {
        "title" : _("Received"),
        "unit"  : "count",
        "color" : "34/a",
        }

metric_info["mirth_error"] = {
        "title" : _("Errors"),
        "unit"  : "count",
        "color" : "46/a",
        }

metric_info["mirth_filtered"] = {
        "title" : _("Filtered"),
        "unit"  : "count",
        "color" : "44/a",
        }

metric_info["mirth_queued"] = {
        "title" : _("Queued"),
        "unit"  : "count",
        "color" : "16/a",
        }

metric_info["mirth_sent"] = {
        "title" : _("Sent"),
        "unit"  : "count",
        "color" : "13/a",
        }

###########################################################################

graph_info.append({
    "title"    : _("Mirth Received"),
    "metrics"  : [
        ( "mirth_received", "line" ),
        ],
    "scalars"  : [
        "mirth_received:warn",
        "mirth_received:crit",
        ],
    })

graph_info.append({
    "title"    : _("Mirth Errors"),
    "metrics"  : [
        ( "mirth_error", "line" ),
        ],
    "scalars"  : [
        "mirth_error:warn",
        "mirth_error:crit",
        ],
    })
	
graph_info.append({
    "title"    : _("Mirth Filtered"),
    "metrics"  : [
        ( "mirth_filtered", "line" ),
        ],
    "scalars"  : [
        "mirth_filtered:warn",
        "mirth_filtered:crit",
        ],
    })

graph_info.append({
    "title"    : _("Mirth Queued"),
    "metrics"  : [
        ( "mirth_queued", "line" ),
        ],
    "scalars"  : [
        "mirth_queued:warn",
        "mirth_queued:crit",
        ],
    })

graph_info.append({
    "title"    : _("Mirth Sent"),
    "metrics"  : [
        ( "mirth_sent", "line" ),
        ],
    "scalars"  : [
        "mirth_sent:warn",
        "mirth_sent:crit",
        ],
    })
