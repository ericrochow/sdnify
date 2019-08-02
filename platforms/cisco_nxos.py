from . import Platform


class NXOS(Platform):
    """
    Instantiates an object of the Platform class with the appropriate options
        for a Cisco NX-OS device.

    Args:
      None
    Returns:
      An instantiated Platform object.
    """

    def __init__(self, arguments):
        """
        """
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
