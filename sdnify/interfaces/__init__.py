from .cli import initialize_parser
from ..platforms.cisco_ios import IOS
from ..platforms.cisco_nxos import NXOS
from ..platforms.cisco_iosxr import IOSXR
from ..platforms.cisco_iosxe import IOSXE
from ..platforms.arista_eos import EOS
from ..platforms.paloalto_panos import PANOS
from ..platforms.juniper_junos import JUNOS
from ..platforms.fortinet import FORTIOS


def create_ios_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
        arguments: An argparse-formatted dictionary
    Returns:
        A screen scraping object.
    """
    scraper_object = IOS(arguments)
    return scraper_object


def create_nxos_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
        arguments: An argparse-formatted dictionary
    Returns:
        A screen scraping object.
    """
    scraper_object = NXOS(arguments)
    return scraper_object


def create_iosxr_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
        arguments: An argparse-formatted dictionary
    Returns:
        A screen scraping object.
    """
    scraper_object = IOSXR(arguments)
    return scraper_object


def create_iosxe_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
        arguments: An argparse-formatted dictionary
    Returns:
        A screen scraping object.
    """
    scraper_object = IOSXE(arguments)
    return scraper_object


def create_eos_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
        arguments: An argparse-formatted dictionary
    Returns:
        A screen scraping object.
    """
    scraper_object = EOS(arguments)
    return scraper_object


def create_panos_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
        arguments: An argparse-formatted dictionary
    Returns:
        A screen scraping object.
    """
    scraper_object = PANOS(arguments)
    return scraper_object


def create_junos_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
        arguments: An argparse-formatted dictionary
    Returns:
        A screen scraping object.
    """
    scraper_object = JUNOS(arguments)
    return scraper_object


def create_foritos_scraper(arguments):
    """
    Generates a screen scraper object.

    Args:
        arguments: An argparse-formatted dictionary
    Returns:
        A screen scraping object.
    """
    scraper_object = FORTIOS(arguments)
    return scraper_object


def generate_scraper(arguments):
    """
    Master function to generate the scraper, scrape the results, then
        format them.

    Args:
        None
    Returns:
        None
    """
    arguments = initialize_parser()
    parsed_args = {"device": arguments.device}
    if arguments.interface:
        parsed_args["interface"] = arguments.interface
    if arguments.route:
        parsed_args["route"] = arguments.route
    if arguments.mac_addr:
        parsed_args["mac"] = arguments.mac_addr
    if arguments.platform == "ios":
        scraper_object = create_ios_scraper(parsed_args)
    elif arguments.platform == "nxos":
        scraper_object = create_nxos_scraper(parsed_args)
    elif arguments.platform == "iosxr":
        scraper_object = create_iosxr_scraper(parsed_args)
    elif arguments.platform == "eos":
        scraper_object = create_eos_scraper(parsed_args)
    return scraper_object
