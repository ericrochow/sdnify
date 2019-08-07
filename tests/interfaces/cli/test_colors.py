# import pytest

from sdnify.cli import Cli
from ...seed_data import rx_details, tx_details


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
    assert rx_string == "\x1b[33m0\x1b[0m"


def test_rx_colorization_alarm():
    rx_details["rx_current"] = "30"
    rx_string = Cli.colorize_rx_level(rx_details)
    assert rx_string == "\x1b[31m0\x1b[0m"


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
        "rx_current": "0",
    }
    rx_string = Cli.colorize_rx_level(rx_details)
    assert rx_string == "9000"


def test_in_errors_none():
    in_errors = Cli.colorize_in_errors(30)
    assert in_errors == "\x1b[31m30\x1b[0m"


def test_out_errors_none():
    out_errors = Cli.colorize_out_errors(0)
    assert out_errors == "0"
