register_check_parameters(
    subgroup_networking,
    "fortigate_vdoms_mem",
    _("Fortigate VDOM Memory Usage"),
        Dictionary(
                help = _("This ruleset can be used to change the value of the VDOM Memory usage"),
                elements = [
                        ("memlevels",
                                Tuple (
                                        title = _("Memory Utilization (in percentage)"),
                                        elements = [
                                                Integer(title=_("Warning at"), default_value = "90"),
                                                Integer(title=_("Critical at"), default_value = "95"),
                                        ]
                           )
                        )
                ]
        ),
        TextAscii(
                title = _("VDOM Name"),
                help = _("The name of the VDOM"),
        ),
        match_type = "dict",
)
