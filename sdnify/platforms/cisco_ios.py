#!/usr/bin/env python
"""
Contains Cisco IOS-specific functions, classes and definitions.
"""
from .platforms import SSHPlatform


class IOS(SSHPlatform):
    """
    Class to interact with devices on the Cisco IOS platform. Methods and
        Attributes inherited from the SSHPlatform parent class.
    """

    def __init__(self, **kwargs):
        """
        Instantiates an object of the Platform class with the appropriate options
            for a Cisco IOS device.

        Args:
          None
        Returns:
          An instantiated Platform object.
        """
        if "interface" in kwargs:
            interface_name = kwargs["interface"]
        else:
            interface_name = None
        if "mac" in kwargs:
            mac = kwargs["mac"]
        else:
            mac = None
        if "route" in kwargs:
            route = kwargs["route"]
        else:
            route = None
        self.platform = "arista_eos"
        self.platform = "cisco_ios"
        self.templates = {
            "counters": "show_interfaces.template",
            "ifconfig": "show_interface_transceiver.template",
            "xcvr": "",
            "version": "",
            "inventory": "",
        }
        self.commands = {
            "counters": "show interfaces {}".format(interface_name),
            "ifconfig": "show running-config interface {}".format(
                interface_name
            ),
            "xcvr": "show interfaces {} transceiver".format(interface_name),
            "version": "",
            "inventory": "",
        }

        self.platform = "cisco_ios"
        super().__init__(arguments, self.templates, self.commands)
