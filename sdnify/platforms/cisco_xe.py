#!/usr/bin/env python
"""
Contains Cisco IOS-XE-specific functions, classes and definitions.
"""
from . import SSHPlatform


class IOSXE(Platform):
    """
    Class to interact with devices on the Cisco IOS-XE platform. Methods and
        Attributes inherited from the SSHPlatform parent class.
    """

    def __init__(self, **kwargs):
        """
        Instantiates an object of the SSHPlatform class with the appropriate
            options for a Cisco IOS-XE device.

        Args:
          None
        Returns:
          An instantiated SSHPlatform object.
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
        self.platform = "cisco_xr"
        self.counters_template_name = ""
        self.xcvr_template_name = ""

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
