#!/usr/bin/env python
"""
Contains Juniper JunOS-specific functions, classes and definitions.
"""
from .platforms import SSHPlatform


class JUNOS(SSHPlatform):
    """
    Class to interact with devices on the Juniper JunOS platform. Methods and
        Attributes inherited from the SSHPlatform parent class.
    """

    def __init__(self, **kwargs):
        """
        Instantiates an object of the Platform class with the appropriate options
            for an Juniper JunOS device.

        Args:
          None
        Returns:
          An instantiated Platform object.
        """
        self.platform = "juniper_junos"
        self.templates = {
            "counters": "show_interfaces.template",
            "ifconfig": "",
            "xcvr": "show_interface_transceiver_details.template",
            "version": "",
            "inventory": "",
        }
        self.commands = {
            "counters": "show interface {}".format(arguments.interface_name),
            "ifconfig": "show running-config interface {}".format(
                arguments.interface_name
            ),
            "xcvr": "show interfaces {} transceiver details".format(
                arguments.interface_name
            ),
            "version": "",
            "inventory": "",
        }

        super().__init__(arguments, self.templates, self.commands)
