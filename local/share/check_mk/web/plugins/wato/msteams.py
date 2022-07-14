#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# Author : ricardoftribeiro@gmail.com @krfribeiro
# Change: 2022-07-13 doc@snowheaven.de Christian Wirtz - migration to Checkmk v2.1 (THX to Joerg Hebel)

from cmk.gui.plugins.wato import HTTPProxyReference
from cmk.utils.site import omd_site

register_notification_parameters("msteams", Dictionary(
    elements = [
        ("url_prefix",
                 TextAscii(
                     title=_("URL prefix for links to Check_MK"),
                     help=_("Your Check_MK servers address with this format : http/https://server/sitename/"),
                     allow_empty=False,
                     regex="^(http|https)://.*/.*/$",
                     regex_error=_("The URL must begin with <tt>http</tt> or <tt>https</tt> and end with <tt>/</tt>."),
                     size=64,
                     default_value="http or https://" + socket.gethostname() + "/" + omd_site() + "/",
        )),
        ("webhook", TextAscii(
            title = _("Webhook URL"),
            help = _("MS-Teams Channel webhook URL"),
            allow_empty = False,
        )),
        ("proxy_url", Transform(
            HTTPProxyReference(),
            forth=lambda v: ("url", v) if isinstance(v, str) else v,
        )),
    ]
))

