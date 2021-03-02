register_check_parameters(
    subgroup_networking,
    "fortigate_vdoms_ses",
    _("Fortigate VDOM Sessions"),
        Dictionary(
                help = _("This ruleset can be used to change the value of the fortigate VDOMs sessions"),
                elements = [
                        ("sessions",
                                Tuple (
                                        title = _("Session Numbers"),
                                        elements = [
                                                Integer(title=_("Warning at"), default_value = None),
                                                Integer(title=_("Critical at"), default_value = None),
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
