# Mirth Datasource Program (Special Agent) for Check_MK
# Tested on Check_MK CEE 1.5 and 1.6
# Author : ricardoftribeiro@gmail.com @krfribeiro

register_check_parameters(
    subgroup_applications,
    "mirth_stats",
    _("Parameters for Mirth Statistics"),
    Dictionary(
        elements = [
            ('error', Tuple(
                title = _('Levels for error messages'),
                help = _("Number of error messages for warning or critical state"),
                elements = [
                    Integer(title = _("Warning at"), default_value = 2),
                    Integer(title = _("Critical at"), default_value = 4),
                ])),
            ('queued', Tuple(
                title = _('Levels for queued messages'),
                help = _("Number of queued messages for warning or critical state"),
                elements = [
                    Integer(title = _("Warning at"), default_value = 2),
                    Integer(title = _("Critical at"), default_value = 4),
                ])),
        ],
    ),
    TextAscii(
        title = _("Channel"),
        allow_empty = False,
    ),
    'dict',
)

