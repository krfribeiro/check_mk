#!/usr/bin/env python3
# License: GNU General Public License v2

from cmk.rulesets.v1 import Help, Label, Title
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    InputHint,
    Integer,
    LevelDirection,
    Password,
    ServiceState,
    SimpleLevels,
    String,
    TimeMagnitude,
    TimeSpan,
    migrate_to_password,
    validators,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, SpecialAgent, Topic


def _agent_form() -> Dictionary:
    return Dictionary(
        title=Title("Cisco IOS-XR OSPF neighbors via SSH"),
        help_text=Help(
            "Connects to the router via SSH and runs 'show ospf vrf all neighbor' "
            "(and optionally 'show ospfv3 vrf all neighbor'). Authenticate either with "
            "an SSH private key file or with a password (needs 'sshpass' on the Checkmk "
            "server). If a key file is set, it is used and the password is ignored. "
            "With neither, the default keys of the site user (~/.ssh) are tried."
        ),
        elements={
            "username": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("Username"),
                    custom_validate=(validators.LengthInRange(min_value=1),),
                ),
            ),
            "password": DictElement(
                required=False,
                parameter_form=Password(title=Title("Password"), migrate=migrate_to_password),
            ),
            "identity_file": DictElement(
                required=False,
                parameter_form=String(
                    title=Title("SSH private key file"),
                    help_text=Help(
                        "Path to the private key on the Checkmk server, readable by the site "
                        "user, e.g. $OMD_ROOT/.ssh/ospf_router. $OMD_ROOT, other environment "
                        "variables and ~ are expanded. The key must not have a passphrase. "
                        "Takes precedence over the password."
                    ),
                    prefill=InputHint("$OMD_ROOT/.ssh/id_ed25519"),
                    custom_validate=(validators.LengthInRange(min_value=1),),
                ),
            ),
            "address": DictElement(
                required=False,
                parameter_form=String(
                    title=Title("Connect to this address instead of the host address"),
                ),
            ),
            "port": DictElement(
                required=False,
                parameter_form=Integer(
                    title=Title("SSH port"),
                    prefill=DefaultValue(22),
                    custom_validate=(validators.NetworkPort(),),
                ),
            ),
            "timeout": DictElement(
                required=False,
                parameter_form=Integer(
                    title=Title("Timeout per command"),
                    unit_symbol="s",
                    prefill=DefaultValue(30),
                    custom_validate=(validators.NumberInRange(min_value=5, max_value=300),),
                ),
            ),
            "ospfv2": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    title=Title("OSPFv2"),
                    label=Label("Collect 'show ospf vrf all neighbor'"),
                    prefill=DefaultValue(True),
                ),
            ),
            "ospfv3": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    title=Title("OSPFv3"),
                    label=Label("Collect 'show ospfv3 vrf all neighbor'"),
                    prefill=DefaultValue(False),
                ),
            ),
            "ssh_options": DictElement(
                required=False,
                parameter_form=String(
                    title=Title("Additional SSH options"),
                    help_text=Help(
                        "Replaces the default options "
                        "'-o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 -o LogLevel=ERROR'."
                    ),
                ),
            ),
        },
    )


rule_spec_special_agent_cisco_xr_ospf = SpecialAgent(
    name="cisco_xr_ospf",
    title=Title("Cisco IOS-XR OSPF neighbors (SSH, all VRFs)"),
    topic=Topic.NETWORKING,
    parameter_form=_agent_form,
)


_STATES = [
    ("full", Title("FULL"), 0),
    ("two_way", Title("2WAY"), 0),
    ("down", Title("DOWN"), 2),
    ("attempt", Title("ATTEMPT"), 1),
    ("init", Title("INIT"), 1),
    ("exstart", Title("EXSTART"), 1),
    ("exchange", Title("EXCHANGE"), 1),
    ("loading", Title("LOADING"), 1),
]


def _check_form() -> Dictionary:
    return Dictionary(
        elements={
            "states": DictElement(
                required=False,
                parameter_form=Dictionary(
                    title=Title("Monitoring state per OSPF neighbor state"),
                    elements={
                        key: DictElement(
                            required=False,
                            parameter_form=ServiceState(title=title, prefill=DefaultValue(default)),
                        )
                        for key, title, default in _STATES
                    },
                ),
            ),
            "state_not_found": DictElement(
                required=False,
                parameter_form=ServiceState(
                    title=Title("State if the neighbor is missing from the output"),
                    prefill=DefaultValue(2),
                ),
            ),
            "uptime_lower": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("Lower levels for the neighbor uptime"),
                    help_text=Help("Alerts when the adjacency was (re)established recently, e.g. after a flap."),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[
                            TimeMagnitude.DAY,
                            TimeMagnitude.HOUR,
                            TimeMagnitude.MINUTE,
                            TimeMagnitude.SECOND,
                        ]
                    ),
                    prefill_fixed_levels=DefaultValue((600.0, 120.0)),
                ),
            ),
        },
    )


rule_spec_cisco_xr_ospf_neighbor = CheckParameters(
    name="cisco_xr_ospf_neighbor",
    title=Title("Cisco IOS-XR OSPF neighbors (per VRF)"),
    topic=Topic.NETWORKING,
    parameter_form=_check_form,
    condition=HostAndItemCondition(item_title=Title("VRF, neighbor ID and interface")),
)
