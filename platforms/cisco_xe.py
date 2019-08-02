from . import Platform


class IOSXE(Platform):
    """
    """

    def __init__(self, arguments):
        """
        """
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
