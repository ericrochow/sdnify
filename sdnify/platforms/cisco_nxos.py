#!/usr/bin/env python
"""
Contains Cisco NXOS-specific functions, classes and definitions.
"""
from .platforms import SSHPlatform


class NXOS(SSHPlatform):
    """
    Class to interact with devices on the Cisco NXOS platform. Methods and
        Attributes inherited from the SSHPlatform parent class.
    """

    def __init__(self, **kwargs):
        """
        Instantiates an object of the Platform class with the appropriate options
            for a Cisco NX-OS device.

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
        self.platform = "cisco_nxos"
        self.templates = {
            "counters": "show_interfaces.template",
            "ifconfig": "",
            "xcvr": "nxos_show_interface_transceiver_details.template",
            "version": "",
            "inventory": "",
        }
        self.commands = {
            "counters": "show interface {}".format(arguments.interface_name),
            "ifconfig": "show running_config interface {}".format(
                arguments.interface_name
            ),
            "xcvr": "show interface {} transceiver details".format(
                arguments.interface_name
            ),
            "version": "",
            "inventory": "",
        }

        super().__init__(arguments, self.templates, self.commands)
