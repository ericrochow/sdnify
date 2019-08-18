#!/usr/bin/env python
"""
Contains Arista EOS-specific functions, classes and definitions.
"""
from .platforms import SSHPlatform


class EOS(SSHPlatform):
    """
    Class to interact with devices on the Arista EOS platform. Methods and
        attributes inherited from the SSHPlatform parent class.
    """

    def __init__(self, **kwargs):
        """
        Instantiates an object of the Platform class with the appropriate options
            for an Arista EOS device.

        Args:
          None
        Returns:
          An instantiated Platform object.
        """
        arguments = {"device_name": kwargs["device"]}
        if "interface" in kwargs:
            arguments["interface_name"] = kwargs["interface"]
        else:
            arguments["interface_name"] = None
        if "mac" in kwargs:
            arguments["mac"] = kwargs["mac"]
        else:
            arguments["mac"] = None
        if "route" in kwargs:
            arguments["route"] = kwargs["route"]
        else:
            arguments["route"] = None
        self.platform = "arista_eos"
        self.templates = {
            "counters": "arista_eos_show_interfaces.template",
            "ifconfig": "",
            "xcvr": "arista_eos_show_interface_transceiver_details.template",
            "version": "",
            "inventory": "",
        }
        self.commands = {
            "counters": "show interface {}".format(
                arguments["interface_name"]
            ),
            "ifconfig": "show running-config interface {}".format(
                arguments["interface_name"]
            ),
            "xcvr": "show interfaces {} transceiver details".format(
                arguments["interface_name"]
            ),
            "version": "",
            "inventory": "",
        }

        self.platform = "arista_eos"
        super().__init__(kwargs, self.templates, self.commands)
