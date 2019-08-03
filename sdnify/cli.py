#!/usr/bin/env python
import argparse
import os
from os.path import dirname, realpath

import colorama

# from netmiko import ConnectHandler

from prettytable import PrettyTable

from termcolor import colored

# from textfsm import TextFSM

# import yaml

from .platforms.arista_eos import EOS
from .platforms.cisco_ios import IOS
from .platforms.cisco_nxos import NXOS
from .platforms.cisco_xe import IOSXE
from .platforms.cisco_xr import IOSXR
from .platforms.fortinet import FORTIOS
from .platforms.juniper_junos import JUNOS
from .platforms.paloalto_panos import PANOS
from .platforms.platforms import Platform
from ..__version__ import __version__


class Cli(object):
    """
    """

    def __init__(
        self, arguments, templates, commands, interface_name=None, address=None
    ):
        """
        """
        self.TEMPLATE_PATH = os.path.join(
            dirname(realpath(__file__))
            + "/fsm_templates/{}/".format(self.platform)
        )

        self.arguments = arguments
        self.templates = templates
        self.commands = commands
        self.device_name = arguments["device_name"]
        self.xcvr_template = open(
            os.path.join(self.TEMPLATE_PATH + self.templates["xcvr"])
        )
        self.counters_template = open(
            os.path.join(self.TEMPLATE_PATH + self.templates["counters"])
        )
        self.version_template = open(
            os.path.join(self.TEMPLATE_PATH + self.templates["version"])
        )
        self.inventory_template = open(
            os.path.join(self.TEMPLATE_PATH + self.templates["inventory"])
        )

    def colorize_tx_level(self, xcvr_details):
        """
        Colorizes the optical Tx levels based on the current value and the
            warn/alarm thresholds.

        Args:
          xcvr_details: A dict containing information about the current Tx
              value and the different thresholds
        Returns:
          A colorized string containing the current Tx level.
        """
        if float(xcvr_details["tx_current"]) > float(
            xcvr_details["tx_alarm_high"]
        ) or float(xcvr_details["tx_current"]) < float(
            xcvr_details["tx_alarm_low"]
        ):
            tx_value = colored(xcvr_details["tx_current"], "red")
        elif float(xcvr_details["tx_current"]) > float(
            xcvr_details["tx_warn_high"]
        ) or float(xcvr_details["tx_current"]) < float(
            xcvr_details["tx_warn_low"]
        ):
            tx_value = colored(xcvr_details["tx_current"], "yellow")
        else:
            tx_value = colored(xcvr_details["tx_current"], "green")
        return tx_value

    def colorize_rx_level(self, xcvr_details):
        """
        Colorizes the optical Rx levels based on the current value and the
            warn/alarm thresholds.

        Args:
          xcvr_details: A dict containing information about the current Rx
              value and the different thresholds
          Returns:
            A colorized string containing the current Rx level.
        """
        if not (
            xcvr_details["rx_alarm_high"]
            or xcvr_details["rx_alarm_low"]
            or xcvr_details["rx_warn_high"]
            or xcvr_details["rx_warn_low"]
        ):
            rx_value = xcvr_details["rx_current"]
        elif float(xcvr_details["rx_current"]) > float(
            xcvr_details["rx_alarm_high"]
        ) or float(xcvr_details["rx_current"]) < float(
            xcvr_details["rx_alarm_low"]
        ):
            rx_value = colored(["rx_current"], "red")
        elif float(xcvr_details["rx_current"]) > float(
            xcvr_details["rx_warn_high"]
        ) or float(xcvr_details["rx_current"]) < float(
            xcvr_details["rx_warn_low"]
        ):
            rx_value = colored(xcvr_details["rx_current"], "yellow")
        else:
            rx_value = colored(xcvr_details["rx_current"], "green")
        return rx_value

    def colorize_in_errors(self, counters_details):
        """
        Colorizes the input errors value in the event of a non-zero value.

        Args:
          counters_details: A dict containing
        Returns:
          A colorized string containing the number of input errors.
        """
        if int(counters_details["input_errors"]) > 0:
            counter = colored(counters_details["input_errors"], "red")
        else:
            counter = counters_details["input_errors"]
        return counter

    def colorize_out_errors(self, counters_details):
        """
        Colorizes the output errors value in the event of a non-zero value.

        Args:
          counters_details: A dict containing
        Returns:
          A colorized string containing the number of input errors.
        """
        if int(counters_details["output_errors"]) > 0:
            counter = colored(counters_details["output_errors"], "red")
        else:
            counter = counters_details["output_errors"]
        return counter

    def colorize_temperature(self, temperature):
        """
        Colorizes the temperature value based on threshold values.

        Args:
          temperature: A dict containing the current temperature and threshold
              values.
        Returns:
          A colorized string containing the temperature.
        """
        if not (
            temperature[""]
            or temperature[""]
            or temperature[""]
            or temperature[""]
        ):
            temperature_str = temperature[""]
        elif float(temperature[""]) > float(temperature[""]):
            temperature_str = colored(temperature[""], "red")
        elif float(temperature[""]) > float(temperature[""]):
            temperature_str = colored(temperature[""], "orange")
        elif float(temperature[""]) < float(temperature[""]):
            temperature_str = colored(temperature[""], "blue")
        elif float(temperature[""]) < float(temperature[""]):
            temperature_str = colored(temperature[""], "cyan")
        else:
            temperature_str = colored(temperature[""], "green")
        return temperature_str

    def colorize_voltage(self, voltage):
        """
        Colorizes the voltage value based on threshold values.

        Args:
          voltage: A dict containing the current voltage and threshold values.
        Returns:
          A colorized string containing the voltage.
        """
        if not (voltage[""] or voltage[""] or voltage[""] or voltage[""]):
            voltage_str = voltage[""]
        elif (float(voltage[""]) > float(voltage[""])) or (
            float(voltage[""]) < float(voltage[""])
        ):
            voltage_str = colored(voltage[""], "red")
        elif (float(voltage[""]) > float(voltage[""])) or (
            float(voltage[""]) < float(voltage[""])
        ):
            voltage_str = colored(voltage[""], "yellow")
        else:
            voltage_str = colored(voltage[""], "green")
        return voltage_str

    def colorize_amperage(self, amps):
        """
        Colorizes the current/amp value based on the threshold values.

        Args:
          amps: A dict containing the current current and threshold values.
        Returns:
          A colorized string containing the current/amperage.
        """
        pass

    @staticmethod
    def format_interface_results(details):
        """
        Formats interface detail results into a multiline string.

        Args:
          details: A dict containing the output of the gather_interface_details
              method.
        Returns:
          A the output of the gather_interface_details method formatted as a
              multiline string.
        """
        output = "\n"
        if details["config"]:
            output += "~" * 37
            output += "CONFIG"
            output += "~" * 37
            output += details["config_results"]
            output += "\n"
        if details["counters"]:
            counter_table = PrettyTable()
            counter_table.field_names = [
                "State",
                "In Rate",
                "Out Rate",
                "In Errors",
                "Out Errors",
            ]
            counter_table.add_row(
                [
                    details["state"],
                    details["input_rate"],
                    details["output_rate"],
                    details["input_errors"],
                    details["output_errors"],
                ]
            )
            output += "~" * 36
            output += "COUNTERS"
            output += "~" * 36
            output += "\n"
            output += str(counter_table)
            output += "\n"
        if details["xcvr"]:
            xcvr_table = PrettyTable()
            xcvr_table.field_names = [
                "Tx Power",
                "Rx Power",
                "Temperature",
                "Voltage",
            ]
            xcvr_table.add_row(
                [
                    "{} dBm".format(details["xcvr_rx_level"]),
                    "{} dBm".format(details["xcvr_rx_level"]),
                    "{} C".format(details["temperature_current"]),
                    "{} Volts".format(details["voltage_current"]),
                ]
            )
            output += "~" * 33
            output += "OPTICAL LEVELS"
            output += "~" * 33
            output += "\n"
            output += str(xcvr_table)
            output += "\n"
        return output

    def format_chassis_results(self, chassis_info):
        """
        Formats the results of the gather_chassis_details method into a
            multiline string.

        Args:
          chassis_info: A dict containing
        Returns:
          The results of the gather_interface_details method formatted into a
              multiline string.
        """
        output = "\n"
        chassis_table = PrettyTable()
        chassis_table.field_names = ["hostname", "software", "model"]
        chassis_table.add_row(
            chassis_info["hostname"],
            chassis_info["software"],
            chassis_info["model"],
        )
        return output

    def format_route_results(self, route):
        """
        Formats the results of the gather_route_results method into a multiline
            string.

        Args:
          route: A dict containing
        Returns:
          The results of the gather_route_results method formatted into a
              multiline string.
        """
        output = "\n"
        return output

    def gather_and_format_details(self):
        """
        Master method that runs the appropriate query and format methods.

        Args:
          None
        Returns:
          A multiline string containing the output ready to pring to console.
        """
        colorama.init()
        valid_query = bool(self.interface_name or self.chassis or self.route)
        if valid_query:
            output = "\n"
            output += ">" * 80
        if self.interface_name:
            interface = self.gather_interface_details()
            output += self.format_interface_results(interface)
        if self.chassis:
            chassis_info = self.gather_chassis_details()
            output += self.format_chassis_results(chassis_info)
        if self.route:
            route_info = self.gather_route_results()
            output += self.format_route_results(route_info)
        if valid_query:
            output += "<" * 80
            output += "\n"
        return output

    def initialize_parser():
        """
        Builds an argument parser object.

        Args:
          None
        Returns:
          A parser object that contains the flags and options passed by the
              CLI.
        """
        desc = "Adds some unicorn dust to your networking!"
        parser = argparse.ArgumentParser(description=desc, version=__version__)
        parser.add_argument(
            "device",
            action="store",
            help="The device which should be checked.",
        )
        parser.add_argument(
            "-p",
            "--platform",
            action="store",
            default="ios",
            choices=["ios", "nxos", "iosxr", "eos"],
            help="The device platform (default ios).",
        )
        parser.add_argument(
            "-i",
            "--interface",
            action="store",
            help="Return the given interface's configuration and details.",
        )
        parser.add_argument(
            "-c",
            "--chassis-details",
            action="store_true",
            help="Return information about the chassis.",
        )
        parser.add_argument(
            "-r",
            "--routes",
            action="store",
            help="Return route(s) to a given IP address.",
        )
        parser.add_argument(
            "-m",
            "--mac_addr",
            action="store",
            help=("Return MAC address table information for a given MAC"
                  " address.",
        )
        return parser.parse_args()
