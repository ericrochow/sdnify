#!/usr/bin/env python
"""
Contains Cisco IOS-XE-specific functions, classes and definitions.
"""
from .platforms import SSHPlatform


class IOSXR(SSHPlatform):
    """
    Class to interact with devices on the Cisco IOS-XR platform. Methods and
        Attributes inherited from the SSHPlatform parent class.
    """

    def __init__(self, **kwargs):
        """
        Instantiates an object of the Platform class with the appropriate options
            for a Cisco IOS-XR device.

        Args:
          None
        Returns:
          An instantiated SSHPlatform object.
        """
        self.platform = "cisco_xr"
        self.templates = {
            "counters": "show_interfaces.template",
            "ifconfig": "",
            "xcvr": "show_controllers_phy.template",
            "version": "",
            "inventory": "",
        }
        self.commands = {
            "counters": "show interfaces {}".format(arguments.interface_name),
            "ifconfig": "show running-config interface {}".format(
                arguments.interface_name
            ),
            "xcvr": "show controllers {} phy".format(arguments.interface_name),
            "version": "",
            "inventory": "",
        }

        super().__init__(arguments, self.templates, self.commands)
