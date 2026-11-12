#!/usr/bin/env python3
# License: GNU General Public License v2
"""Cisco IOS-XR OSPF/OSPFv3 neighbors of all VRFs (special agent cisco_xr_ospf)

Example agent output (raw CLI output, one block per protocol):

<<<cisco_xr_ospf_neighbors:sep(0)>>>
[[[ospfv2]]]
Neighbors for OSPF 1, VRF CUST-A

Neighbor ID     Pri   State           Dead Time   Address         Interface
10.255.0.2      1     FULL/  -        00:00:35    10.0.0.2        GigabitEthernet0/0/0/0
    Neighbor is up for 2d03h
[[[ospfv3:error]]]
ssh rc=255: Connection timed out
"""

import re
from collections.abc import Mapping, MutableMapping, Sequence
from dataclasses import dataclass, field

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    StringTable,
    check_levels,
    render,
)

DEFAULT_STATES = {
    "full": 0,
    "two_way": 0,
    "down": 2,
    "attempt": 1,
    "init": 1,
    "exstart": 1,
    "exchange": 1,
    "loading": 1,
}


@dataclass(frozen=True)
class Neighbor:
    protocol: str
    process: str
    vrf: str
    neighbor_id: str
    priority: str
    state: str  # e.g. FULL
    role: str  # e.g. DR, BDR, DROTHER, -
    dead_time: str
    address: str
    interface_id: str
    interface: str
    uptime_text: str | None = None
    uptime: int | None = None


@dataclass
class Section:
    neighbors: MutableMapping[str, MutableMapping[str, Neighbor]] = field(
        default_factory=lambda: {"ospfv2": {}, "ospfv3": {}}
    )
    errors: MutableMapping[str, str] = field(default_factory=dict)
    collected: set[str] = field(default_factory=set)


