#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = 'datasource_programs'

register_rule(group,
    "special_agents:graphite",
    Transform(
        Dictionary(
            elements = [
                ("user", TextAscii(title = _("Username"),
                    allow_empty = True,
                )),
                ("password", Password(title = _("Password"),
                    allow_empty = True,
                )),
                ("values", ListOfStrings(
                    title = _("Values/metrics to fetch"),
                    orientation = "horizontal",
                    help = _("You need to specify any value - this is mandatory. You can give regex patterns for the metrics you need to retrieve."),
                    allow_empty = False,
                )),
            ],
            optional_keys = [ "user", "password" ],
        ),
    ),
    title = _("Agent Graphite Configuration"),
    match = 'first',
             )