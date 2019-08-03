from . import Platform


class IOSXR(Platform):
    """
    Instantiates an object of the Platform class with the appropriate options
        for a Cisco IOS-XR device.

    Args:
      None
    Returns:
      An instantiated Platform object.
    """

    def __init__(self, **kwargs):
        """
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
