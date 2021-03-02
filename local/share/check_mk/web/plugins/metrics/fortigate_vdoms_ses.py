metric_info["fortigate_vdoms_ses_count"] = {
    "title" : _("Active sessions"),
    "unit"  : "count",
    "color" : "11/a",
}

graph_info["fortigate_vdoms_ses_sessions"] = {
    "title" : _("VDOM Sessions"),
    "metrics" : [
        ("fortigate_vdom_ses_count", "area"),
    ],
}

check_metrics["check_mk-fortigate_vdoms_ses"] = {
    "SESUsage" : { "name": "fortigate_vdoms_ses_count", },
}
