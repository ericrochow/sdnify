#!/usr/bin/env python
import os
from os.path import dirname, realpath
import argparse
import colorama
from prettytable import PrettyTable
from netmiko import ConnectHandler
from termcolor import colored
from textfsm import TextFSM
import yaml

from .arista_eos import EOS
from .cisco_ios import IOS
from .cisco_nxos import NXOS
from .cisco_xe import IOSXE
from .cisco_xr import IOSXR
from .fortinet import FORTIOS
from .juniper_junos import JUNOS
from .paloalto_panos import PANOS
from ..__version__ import __version__


class Platform(object):
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

    def build_device(self):
        """
        Generates a netmiko connection handler. Attempts to read credentials
            first from arguments passed from the CLI, follwed by environment
            variables, from a configuration file, then finally falls back on
            prompting for credentials at run time.

        Args:
          None
        Returns:
          An instantiated netmiko connection handler.
        """
        if self.arguments.username and self.arguments.password:
            username, password = (
                self.arguments.username,
                self.arguments.password,
            )
        elif os.environ["NETUSERNAME"] and os.environ["NETPASSWORD"]:
            username, password = (
                os.environ["NETUSERNAME"],
                os.environ["NETPASSWORD"],
            )
        else:
            try:
                config_file = dirname(realpath(__file__)) + "/../.config.yml"
                with open(config_file) as saved_config:
                    configuration = yaml.safe_load(saved_config)["routers"]
                    username, password = (
                        configuration["username"],
                        configuration["password"],
                    )
            except IOError:
                import getpass

                username = input("Username: ")
                password = getpass("Password: ")
        creds = {"username": username, "password": password}
        device = {
            "ip": self.device_name,
            "username": creds["username"],
            "password": creds["password"],
            "device_type": self.platform,
        }
        self.net_connect = ConnectHandler(**device)

    def config(self):
        """
        Finds the running configuration of the interface.

        Args:
          None
        Returns:
          A multiline string containing the configure of the interface.
        """
        output = self.net_connect.send_command(self.ifconfig_command)
        return output

    def counters(self):
        """
        Finds an interfaces counters.

        Args:
          None
        Returns:
          A list of the parsed counter results.
        """
        output = self.net_connect.send_command(self.counters_command)
        fsm_template = TextFSM(self.counters_template)
        counters_results = fsm_template.ParseText(output)[0]
        self.interface_name = counters_results[0]
        return counters_results

    def transceiver(self):
        """
        Finds transceiver statistics for the given interface.

        Args:
          None
        Returns:
          A list of the parsed transceiver statistics.
        """
        output = self.net_connect.send_command(self.xcvr_command)
        fsm_template = TextFSM(self.xcvr_template)
        xcvr_results = fsm_template.ParseText(output)[0]
        self.interface_name = xcvr_results[0]
        return xcvr_results

    def routes(self):
        """
        Finds routes from the specified device to the specified address.

        Args:
          None
        Returns:
          A list of the parsed routing table output.
        """
        output = self.net_connect.send_command(self.route_command)
        fsm_template = TextFSM(self.route_template)
        route_results = fsm_template.ParseText(output)[0]
        return route_results

    def chassis_details(self):
        """
        Find chassis information for the given device.

        Args:
          None
        Returns:
          A list of parsed information from the chassis info output.
        """
        output = self.net_connect.send_command(self.chassis_details_command)
        fsm_template = TextFSM(self.chasssis_template)
        chassis_results = fsm_template.ParseText(output)[0]
        return chassis_results

    def software_version(self):
        """
        Finds the software version running on the given device.

        Args:
          None
        Returns:
          A list containing the parsed results of the version query.
        """
        output = self.net_connect.send_command(self.software_version_command)
        fsm_template = TextFSM(self.software_template)
        software_results = fsm_template.ParseText(output)[0]
        return software_results

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
            pigment = "red"
        elif float(xcvr_details["tx_current"]) > float(
            xcvr_details["tx_warn_high"]
        ) or float(xcvr_details["tx_current"]) < float(
            xcvr_details["tx_warn_low"]
        ):
            pigment = "yellow"
        else:
            pigment = "green"
        return colored(xcvr_details["tx_current"], pigment)

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

    def gather_interface_details(self):
        """
        Connects to the device to gather information about a given interface.

        Args:
          None
        Returns:
          A dict containing the configuration, counters, statistics, and
              thresholds for the specified interface.
        """
        self.device = self.build_device()
        config_results = self.config()
        counters_results = self.counters()
        xcvr_results = self.transceiver()
        details = {}
        if config_results:
            config_details = {"config": True, "config_results": config_results}
        else:
            config_details = {"config": False}
        details = {**details, **config_details}
        if counters_results:
            counters_details = {
                "counters": True,
                "interface_name": counters_results[0],
                "state": "{}/{}".format(
                    counters_results[1], counters_results[2]
                ),
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
            counters_details["input_errors"] = self.colorize_in_errors(
                counters_details
            )
            counters_details["output_errors"] = self.colorize_out_errors(
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
            xcvr_details["xcvr_rx_level"] = self.colorize_rx_level(
                xcvr_details
            )
            xcvr_details["xcvr_tx_level"] = self.colorize_tx_level(
                xcvr_details
            )
        else:
            xcvr_details = {"xcvr": False}
        details = {**details, **xcvr_details}
        return details

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

    def gather_details(self):
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


def create_ios_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = IOS(
        arguments.device, arguments.interfacece, arguments.route
    )
    return scraper_object


def create_nxos_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = NXOS(
        arguments.device, arguments.interfacece, arguments.route
    )
    return scraper_object


def create_iosxr_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = IOSXR(
        arguments.device, arguments.interfacece, arguments.route
    )
    return scraper_object


def create_iosxe_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = IOSXE(
        arguments.device, arguments.interfacece, arguments.route
    )
    return scraper_object


def create_eos_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = EOS(
        arguments.device, arguments.interfacece, arguments.route
    )
    return scraper_object


def create_panos_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = PANOS(
        arguments.device, arguments.interfacece, arguments.route
    )
    return scraper_object


def create_junos_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = JUNOS(
        arguments.device, arguments.interfacece, arguments.route
    )
    return scraper_object


def create_foritos_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
      arguments: An argparse-formatted dictionary
    Returns:
      A screen scraping object.
    """
    scraper_object = FORTIOS(
        arguments.device, arguments.interfacece, arguments.route
    )
    return scraper_object


def initialize_parser():
    """
    Builds an argument parser object.

    Args:
      None
    Returns:
      A parser object that contains the flags and options passed by the CLI.
    """
    desc = "Adds some unicorn dust to your networking!"
    parser = argparse.ArgumentParser(description=desc, version=__version__)
    parser.add_argument(
        "device", action="store", help="The device which should be checked."
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
    return parser.parse_args()


def main():
    """
    Master function to generate the scraper, scrape the results, then format
        them.

    Args:
      None
    Returns:
      None
    """
    arguments = initialize_parser()
    if arguments.platform == "ios":
        scraper_object = create_ios_scraper(arguments)
    elif arguments.platform == "nxos":
        scraper_object = create_nxos_scraper(arguments)
    elif arguments.platform == "iosxr":
        scraper_object = create_iosxr_scraper(arguments)
    elif arguments.platform == "eos":
        scraper_object = create_eos_scraper(arguments)
    output = scraper_object.gather_details()
    print(output)
