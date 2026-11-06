#!/usr/bin/env python3
# Copyright (C) 2026 Ricardo Ribeiro - License: GNU General Public License v2
#
# Checkmk 2.4 plugin: temperature and humidity sensors of Server Technology
# Sentry PDUs / CDUs.
#
# Supports both MIB generations:
#   * Sentry3-MIB (sysObjectID .1.3.6.1.4.1.1718.3), e.g. "Sentry Smart CDU",
#     Sentry Switched CDU. Table tempHumidSensorTable .1.3.6.1.4.1.1718.3.2.5.1
#   * Sentry4-MIB (sysObjectID .1.3.6.1.4.1.1718.4), e.g. PRO1/PRO2 PDUs.
#     Tables st4TemperatureSensors / st4HumiditySensors.
#
# Both SNMP sections feed the same parsed section "sentry_cdu_env", which is
# consumed by the two check plugins "sentry_cdu_temp" and "sentry_cdu_humidity".
# Thresholds come from the device unless overridden with the built-in rules
# "Temperature" and "Humidity Levels".
#
# Sentry3-MIB example:
#   tempHumidSensorID.1.1            = STRING: "A1"
#   tempHumidSensorName.1.1          = STRING: "Temp_Humid_Sensor_A1"
#   tempHumidSensorStatus.1.1        = INTEGER: found(0)
#   tempHumidSensorTempStatus.1.1    = INTEGER: normal(0)
#   tempHumidSensorTempValue.1.1     = INTEGER: 231 tenth degrees
#   tempHumidSensorTempLowThresh.1.1 = INTEGER: 5 degrees
#   tempHumidSensorTempHighThresh.1.1= INTEGER: 40 degrees
#   tempHumidSensorHumidStatus.1.1   = INTEGER: normal(0)
#   tempHumidSensorHumidValue.1.1    = INTEGER: 38 percentage relative humidity
#   tempHumidSensorHumidLowThresh.1.1= INTEGER: 10
#   tempHumidSensorHumidHighThresh.1.1=INTEGER: 80
#   tempHumidSensorTempScale.1.1     = INTEGER: celsius(0)

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from cmk.agent_based.v2 import (
    check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_value_store,
    render,
    Result,
    Service,
    SNMPSection,
    SNMPTree,
    startswith,
    State,
    StringTable,
)
from cmk.plugins.lib.temperature import check_temperature, TempParamType

Levels = tuple[float, float]


@dataclass(frozen=True)
class Reading:
    value: float | None
    unit: str  # "c" / "f" for temperature, "%" for humidity
    levels_upper: Levels | None
    levels_lower: Levels | None
    # Problem reported by the device that is *not* a threshold violation
    # (sensor lost, read error, ...). Threshold states are evaluated by Checkmk.
    error: tuple[State, str] | None


@dataclass(frozen=True)
class Section:
    temperature: Mapping[str, Reading]
    humidity: Mapping[str, Reading]


