#!/usr/bin/env python
"""
Contains methods for use via the sdnify CLI.
"""
import argparse

import colorama

from prettytable import PrettyTable

from termcolor import colored

# from .core import generate_scraper
from sdnify.__version__ import __version__


class Cli(object):
    """
    """

    def __init__(self):
        """
        """
        pass

    @staticmethod
    def colorize_tx_level(xcvr_details):
        """
        Colorizes the optical Tx levels based on the current value and the
            warn/alarm thresholds.

        Args:
          xcvr_details: A dict containing information about the current Tx
              value and the different thresholds
        Returns:
          A colorized string containing the current Tx level.
        """
        if not (
            xcvr_details["tx_alarm_high"]
            or xcvr_details["tx_alarm_low"]
            or xcvr_details["tx_warn_high"]
            or xcvr_details["tx_warn_low"]
        ):
            tx_value = xcvr_details["tx_current"]
        elif float(xcvr_details["tx_current"]) > float(
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

    @staticmethod
    def colorize_rx_level(xcvr_details):
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
            rx_value = colored(xcvr_details["rx_current"], "red")
        elif float(xcvr_details["rx_current"]) > float(
            xcvr_details["rx_warn_high"]
        ) or float(xcvr_details["rx_current"]) < float(
            xcvr_details["rx_warn_low"]
        ):
            rx_value = colored(xcvr_details["rx_current"], "yellow")
        else:
            rx_value = colored(xcvr_details["rx_current"], "green")
        return rx_value

    @staticmethod
    def colorize_in_errors(counters_details):
        """
        Colorizes the input errors value in the event of a non-zero value.

        Args:
          counters_details: A dict containing
        Returns:
          A colorized string containing the number of input errors.
        """
        if float(counters_details["input_errors"]) > 0:
            counter = colored(counters_details["input_errors"], "red")
        else:
            counter = counters_details["input_errors"]
        return counter

    @staticmethod
    def colorize_out_errors(counters_details):
        """
        Colorizes the output errors value in the event of a non-zero value.

        Args:
          counters_details: A dict containing
        Returns:
          A colorized string containing the number of input errors.
        """
        if float(counters_details["output_errors"]) > 0:
            counter = colored(counters_details["output_errors"], "red")
        else:
            counter = counters_details["output_errors"]
        return counter

    @staticmethod
    def colorize_temperature(temperature):
        """
        Colorizes the temperature value based on threshold values.

        Args:
          temperature: A dict containing the current temperature and threshold
              values.
        Returns:
          A colorized string containing the temperature.
        """
        if not (
            temperature["temperature_alarm_high"]
            or temperature["temperature_alarm_low"]
            or temperature["temperature_warn_high"]
            or temperature["temperature_warn_low"]
        ):
            temperature_str = temperature["temperature_current"]
        elif float(temperature["temperature_current"]) > float(
            temperature["temperature_alarm_high"]
        ):
            temperature_str = colored(
                temperature["temperature_current"], "red"
            )
        elif float(temperature["temperature_current"]) > float(
            temperature["temperature_warn_high"]
        ):
            temperature_str = colored(
                temperature["temperature_current"], "yellow"
            )
        elif float(temperature["temperature_current"]) < float(
            temperature["temperature_warn_low"]
        ):
            temperature_str = colored(
                temperature["temperature_current"], "blue"
            )
        elif float(temperature["temperature_current"]) < float(
            temperature["temperature_alarm_low"]
        ):
            temperature_str = colored(
                temperature["temperature_current"], "cyan"
            )
        else:
            temperature_str = colored(
                temperature["temperature_current"], "green"
            )
        return temperature_str

    @staticmethod
    def colorize_voltage(voltage):
        """
        Colorizes the voltage value based on threshold values.

        Args:
          voltage: A dict containing the current voltage and threshold values.
        Returns:
          A colorized string containing the voltage.
        """
        if not (
            voltage["voltage_alarm_high"]
            or voltage["voltage_warn_high"]
            or voltage["voltage_warn_low"]
            or voltage["voltage_alarm_low"]
        ):
            voltage_str = voltage["voltage_current"]
        elif (
            float(voltage["voltage_current"])
            > float(voltage["voltage_alarm_high"])
        ) or (
            float(voltage["voltage_current"])
            < float(voltage["voltage_alarm_low"])
        ):
            voltage_str = colored(voltage["voltage_current"], "red")
        elif (
            float(voltage["voltage_current"])
            > float(voltage["voltage_warn_high"])
        ) or (
            float(voltage["voltage_current"])
            < float(voltage["voltage_warn_low"])
        ):
            voltage_str = colored(voltage["voltage_current"], "yellow")
        else:
            voltage_str = colored(voltage["voltage_current"], "green")
        return voltage_str

    @staticmethod
    def colorize_amperage(amps):
        """
        Colorizes the current/amp value based on the threshold values.

        Args:
          amps: A dict containing the current current and threshold values.
        Returns:
          A colorized string containing the current/amperage.
        """
        if not (
            amps["_alarm_high"]
            or amps["_warn_high"]
            or amps["_alarm_low"]
            or amps["_alarm_low"]
        ):
            amps_str = amps["_current"]
        elif (float(amps["_current"]) > float(amps["_alarm_high"])) or (
            float(amps["_current"]) < float(amps["_alarm_low"])
        ):
            amps_str = colored(amps["_current"], "red")
        elif (float(amps["_current"]) > float(amps["_warn_high"])) or (
            float(amps["_current"]) < float(amps["_warn_low"])
        ):
            amps_str = colored(amps["_current"], "yellow")
        else:
            amps_str = colored(amps["_current"], "green")
        return amps_str

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

    @staticmethod
    def format_chassis_results(chassis_info):
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

    @staticmethod
    def format_route_results(route):
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

    def gather_details(self):
        """
        Master method that runs the appropriate query and format methods.

        Args:
          None
        Returns:
          A multiline string containing the output ready to pring to console.
        """
        results = self.gather_details(self)
        colorama.init()
        if not results["error"]:
            interface_info = results.get("interface_info", default=None)
            chassis_info = results.get("chassis_info", default=None)
            route_info = results.get("route_info", default=None)
            output = "\n"
            output += ">" * 80
            if interface_info:
                output += self.format_interface_results(interface_info)
            if chassis_info:
                output += self.format_chassis_results(chassis_info)
            if route_info:
                output += self.format_route_results(route_info)
            output += "<" * 80
            output += "\n"
        else:
            output = colored("EPIC FAIL", "red")
        return output

    # def gather_and_format_details(self):
    # """
    # Master method that runs the appropriate query and format methods.

    # Args:
    # None
    # Returns:
    # A multiline string containing the output ready to pring to console.
    # """
    # colorama.init()
    # valid_query = bool(self.interface_name or self.chassis or self.route)
    # if valid_query:
    # output = "\n"
    # output += ">" * 80
    # if self.interface_name:
    # interface = self.gather_interface_details()
    # output += self.format_interface_results(interface)
    # if self.chassis:
    # chassis_info = self.gather_chassis_details()
    # output += self.format_chassis_results(chassis_info)
    # if self.route:
    # route_info = self.gather_route_results()
    # output += self.format_route_results(route_info)
    # if valid_query:
    # output += "<" * 80
    # output += "\n"
    # return output

    @staticmethod
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
            help=(
                "Return MAC address table information for a given MAC"
                " address."
            ),
        )
        arguments = parser.parse_args()
        return vars(arguments)
