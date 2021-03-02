register_check_parameters(
    subgroup_applications,
    "mirth_stats",
    "Parameters for Mirth Statistics",
    Dictionary(
        elements = [
            ('mirth_error', Tuple(
                title = 'Levels for error messages',
                help = "Number of error messages for warning or critical state",
                elements = [
                    Integer(title = "Warning at", default_value = 2),
                    Integer(title = "Critical at", default_value = 4),
                ])),
            ('mirth_queued', Tuple(
                title = 'Levels for queued messages',
                help = "Number of queued messages for warning or critical state",
                elements = [
                    Integer(title = "Warning at", default_value = 20),
                    Integer(title = "Critical at", default_value = 40),
                ])),
        ],
    ),
    TextAscii(
        title = "Channel",
        allow_empty = False,
    ),
    'dict',
)
