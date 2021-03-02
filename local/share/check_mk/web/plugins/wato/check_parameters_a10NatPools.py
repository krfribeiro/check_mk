register_check_parameters(
    subgroup_networking,
    "a10NatPools",
    _("A10 NAT Pools total misses"),
        Dictionary(
                help = _("This ruleset can be used to change the value of the NAT Pools misses"),
                elements = [
                        ("poolmisses",
                                Tuple (
                                        title = _("NAT misses"),
                                        elements = [
                                                Integer(title=_("Warning at"), default_value = None),
                                                Integer(title=_("Critical at"), default_value = None),
                                        ]
                           )
                        )
                ]
        ),
        TextAscii(
                title = _("NAT Pool"),
                help = _("The name of the NAT Pool"),
        ),
        match_type = "dict",
)
