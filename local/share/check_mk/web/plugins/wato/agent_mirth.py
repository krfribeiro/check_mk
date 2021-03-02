#!/usr/bin/env python
# Mirth Datasource Program (Special Agent) for Check_MK
# Tested on Check_MK CEE 1.5 and 1.6
# Author : ricardo.ribeiro@axians.com
# -*- coding: utf-8 -*-

group = 'datasource_programs'

register_rule(group,
    "special_agents:mirth",
    Transform(
        Dictionary(
            elements = [
                ("user", TextAscii(title = _("Username"),
                    allow_empty = False,
                )),
                ("secret", Password(title = _("Secret"),
                    allow_empty = False,
                )),
				("port", TextAscii(title = _("Port"),
                    allow_empty = False,
                )),
            ],
        ),
    ),
    title = _("Agent Mirth Configuration"),
    match = 'first',
)
