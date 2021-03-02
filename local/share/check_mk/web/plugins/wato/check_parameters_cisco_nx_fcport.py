register_check_parameters(
    subgroup_storage,
    "cisco_nx_fcport",
    _("Cisco NX FibreChannel ports"),
        Dictionary(
                help = _("This ruleset can be used to change Cisco NX FibreChannel values for some of the collected data and configure your own warn and crit thresholds"),
                elements = [
                        ("fcIfLinkFailures",
                                Tuple (
                                        title = _("Link Failures"),
                                        elements = [
                                                Integer(title=_("Warning at"), default_value = 0),
                                                Integer(title=_("Critical at"), default_value = 1),
                                        ]
                           )
                        ),
                        ("fcIfSyncLosses",
                                Tuple (
                                        title = _("Sync Losses"),
                                        elements = [
                                                Integer(title=_("Warning at"), default_value = 0),
                                                Integer(title=_("Critical at"), default_value = 1),
                                        ]
                                )
                        ),
                        ("fcIfLinkResetIns",
                                Tuple (
                                        title = _("Link Reset Ins"),
                                        elements = [
                                                Integer(title=_("Warning at"), default_value = 0),
                                                Integer(title=_("Critical at"), default_value = 1),
                                        ]
                                )
                        ),
                        ("fcIfLinkResetOuts",
                                Tuple (
                                        title = _("Link Reset Outs"),
                                        elements = [
                                                Integer(title=_("Warning at"), default_value = 0),
                                                Integer(title=_("Critical at"), default_value = 1),
                                        ]
                                )
                        )
                ]
        ),
        TextAscii(
                title = _("port name"),
                help = _("The name of the switch port (not the alias - so use fc1/1, fc1/2, and so on.)"),
        ),
        match_type = "dict",
)
