metric_info["a10virtSrv_bytesin"] = {
    "title" : _("Bytes In"),
    "unit"  : "bytes",
    "color" : "36/a",
}

metric_info["a10virtSrv_bytesout"] = {
    "title" : _("Bytes Out"),
    "unit"  : "bytes",
    "color" : "31/a",
}

metric_info["a10virtSrv_packetsin"] = {
    "title" : _("Packets in"),
    "unit"  : "count",
    "color" : "13/a",
}

metric_info["a10virtSrv_packetsout"] = {
    "title" : _("Packets in"),
    "unit"  : "count",
    "color" : "11/a",
}

metric_info["a10virtSrv_persistantcons"] = {
    "title" : _("Persistant Connections"),
    "unit"  : "count",
    "color" : "12/a",
}

metric_info["a10virtSrv_totalcons"] = {
    "title" : _("Total Connections"),
    "unit"  : "count",
    "color" : "13/a",
}

metric_info["a10virtSrv_peakcons"] = {
    "title" : _("Peak Connections"),
    "unit"  : "count",
    "color" : "11/a",
}

metric_info["a10virtSrv_currentcons"] = {
    "title" : _("Current Connections"),
    "unit"  : "count",
    "color" : "31/a",
}

metric_info["a10virtSrv_totall7reqs"] = {
    "title" : _("Total L7 Requests"),
    "unit"  : "count",
    "color" : "36/a",
}

graph_info["a10virtSrv_bytes"] = {
    "title" : _("Bytes in and Bytes out"),
    "metrics" : [
        ("a10virtSrv_bytesin", "area"),
		("a10virtSrv_bytesout", "-area"),
    ],
}

graph_info["a10virtSrv_packets"] = {
    "title" : _("Packets in and Packets out"),
    "metrics" : [
        ("a10virtSrv_packetsin", "area"),
		("a10virtSrv_packetsout", "-area"),
    ],
}

graph_info["a10virtSrv_connections"] = {
    "title" : _("Connections"),
    "metrics" : [
        ("a10virtSrv_persistantcons", "area"),
		("a10virtSrv_totalcons", "stack"),
		("a10virtSrv_peakcons", "stack"),
		("a10virtSrv_currentcons", "line"),
    ],
}

graph_info["a10NatPools_totall7reqs"] = {
    "title" : _("Total L7 Requests"),
    "metrics" : [
        ("a10virtSrv_totall7reqs", "area"),
    ],
}

check_metrics["check_mk-a10virtSrv"] = {
    "packetsin"			: { "name": "a10virtSrv_packetsin", },
	"packetsout"     	: { "name": "a10virtSrv_packetsout", },
	"bytesin"     		: { "name": "a10virtSrv_bytesin", },
	"bytesout"          : { "name": "a10virtSrv_bytesout", },
	"persistantcons"    : { "name": "a10virtSrv_persistantcons", },
	"totalcons"         : { "name": "a10virtSrv_totalcons", },
	"peakcons"          : { "name": "a10virtSrv_peakcons", },
	"currentcons"       : { "name": "a10virtSrv_currentcons", },
	"totall7reqs"       : { "name": "a10virtSrv_totall7reqs", },
}
