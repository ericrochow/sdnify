# import pytest

from sdnify.interfaces.cli import Cli
from ...seed_data.parsed_output.interface_data import (
    rx_details,
    tx_details,
    # current_details,
    voltage_details,
    temperature_details,
    counters_details,
)


def test_tx_colorization_warn():
    tx_details["tx_current"] = "17"
    tx_string = Cli.colorize_tx_level(tx_details)
    assert tx_string == "\x1b[33m17\x1b[0m"


def test_tx_colorization_alarm():
    tx_details["tx_current"] = "30"
    tx_string = Cli.colorize_tx_level(tx_details)
    assert tx_string == "\x1b[31m30\x1b[0m"


def test_tx_colorization_pass():
    tx_details["tx_current"] = "0"
    tx_string = Cli.colorize_tx_level(tx_details)
    assert tx_string == "\x1b[32m0\x1b[0m"


def test_tx_colorization_none():
    tx_details = {
        "tx_warn_high": "",
        "tx_alarm_high": "",
        "tx_warn_low": "",
        "tx_alarm_low": "",
        "tx_current": "9000",
    }
    tx_string = Cli.colorize_tx_level(tx_details)
    assert tx_string == "9000"


def test_rx_colorization_warn():
    rx_details["rx_current"] = "17"
    rx_string = Cli.colorize_rx_level(rx_details)
    assert rx_string == "\x1b[33m17\x1b[0m"


def test_rx_colorization_alarm():
    rx_details["rx_current"] = "30"
    rx_string = Cli.colorize_rx_level(rx_details)
    assert rx_string == "\x1b[31m30\x1b[0m"


def test_rx_colorization_pass():
    rx_details["rx_current"] = "0"
    rx_string = Cli.colorize_rx_level(rx_details)
    assert rx_string == "\x1b[32m0\x1b[0m"


def test_rx_colorization_none():
    rx_details = {
        "rx_warn_high": "",
        "rx_alarm_high": "",
        "rx_warn_low": "",
        "rx_alarm_low": "",
        "rx_current": "9000",
    }
    rx_string = Cli.colorize_rx_level(rx_details)
    assert rx_string == "9000"


def test_temp_colorization_alarm_high():
    temperature_details["temperature_current"] = "200"
    temp_string = Cli.colorize_temperature(temperature_details)
    assert temp_string == "\x1b[31m200\x1b[0m"


def test_temp_colorization_warn_high():
    temperature_details["temperature_current"] = "102"
    temp_string = Cli.colorize_temperature(temperature_details)
    assert temp_string == "\x1b[33m102\x1b[0m"


def test_temp_colorization_pass():
    temperature_details["temperature_current"] = "69"
    temp_string = Cli.colorize_temperature(temperature_details)
    assert temp_string == "\x1b[32m69\x1b[0m"


def test_temp_colorization_warn_low():
    temperature_details["temperature_current"] = "24"
    temp_string = Cli.colorize_temperature(temperature_details)
    assert temp_string == "\x1b[34m24\x1b[0m"


def test_temp_colorization_alarm_low():
    temperature_details["temperature_current"] = "-69"
    temp_string = Cli.colorize_temperature(temperature_details)
    assert temp_string == "\x1b[34m-69\x1b[0m"


def test_temp_colorization_none():
    temperature_details = {
        "temperature_warn_high": "",
        "temperature_warn_low": "",
        "temperature_alarm_high": "",
        "temperature_alarm_low": "",
        "temperature_current": "9000",
    }
    temp_string = Cli.colorize_temperature(temperature_details)
    assert temp_string == "9000"


def test_voltage_colorization_alarm():
    voltage_details["voltage_current"] = "300"
    voltage_string = Cli.colorize_voltage(voltage_details)
    assert voltage_string == "\x1b[31m300\x1b[0m"


def test_voltage_colorization_warn():
    voltage_details["voltage_current"] = "269"
    voltage_string = Cli.colorize_voltage(voltage_details)
    assert voltage_string == "\x1b[33m269\x1b[0m"


def test_voltage_colorization_pass():
    voltage_details["voltage_current"] = "208"
    voltage_string = Cli.colorize_voltage(voltage_details)
    assert voltage_string == "\x1b[32m208\x1b[0m"


def test_voltage_colorization_none():
    voltage_details = {
        "voltage_alarm_high": "",
        "voltage_warn_high": "",
        "voltage_warn_low": "",
        "voltage_alarm_low": "",
        "voltage_current": "24",
    }
    voltage_string = Cli.colorize_voltage(voltage_details)
    assert voltage_string == "24"


"""
def test_current_colorization_alarm():
    current_details["current_current"] = 42
    current_string = Cli.colorize_amperage(current_details)
    assert current_string == "\x1b[31m42\x1b[0m"


def test_current_colorization_warn():
    current_details["current_current"] = 26
    current_string = Cli.colorize_amperage(current_details)
    assert current_string == "\x1b[33m26\x1b[0m"


def test_current_colorization_pass():
    current_details["current_current"] = 20
    current_string = Cli.colorize_amperage(current_details)
    assert current_string == "\x1b[32m20\x1b[0m"


def test_current_colorization_none():
    current_details = {
        "current_alarm_high": "",
        "current_warn_high": "",
        "current_warn_low": "",
        "current_alarm_low": "",
        "current_current": "9000",
    }
    current_string = Cli.colorize_amperage(current_details)
    assert current_string == "24"
"""


def test_in_errors_none():
    in_errors = Cli.colorize_in_errors(counters_details)
    assert in_errors == "0"


def test_out_errors_none():
    out_errors = Cli.colorize_out_errors(counters_details)
    assert out_errors == "0"


def test_in_errors_positive():
    counters_details["input_errors"] = 30
    in_errors = Cli.colorize_in_errors(counters_details)
    assert in_errors == "\x1b[31m30\x1b[0m"


def test_out_errors_positive():
    counters_details["output_errors"] = 30
    out_errors = Cli.colorize_out_errors(counters_details)
    assert out_errors == "\x1b[31m30\x1b[0m"
