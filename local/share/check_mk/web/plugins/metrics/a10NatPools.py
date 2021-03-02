metric_info["a10NatPools_NATtotalportsused"] = {
    "title" : _("Total NAT Ports Used"),
    "unit"  : "count",
    "color" : "13/a",
}

metric_info["a10NatPools_NATtotalusedaddresses"] = {
    "title" : _("Total NAT Used Addresses"),
    "unit"  : "count",
    "color" : "12/a",
}

metric_info["a10NatPools_NATtotalfreeaddresses"] = {
    "title" : _("Total NAT Free Addresses"),
    "unit"  : "count",
    "color" : "11/a",
}

metric_info["a10NatPools_NATtotalmisses"] = {
    "title" : _("Total NAT Total Misses"),
    "unit"  : "count",
    "color" : "11/a",
}

graph_info["a10NatPools_NATtotalportsused"] = {
    "title" : _("Total NAT Ports Used"),
    "metrics" : [
        ("a10NatPools_NATtotalportsused", "area"),
    ],
}

graph_info["a10NatPools_Addresses"] = {
    "title" : _("Total and Free NAT Addresses"),
    "metrics" : [
        ("a10NatPools_NATtotalusedaddresses", "area"),
        ("a10NatPools_NATtotalfreeaddresses", "-area"),
    ],
}

graph_info["a10NatPools_NATtotalmisses"] = {
    "title" : _("Total NAT Misses"),
    "metrics" : [
        ("a10NatPools_NATtotalmisses", "area"),
    ],
}

check_metrics["check_mk-a10NatPools"] = {
    "NATtotalportsused"         : { "name": "a10NatPools_NATtotalportsused", },
    "NATtotalusedaddresses"     : { "name": "a10NatPools_NATtotalusedaddresses", },
    "NATtotalfreeaddresses"     : { "name": "a10NatPools_NATtotalfreeaddresses", },
    "NATtotalmisses"            : { "name": "a10NatPools_NATtotalmisses", },
}
