#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_notification_parameters("telegram", Dictionary(
    elements = [
        ("token",
                 TextAscii(
                     title=_("Token"),
                     help=_("The token for your telegram token"),
                     allow_empty=False,
        )),
        ("chat_id", TextAscii(
            title = _("Chat-ID"),
            help = _("ChatID where you will receive messages into"),
            allow_empty = False,
        )),
        ("common_body",
             TextAreaUnicode(
                 title=_("Body head for both host and service notifications"),
                 rows=7,
                 cols=58,
                 monospaced=True,
                 default_value="""Host:     $HOSTNAME$
Alias:    $HOSTALIAS$
Address:  $HOSTADDRESS$
""",
             )),
        ("host_body",
             TextAreaUnicode(
                 title=_("Body tail for host notifications"),
                 rows=9,
                 cols=58,
                 monospaced=True,
                 default_value="""Event:    $EVENT_TXT$
Output:   $HOSTOUTPUT$
Perfdata: $HOSTPERFDATA$
$LONGHOSTOUTPUT$
""",
             )),
        ("service_body",
             TextAreaUnicode(
                 title=_("Body tail for service notifications"),
                 rows=11,
                 cols=58,
                 monospaced=True,
                 default_value="""Service:  $SERVICEDESC$
Event:    $EVENT_TXT$
Output:   $SERVICEOUTPUT$
Perfdata: $SERVICEPERFDATA$
$LONGSERVICEOUTPUT$
""",
             )),
    ]
))