_RE_BLOCK = re.compile(r"^\[\[\[(ospfv[23])(:error)?\]\]\]$")
_RE_HEADER = re.compile(r"^Neighbors for OSPF(?:v3)?\s+(\S+?)(?:,\s+VRF\s+(.+?))?\s*$")
_RE_UP = re.compile(r"^\s*Neighbor is up for\s+(.+?)\s*$")
_RE_COLUMNS = re.compile(r"Neighbor ID|Dead Time|Interface ID|Up Time|\S+")
_RE_STATE_SPACES = re.compile(r"(\b[A-Za-z0-9]+/)\s+(-)")
_RE_UNITS = re.compile(r"(\d+)([ywdhms])")
_UNIT_SECONDS = {"y": 31536000, "w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}

_DEFAULT_COLUMNS = {
    "ospfv2": ["Neighbor ID", "Pri", "State", "Dead Time", "Address", "Interface"],
    "ospfv3": ["Neighbor ID", "Pri", "State", "Dead Time", "Interface ID", "Interface"],
}


def parse_uptime(text: str) -> int | None:
    """
    >>> parse_uptime("00:42:10"), parse_uptime("2d03h"), parse_uptime("1w2d"), parse_uptime("never")
    (2530, 183600, 777600, None)
    """
    text = text.strip()
    if re.fullmatch(r"\d+:\d{2}:\d{2}", text):
        h, m, s = (int(x) for x in text.split(":"))
        return h * 3600 + m * 60 + s
    units = _RE_UNITS.findall(text)
    if units and "".join(n + u for n, u in units) == text.replace(" ", ""):
        return sum(int(n) * _UNIT_SECONDS[u] for n, u in units)
    return None


def _neighbor_from_row(
    protocol: str, process: str, vrf: str, columns: Sequence[str], line: str
) -> Neighbor | None:
    tokens = _RE_STATE_SPACES.sub(r"\1\2", line.strip()).split()
    if len(tokens) != len(columns):
        return None
    row = dict(zip(columns, tokens))
    if not row.get("Pri", "").isdigit() or "Neighbor ID" not in row:
        return None
    state, _, role = row.get("State", "").partition("/")
    uptime_text = row.get("Up Time")
    return Neighbor(
        protocol=protocol,
        process=process,
        vrf=vrf,
        neighbor_id=row["Neighbor ID"].strip("*#"),
        priority=row["Pri"],
        state=state.upper(),
        role=role or "-",
        dead_time=row.get("Dead Time", ""),
        address=row.get("Address", ""),
        interface_id=row.get("Interface ID", ""),
        interface=row.get("Interface", ""),
        uptime_text=uptime_text,
        uptime=parse_uptime(uptime_text) if uptime_text else None,
    )


def neighbor_item(neighbor: Neighbor) -> str:
    return f"{neighbor.vrf} {neighbor.neighbor_id} on {neighbor.interface}"


def parse_cisco_xr_ospf_neighbors(string_table: StringTable) -> Section:
    section = Section()
    protocol: str | None = None
    is_error = False
    process = vrf = ""
    columns: list[str] = []
    last: Neighbor | None = None

    for (line,) in (row if row else [""] for row in string_table):
        if match := _RE_BLOCK.match(line.strip()):
            protocol, is_error = match.group(1), bool(match.group(2))
            section.collected.add(protocol)
            process = vrf = ""
            last = None
            continue
        if protocol is None:
            continue
        if is_error:
            if line.strip():
                section.errors[protocol] = " ".join(
                    filter(None, [section.errors.get(protocol), line.strip()])
                )
            continue

        if match := _RE_HEADER.match(line.strip()):
            process = match.group(1)
            vrf = (match.group(2) or "default").strip()
            columns = list(_DEFAULT_COLUMNS[protocol])
            last = None
            continue
        if not process:
            continue
        if line.strip().startswith("Neighbor ID"):
            columns = _RE_COLUMNS.findall(line.strip())
            continue
        if match := _RE_UP.match(line):
            if last is not None:
                text = match.group(1)
                last = Neighbor(**{**last.__dict__, "uptime_text": text, "uptime": parse_uptime(text)})
                section.neighbors[protocol][neighbor_item(last)] = last
            continue
        if neighbor := _neighbor_from_row(protocol, process, vrf, columns, line):
            section.neighbors[protocol][neighbor_item(neighbor)] = neighbor
            last = neighbor
            continue
        if line.strip():
            last = None

    return section


agent_section_cisco_xr_ospf_neighbors = AgentSection(
    name="cisco_xr_ospf_neighbors",
    parse_function=parse_cisco_xr_ospf_neighbors,
)


def _discover(protocol: str, section: Section) -> DiscoveryResult:
    for item in section.neighbors[protocol]:
        yield Service(item=item)


def _check(protocol: str, item: str, params: Mapping, section: Section) -> CheckResult:
    neighbor = section.neighbors[protocol].get(item)
    if neighbor is None:
        if protocol in section.errors:
            yield Result(
                state=State.UNKNOWN,
                summary=f"Data collection failed: {section.errors[protocol]}",
            )
            return
        if protocol not in section.collected:
            yield Result(
                state=State.UNKNOWN,
                summary=f"{protocol.upper()} is not collected (check the special agent rule)",
            )
            return
        yield Result(
            state=State(params.get("state_not_found", 2)),
            summary="Neighbor not found in 'show ospf' output",
        )
        return

    states = {**DEFAULT_STATES, **params.get("states", {})}
    state_key = {"2WAY": "two_way"}.get(neighbor.state, neighbor.state.lower())
    role = f"/{neighbor.role}" if neighbor.role not in ("", "-") else ""
    yield Result(
        state=State(states.get(state_key, 3)),
        summary=f"State: {neighbor.state}{role}",
    )
    if neighbor.address:
        yield Result(state=State.OK, summary=f"Address: {neighbor.address}")
    yield Result(state=State.OK, summary=f"Process: {neighbor.process}")

    if neighbor.uptime is not None:
        yield from check_levels(
            neighbor.uptime,
            levels_lower=params.get("uptime_lower"),
            metric_name="uptime",
            render_func=render.timespan,
            label="Up for",
        )
    elif neighbor.uptime_text:
        yield Result(state=State.OK, summary=f"Up for: {neighbor.uptime_text}")

    yield Result(state=State.OK, notice=f"VRF: {neighbor.vrf}")
    yield Result(state=State.OK, notice=f"Neighbor ID: {neighbor.neighbor_id}")
    yield Result(state=State.OK, notice=f"Interface: {neighbor.interface}")
    if neighbor.interface_id:
        yield Result(state=State.OK, notice=f"Interface ID: {neighbor.interface_id}")
    yield Result(state=State.OK, notice=f"Priority: {neighbor.priority}")
    yield Result(state=State.OK, notice=f"Dead time: {neighbor.dead_time}")


def discover_cisco_xr_ospf_neighbor(section: Section) -> DiscoveryResult:
    yield from _discover("ospfv2", section)


def check_cisco_xr_ospf_neighbor(item: str, params: Mapping, section: Section) -> CheckResult:
    yield from _check("ospfv2", item, params, section)


def discover_cisco_xr_ospfv3_neighbor(section: Section) -> DiscoveryResult:
    yield from _discover("ospfv3", section)


def check_cisco_xr_ospfv3_neighbor(item: str, params: Mapping, section: Section) -> CheckResult:
    yield from _check("ospfv3", item, params, section)


_DEFAULT_PARAMS = {"state_not_found": 2}

check_plugin_cisco_xr_ospf_neighbor = CheckPlugin(
    name="cisco_xr_ospf_neighbor",
    sections=["cisco_xr_ospf_neighbors"],
    service_name="OSPF VRF neighbor %s",
    discovery_function=discover_cisco_xr_ospf_neighbor,
    check_function=check_cisco_xr_ospf_neighbor,
    check_default_parameters=_DEFAULT_PARAMS,
    check_ruleset_name="cisco_xr_ospf_neighbor",
)

check_plugin_cisco_xr_ospfv3_neighbor = CheckPlugin(
    name="cisco_xr_ospfv3_neighbor",
    sections=["cisco_xr_ospf_neighbors"],
    service_name="OSPFv3 VRF neighbor %s",
    discovery_function=discover_cisco_xr_ospfv3_neighbor,
    check_function=check_cisco_xr_ospfv3_neighbor,
    check_default_parameters=_DEFAULT_PARAMS,
    check_ruleset_name="cisco_xr_ospf_neighbor",
)
