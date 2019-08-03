from . import Platform


class JUNOS(Platform):
    """
    Instantiates an object of the Platform class with the appropriate options
        for an Arista EOS device.

    Args:
      None
    Returns:
      An instantiated Platform object.
    """

    def __init__(self, **kwargs):
        """
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
