#!/usr/bin/env python3
# License: GNU General Public License v2

from collections.abc import Iterator, Mapping

from cmk.server_side_calls.v1 import (
    HostConfig,
    SpecialAgentCommand,
    SpecialAgentConfig,
    noop_parser,
)


def _address(params: Mapping[str, object], host_config: HostConfig) -> str:
    if address := params.get("address"):
        return str(address)
    try:
        if host_config.primary_ip_config.address:
            return host_config.primary_ip_config.address
    except ValueError:
        pass
    return host_config.name


def commands_cisco_xr_ospf(
    params: Mapping[str, object], host_config: HostConfig
) -> Iterator[SpecialAgentCommand]:
    args: list = [
        "--host", _address(params, host_config),
        "--user", str(params["username"]),
        "--port", str(params.get("port", 22)),
        "--timeout", str(params.get("timeout", 30)),
    ]
    if (password := params.get("password")) is not None:
        # passed as "<id>:<password store file>", never as plain text
        args += ["--password-ref", password]
    if ssh_options := params.get("ssh_options"):
        args += ["--ssh-options", str(ssh_options)]
    if params.get("ospfv2", True):
        args.append("--ospfv2")
    if params.get("ospfv3", False):
        args.append("--ospfv3")
    yield SpecialAgentCommand(command_arguments=args)


special_agent_cisco_xr_ospf = SpecialAgentConfig(
    name="cisco_xr_ospf",
    parameter_parser=noop_parser,
    commands_function=commands_cisco_xr_ospf,
)
