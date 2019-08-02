from . import Platform


class IOS(Platform):
    """
    Instantiates an object of the Platform class with the appropriate options
        for a Cisco IOS device.

    Args:
      None
    Returns:
      An instantiated Platform object.
    """

    def __init__(self, arguments):
        """
        """
        self.platform = "cisco_ios"
        self.templates = {
            "counters": "show_interfaces.template",
            "ifconfig": "show_interface_transceiver.template",
            "xcvr": "",
            "version": "",
            "inventory": "",
        }
        self.commands = {
            "counters": "show interfaces {}".format(arguments.interface_name),
            "ifconfig": "show running-config interface {}".format(
                arguments.interface_name
            ),
            "xcvr": "show interfaces {} transceiver".format(
                arguments.interface_name
            ),
            "version": "",
            "inventory": "",
        }

        self.platform = "cisco_ios"
        super().__init__(arguments, self.templates, self.commands)