def _to_int(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None


def _item(sensor_id: str, name: str) -> str:
    sensor_id, name = sensor_id.strip(), name.strip()
    if name and name != sensor_id:
        return f"{sensor_id} {name}"
    return sensor_id or name


def _single_levels(value: int | None) -> Levels | None:
    return None if value is None else (float(value), float(value))


#   .--Sentry3-------------------------------------------------------------.

# tempHumidSensorStatus
_V3_SENSOR_STATUS = {
    0: (State.OK, "found"),
    1: (State.CRIT, "not found"),
    2: (State.CRIT, "lost"),
    3: (State.CRIT, "no communication"),
}

# tempHumidSensorTempStatus / tempHumidSensorHumidStatus
# 3 (low) and 4 (high) are threshold states -> evaluated via levels instead.
_V3_VALUE_ERRORS = {
    1: (State.CRIT, "not found"),
    2: (State.WARN, "reading"),
    5: (State.CRIT, "read error"),
    6: (State.CRIT, "lost"),
    7: (State.CRIT, "no communication"),
}


def _v3_reading(
    raw_value: int | None,
    divisor: int,
    unit: str,
    low: int | None,
    high: int | None,
    sensor_status: int | None,
    value_status: int | None,
) -> Reading | None:
    if sensor_status == 1 or value_status == 1:  # notFound: no sensor attached
        return None
    if raw_value is None or raw_value < 0:
        # -1 means "no value" (e.g. temperature-only probe has no humidity)
        if sensor_status == 0 and value_status in (None, 0, 1):
            return None
        value = None
    else:
        value = raw_value / divisor

    error = None
    if sensor_status is not None and sensor_status != 0:
        error = _V3_SENSOR_STATUS.get(sensor_status, (State.UNKNOWN, f"unknown ({sensor_status})"))
    elif value_status in _V3_VALUE_ERRORS:
        error = _V3_VALUE_ERRORS[value_status]
    elif value is None:
        error = (State.UNKNOWN, "no value available")

    return Reading(
        value=value,
        unit=unit,
        levels_upper=_single_levels(high),
        levels_lower=_single_levels(low),
        error=error,
    )


def parse_sentry3_env(string_table: StringTable) -> Section | None:
    temperature: dict[str, Reading] = {}
    humidity: dict[str, Reading] = {}

    for (
        sensor_id,
        name,
        sensor_status,
        temp_status,
        temp_value,
        temp_low,
        temp_high,
        humid_status,
        humid_value,
        humid_low,
        humid_high,
        temp_scale,
    ) in string_table:
        item = _item(sensor_id, name)
        if not item:
            continue
        s_status = _to_int(sensor_status)

        temp = _v3_reading(
            _to_int(temp_value),
            10,
            "f" if temp_scale == "1" else "c",
            _to_int(temp_low),
            _to_int(temp_high),
            s_status,
            _to_int(temp_status),
        )
        if temp is not None:
            temperature[item] = temp

        humid = _v3_reading(
            _to_int(humid_value),
            1,
            "%",
            _to_int(humid_low),
            _to_int(humid_high),
            s_status,
            _to_int(humid_status),
        )
        if humid is not None:
            humidity[item] = humid

    if not temperature and not humidity:
        return None
    return Section(temperature=temperature, humidity=humidity)


snmp_section_sentry3_env = SNMPSection(
    name="sentry3_cdu_env",
    parsed_section_name="sentry_cdu_env",
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.1718.3"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.1718.3.2.5.1",  # Sentry3-MIB::tempHumidSensorEntry
        oids=[
            "2",  # tempHumidSensorID
            "3",  # tempHumidSensorName
            "4",  # tempHumidSensorStatus
            "5",  # tempHumidSensorTempStatus
            "6",  # tempHumidSensorTempValue (tenth degrees)
            "7",  # tempHumidSensorTempLowThresh (degrees)
            "8",  # tempHumidSensorTempHighThresh (degrees)
            "9",  # tempHumidSensorHumidStatus
            "10",  # tempHumidSensorHumidValue (%RH)
            "11",  # tempHumidSensorHumidLowThresh
            "12",  # tempHumidSensorHumidHighThresh
            "13",  # tempHumidSensorTempScale celsius(0) fahrenheit(1)
        ],
    ),
    parse_function=parse_sentry3_env,
)

#   .--Sentry4-------------------------------------------------------------.

# Sentry4-MIB DeviceStatus. Threshold states (14-17) are evaluated via levels.
_V4_ERRORS = {
    1: (State.CRIT, "disabled"),
    2: (State.CRIT, "purged"),
    5: (State.WARN, "reading"),
    6: (State.WARN, "settle"),
    8: (State.CRIT, "lost"),
    9: (State.CRIT, "read error"),
    10: (State.CRIT, "no comm"),
    11: (State.CRIT, "pwr error"),
    18: (State.CRIT, "alarm"),
    21: (State.CRIT, "nvm fail"),
    22: (State.CRIT, "profile error"),
    23: (State.CRIT, "conflict"),
}
_V4_NOT_FOUND = 7


def _v4_levels(warn: int | None, crit: int | None) -> Levels | None:
    if warn is None and crit is None:
        return None
    if warn is None:
        warn = crit
    if crit is None:
        crit = warn
    assert warn is not None and crit is not None
    return float(warn), float(crit)


def _v4_readings(rows: StringTable, divisor: int, unit: str) -> dict[str, Reading]:
    readings: dict[str, Reading] = {}
    for sensor_id, name, value, status, low_alarm, low_warn, high_warn, high_alarm in rows:
        item = _item(sensor_id, name)
        int_status = _to_int(status)
        if not item or int_status == _V4_NOT_FOUND:
            continue
        int_value = _to_int(value)
        error = None
        if int_status in _V4_ERRORS:
            error = _V4_ERRORS[int_status]
        elif int_value is None:
            error = (State.UNKNOWN, "no value available")
        readings[item] = Reading(
            value=None if int_value is None or error else int_value / divisor,
            unit=unit,
            levels_upper=_v4_levels(_to_int(high_warn), _to_int(high_alarm)),
            levels_lower=_v4_levels(_to_int(low_warn), _to_int(low_alarm)),
            error=error,
        )
    return readings


