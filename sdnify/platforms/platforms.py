#!/usr/bin/env python
# import argparse
import os
from os.path import dirname, realpath

import requests

from netmiko import ConnectHandler

from prettytable import PrettyTable

from textfsm import TextFSM

import yaml


class Platform(object):
    """
    """

    def __init__(self, arguments):
        """
        """
        self.arguments = arguments


class SSHPlatform(Platform):
    """
    """

    def __init__(self, arguments, templates, commands):
        """
        """
        self.TEMPLATE_PATH = os.path.join(
            dirname(realpath(__file__))
            + "/fsm_templates/{}/".format(self.platform)
        )

        # self.arguments = arguments
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
        super().__init__(self, arguments)

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
        if "username" in self.arguments and "password" in self.arguments:
            username, password = (
                self.arguments["username"],
                self.arguments["password"],
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
        Master method that runs all appropriate commands.

        Args:
          None
        Returns:
          A dictionary containing the formatted results of the commands.
        """
        valid_query = bool(self.interface_name or self.chassis or self.route)
        results = {}
        if valid_query:
            if self.interface_name:
                results["interface_info"] = self.gather_interface_details()
            if self.chassis:
                results["chassis_info"] = self.gather_chassis_details()
            if self.route:
                results["route_info"] = self.gather_route_results()
        else:
            results["error"] = True
        return results


class APIPlatform(Platform):
    """
    """

    def __init__(self, arguments, filters, methods, **kwargs):

        """
        """
        self.filters = filters
        self.methods = methods
        self.username = arguments.get("username", default=None)
        self.password = arguments.get("password", default=None)
        self.token = arguments.get("api_token", default=None)
        self.base_url = arguments.get("base_url", default=None)
        self.port = arguments.get("port", 443)
        self.timeout = arguments.get("timeout", 30)
        self.verify_cert = arguments.get("verify_cert", default=True)
        self.raise_on_error = arguments.get("raise_on_error", default=True)
        self.sess = requests.Session()
        super().__init__(self, arguments)

    def build_device(self):
        """
        """
        pass

    def _get(self, request, payload=None, raw_json=True):
        """
        Sends an HTTP GET request.

        Args:
          request: blah
          payload: blah
          raw_json: blah
        Returns:
          The results of the GET request.
        """
        # TODO: Find way of generating base URL
        url = "{}/{}".format(self.base_url, request)
        r = self.sess.get(
            url,
            params=payload,
            headers=self.headers,
            auth=self.creds,
            timeout=self.timeout,
            verify=self.verify,
        )
        if r.ok:
            resp = r.json()
            if raw_json:
                return resp
            else:
                return r.text
        else:
            return r.raise_for_status()

    def _post(self, request, data=None, payload=None, raw_json=None):
        """
        Sends an HTTP POST request.

        Args:
          request: blah
          payload: blah
          data: blah
          raw_json: blah
        Returns:
          The results of the POST request.
        """
        # TODO: Add method of generating the base URL
        url = "{}/{}".format(self.base_url, request)
        r = self.sess.post(
            url,
            json=data,
            payload=payload,
            headers=self.headers,
            auth=self.creds,
            timeout=self.timeout,
            verify=self.verify,
        )
        if r.ok:
            resp = r.json()
            if raw_json:
                return resp
            else:
                return r.text
        else:
            return r.raise_for_status()
