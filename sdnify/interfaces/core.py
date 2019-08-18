#!/usr/bin/env python
"""
Contains interface methods common to all interfaces.
"""

import tablib

from .platforms.arista_eos import EOS
from .platforms.cisco_ios import IOS
from .platforms.cisco_nxos import NXOS
from .platforms.cisco_xe import IOSXE
from .platforms.cisco_xr import IOSXR
from .platforms.fortinet import FORTIOS
from .platforms.juniper_junos import JUNOS
from .platforms.paloalto_panos import PANOS


def create_ios_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = IOS(arguments)
    return scraper_object


def create_nxos_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = NXOS(arguments)
    return scraper_object


def create_iosxr_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = IOSXR(arguments)
    return scraper_object


def create_iosxe_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = IOSXE(arguments)
    return scraper_object


def create_eos_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = EOS(arguments)
    return scraper_object


def create_panos_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = PANOS(arguments)
    return scraper_object


def create_junos_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = JUNOS(arguments)
    return scraper_object


def create_fortios_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = FORTIOS(arguments)
    return scraper_object


def generate_scraper(**connect):
    """
    Master function to generate the scraper, scrape the results, then format
        them.

    Args:
      None
    Returns:
      None
    """
    platform = connect["platform"]
    if platform == "eos":
        scraper_object = create_eos_scraper(connect)
    elif platform == "ios":
        scraper_object = create_ios_scraper(connect)
    elif platform == "nxos":
        scraper_object = create_nxos_scraper(connect)
    elif platform == "iosxe":
        scraper_object = create_iosxe_scraper(connect)
    elif platform == "iosxr":
        scraper_object = create_iosxr_scraper(connect)
    elif platform == "fortinet":
        scraper_object = create_fortios_scraper(connect)
    elif platform == "junos":
        scraper_object = "juniper_junos"
    return scraper_object


def gather_interface_details(scraper_object):
    """
    Connects to the device to gather information about a given interface.

    Args:
      scraper_object: An instantiated object of the appropriate platform
    Returns:
      A dict containing the configuration, counters, statistics, and
          thresholds for the specified interface.
    """
    # TODO: Move colorization to CLI module
    scraper_object.device = scraper_object.build_device()
    config_results = scraper_object.config()
    counters_results = scraper_object.counters()
    xcvr_results = scraper_object.transceiver()
    details = {}
    if config_results:
        config_details = {"config": True, "config_results": config_results}
    else:
        config_details = {"config": False}
    details = {**details, **config_details}
    if counters_results:
        # TODO: Is tablib the right tool for the job? Seems convoluted to
        # modify existing data.
        """
        counters_details = tablib.Dataset()
        counters_details.headers = [
            "Counters",
            "Interface Name",
            "State",
            "Hardware Type",
            "MAC",
            "MTU",
            "Duplex",
            "Speed",
            "Bandwidth",
            "Encapsulation",
            "Input Rate",
            "Output Rate",
            "Input Errors",
            "Output Errors",
        ]
        counters_details.append(
            True,
            counters_results[0],
            "{}/{}".format(counters_results[1], counters_results[2]),
            counters_results[3],
            counters_results[4],
            counters_results[5],
            counters_results[6],
            counters_results[7],
            counters_results[8],
            counters_results[9],
            counters_results[10],
            counters_results[11],
            counters_results[12],
            counters_results[13],
        )
        """
        counters_details = {
            "counters": True,
            "interface_name": counters_results[0],
            "state": "{}/{}".format(counters_results[1], counters_results[2]),
            "hardware_type": counters_results[3],
            "mac": counters_results[4],
            "mtu": counters_results[5],
            "duplex": counters_results[6],
            "speed": counters_results[7],
            "bandwidth": counters_results[8],
            "encapsulation": counters_results[9],
            "input_rate": counters_results[10],
            "output_rate": counters_results[11],
            "input_errors": counters_results[12],
            "output_errors": counters_results[13],
        }
        counters_details["input_errors"] = scraper_object.colorize_in_errors(
            counters_details
        )
        counters_details["output_errors"] = scraper_object.colorize_out_errors(
            counters_details
        )
    else:
        counters_details = {"counters": False}
    details = {**details, **counters_details}
    if xcvr_results:
        xcvr_details = {
            "xcvr": True,
            "temperature_current": xcvr_results[1],
            "temperature_alarm_high": xcvr_results[2],
            "temperature_alarm_low": xcvr_results[3],
            "temperature_warn_high": xcvr_results[4],
            "temperature_warn_low": xcvr_results[5],
            "voltage_current": xcvr_results[6],
            "voltage_alarm_high": xcvr_results[7],
            "voltage_alarm_low": xcvr_results[8],
            "voltage_warn_high": xcvr_results[9],
            "voltage_warn_low": xcvr_results[10],
            "tx_current": xcvr_results[11],
            "tx_alarm_high": xcvr_results[12],
            "tx_alarm_low": xcvr_results[13],
            "tx_warn_high": xcvr_results[14],
            "tx_warn_low": xcvr_results[15],
            "rx_current": xcvr_results[16],
            "rx_alarm_high": xcvr_results[17],
            "rx_alarm_low": xcvr_results[18],
            "rx_warn_high": xcvr_results[19],
            "rx_warn_low": xcvr_results[20],
        }
        xcvr_details["xcvr_rx_level"] = scraper_object.colorize_rx_level(
            xcvr_details
        )
        xcvr_details["xcvr_tx_level"] = scraper_object.colorize_tx_level(
            xcvr_details
        )
    else:
        xcvr_details = {"xcvr": False}
    details = {**details, **xcvr_details}
    return details