def parse_sentry4_env(string_table: list[StringTable]) -> Section | None:
    scale_rows, temp_rows, humid_rows = string_table
    scale = scale_rows[0][0] if scale_rows and scale_rows[0] else "0"
    section = Section(
        temperature=_v4_readings(temp_rows, 10, "f" if scale == "1" else "c"),
        humidity=_v4_readings(humid_rows, 1, "%"),
    )
    if not section.temperature and not section.humidity:
        return None
    return section


_V4_SENSOR_COLUMNS = [
    "2.1.2",  # ...SensorID
    "2.1.3",  # ...SensorName
    "3.1.1",  # ...SensorValue
    "3.1.2",  # ...SensorStatus
    "4.1.2",  # ...SensorLowAlarm
    "4.1.3",  # ...SensorLowWarning
    "4.1.4",  # ...SensorHighWarning
    "4.1.5",  # ...SensorHighAlarm
]

snmp_section_sentry4_env = SNMPSection(
    name="sentry4_cdu_env",
    parsed_section_name="sentry_cdu_env",
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.1718.4"),
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.1718.4.1.9.1",  # st4TempSensorCommonConfig
            oids=["10"],  # st4TempSensorScale celsius(0) fahrenheit(1)
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.1718.4.1.9",  # st4TemperatureSensors
            oids=_V4_SENSOR_COLUMNS,
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.1718.4.1.10",  # st4HumiditySensors
            oids=_V4_SENSOR_COLUMNS,
        ),
    ],
    parse_function=parse_sentry4_env,
)

#   .--Temperature---------------------------------------------------------.


def discover_sentry_cdu_temp(section: Section) -> DiscoveryResult:
    for item in section.temperature:
        yield Service(item=item)


def check_sentry_cdu_temp(item: str, params: TempParamType, section: Section) -> CheckResult:
    if (reading := section.temperature.get(item)) is None:
        return
    if reading.error is not None:
        state, text = reading.error
        yield Result(state=state, summary=f"Sensor status: {text}")
    if reading.value is None:
        return
    yield from check_temperature(
        reading.value,
        params,
        unique_name=f"sentry_cdu_temp.{item}",
        value_store=get_value_store(),
        dev_unit=reading.unit,
        dev_levels=reading.levels_upper,
        dev_levels_lower=reading.levels_lower,
    )


check_plugin_sentry_cdu_temp = CheckPlugin(
    name="sentry_cdu_temp",
    sections=["sentry_cdu_env"],
    service_name="Temperature %s",
    discovery_function=discover_sentry_cdu_temp,
    check_function=check_sentry_cdu_temp,
    check_ruleset_name="temperature",
    check_default_parameters={},
)

#   .--Humidity------------------------------------------------------------.


def discover_sentry_cdu_humidity(section: Section) -> DiscoveryResult:
    for item in section.humidity:
        yield Service(item=item)


def _levels(user: Any, device: Levels | None) -> tuple[str, Levels] | None:
    if user:
        return ("fixed", (float(user[0]), float(user[1])))
    if device:
        return ("fixed", device)
    return None


def check_sentry_cdu_humidity(
    item: str, params: Mapping[str, Any], section: Section
) -> CheckResult:
    if (reading := section.humidity.get(item)) is None:
        return
    if reading.error is not None:
        state, text = reading.error
        yield Result(state=state, summary=f"Sensor status: {text}")
    if reading.value is None:
        return

    # User levels (rule "Humidity Levels") win over the device thresholds.
    user_configured = "levels" in params or "levels_lower" in params
    yield from check_levels(
        reading.value,
        levels_upper=_levels(
            params.get("levels"), None if user_configured else reading.levels_upper
        ),
        levels_lower=_levels(
            params.get("levels_lower"), None if user_configured else reading.levels_lower
        ),
        metric_name="humidity",
        render_func=render.percent,
        label="Humidity",
        boundaries=(0.0, 100.0),
    )
    yield Result(
        state=State.OK,
        notice="Levels source: " + ("user rule" if user_configured else "device"),
    )


check_plugin_sentry_cdu_humidity = CheckPlugin(
    name="sentry_cdu_humidity",
    sections=["sentry_cdu_env"],
    service_name="Humidity %s",
    discovery_function=discover_sentry_cdu_humidity,
    check_function=check_sentry_cdu_humidity,
    check_ruleset_name="humidity",
    check_default_parameters={},
)
