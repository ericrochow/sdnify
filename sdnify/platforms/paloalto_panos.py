#!/usr/bin/env python
"""
Contains Palo Alto PANOS-specific functions, classes and definitions.
"""
from .platforms import SSHPlatform


class PANOS(SSHPlatform):
    """
    Class to interact with devices on the Palo Alto PANOS platform. Methods and
        Attributes inherited from the SSHPlatform parent class.
    """

    def __init__(self, **kwargs):
        """
        Instantiates an object of the Platform class with the appropriate options
            for an Palo Alto PANOS device.

        Args:
          None
        Returns:
          An instantiated SSHPlatform object.
       """
        self.platform = "paloalto_panos"

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
