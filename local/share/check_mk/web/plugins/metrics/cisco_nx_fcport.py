metric_info["cisco_nx_fc_c_frames_in"] = {
    "title" : _("C Received Frames"),
    "unit"  : "count",
    "color" : "35/b",
}

metric_info["cisco_nx_fc_c_frames_out"] = {
    "title" : _("C Transmited Frames"),
    "unit"  : "count",
    "color" : "31/b",
}

metric_info["cisco_nx_fc_f_frames_in"] = {
    "title" : _("F Received Frames"),
    "unit"  : "count",
    "color" : "35/b",
}

metric_info["cisco_nx_fc_f_frames_out"] = {
    "title" : _("F Transmitted Frames"),
    "unit"  : "count",
    "color" : "31/b",
}

metric_info["cisco_nx_fc_link_fails"] = {
    "title" : _("Link failures"),
    "unit"  : "count",
    "color" : "11/a",
}

metric_info["cisco_nx_fc_sync_losses"] = {
    "title" : _("Sync losses"),
    "unit"  : "count",
    "color" : "12/a",
}

metric_info["cisco_nx_fc_link_resets_in"] = {
    "title" : _("Link resets in"),
    "unit"  : "1/s",
    "color" : "21/a",
}

metric_info["cisco_nx_fc_link_resets_out"] = {
    "title" : _("Link resets out"),
    "unit"  : "1/s",
    "color" : "22/a",
}

metric_info["cisco_nx_fc_crc_errors"] = {
    "title" : _("Receive CRC errors"),
    "unit"  : "count",
    "color" : "21/a",
}

metric_info["cisco_nx_fc_c3discards"] = {
    "title" : _("C3 discards"),
    "unit"  : "count",
    "color" : "13/a",
}

metric_info["cisco_nx_fc_txbcredits"] = {
    "title" : _("TX Buffer Credits"),
    "unit"  : "count",
    "color" : "13/a",
}
metric_info["cisco_nx_fc_rxbcredits"] = {
    "title" : _("RX Buffer Credits"),
    "unit"  : "count",
    "color" : "14/a",
}

metric_info["cisco_nx_fc_bbcredit_zero"] = {
    "title" : _("BB Credits from Zero"),
    "unit"  : "count",
    "color" : "14/a",
}

graph_info["cisco_nx_credits"] = {
    "title" : _("Received and Transmitted Credits"),
    "metrics" : [
        ("cisco_nx_fc_rxbcredits", "-area"),
        ("cisco_nx_fc_txbcredits", "area"),
    ],
}

graph_info["cisco_nx_errors"] = {
    "title" : _("Cisco NX Errors"),
    "metrics" : [
        ( "cisco_nx_fc_crc_errors",       "area" ),
        ( "cisco_nx_fc_c3discards",       "stack" ),
        ( "cisco_nx_fc_bbcredit_zero",    "stack" ),
        ( "cisco_nx_fc_link_fails",       "stack" ),
        ( "cisco_nx_fc_sync_losses",      "stack" ),
    ],
}

graph_info["cisco_nx_cframes"] = {
    "title" : _("C Frames"),
    "metrics" : [
        ("cisco_nx_fc_c_frames_in", "-area"),
        ("cisco_nx_fc_c_frames_out", "area"),
    ],
}

graph_info["cisco_nx_fframes"] = {
    "title" : _("F Frames"),
    "metrics" : [
        ("cisco_nx_fc_f_frames_in", "-area"),
        ("cisco_nx_fc_f_frames_out", "area"),
    ],
}

graph_info["cisco_nx_link_resets"] = {
    "title" : _("Link Resets (in/out)"),
    "metrics" : [
        ("cisco_nx_fc_link_resets_in", "-area"),
        ("cisco_nx_fc_link_resets_out", "area"),
    ],
}

check_metrics["check_mk-cisco_nx_fcport"] = {
    "in"             : { "name": "if_out_bps", },
    "out"            : { "name": "if_in_bps", },
    "InvalidCRCs"    : { "name": "cisco_nx_fc_crc_errors" },
    "LinkFailures"   : { "name": "cisco_nx_fc_link_fails" },
    "SyncLosses"     : { "name": "cisco_nx_fc_sync_losses" },
    "LinkResetIns"   : { "name": "cisco_nx_fc_link_resets_in" },
    "LinkResetOuts"  : { "name": "cisco_nx_fc_link_resets_out" },
    "TXBBFromZero"   : { "name": "cisco_nx_fc_bbcredit_zero" },
    "CFramesIn"      : { "name": "cisco_nx_fc_c_frames_in" },
    "CFramesOut"     : { "name": "cisco_nx_fc_c_frames_out" },
    "C3Discards"     : { "name": "cisco_nx_fc_c3discards" },
    "FramesIn"       : { "name": "cisco_nx_fc_f_frames_in" },
    "FramesOut"      : { "name": "cisco_nx_fc_f_frames_out" },
    "RXBCredits"     : { "name": "cisco_nx_fc_rxbcredits" },
    "TXBCredits"     : { "name": "cisco_nx_fc_txbcredits" },
}

